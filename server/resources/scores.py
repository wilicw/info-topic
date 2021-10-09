# -*- encoding: utf8-*-
from flask import Flask, Blueprint
from flask.helpers import send_file, send_from_directory
from flask_restful import Api, Resource, request, reqparse
from werkzeug import exceptions
import model
import err
import entities
import csv

app = Flask(__name__)
api_bp = Blueprint("scores", __name__, url_prefix="/api")
api = Api(api_bp)


class scores_weight(Resource):
    def get(self):
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        _, group = res
        if group != entities.group_admin:
            return err.not_allow_error
        weight_data = entities.to_obj_list(model.Score_weight.query.all())
        return weight_data

    def put(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        changed = data["data"]
        _, group = res
        if group != entities.group_admin:
            return err.not_allow_error
        for c in changed:
            year = int(c["year"])
            classification_id = int(c["classification_id"])
            weight = int(c["weight"])
            score_obj = model.Score_weight.query.filter_by(
                year=year, score_classification_id=classification_id
            ).first()
            if score_obj == None:
                new_score_obj = model.Score_weight(
                    year=year, score_classification_id=classification_id, weight=weight
                )
                model.db.session.add(new_score_obj)
            else:
                score_obj.weight = weight
            model.db.session.commit()
        entities.calculate_ranking()
        return {"status": "success"}


class scores_classification(Resource):
    def get(self):
        classification_data = entities.to_obj_list(
            model.Score_classification.query.filter_by(enabled=True).all()
        )
        return classification_data

    def post(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        description = data["description"]
        is_global = bool(data["global"])
        _, group = res
        if group != entities.group_admin:
            return err.not_allow_error
        score_classification_obj = model.Score_classification(
            description=description, is_global=is_global, enabled=True
        )
        model.db.session.add(score_classification_obj)
        model.db.session.commit()
        return {"status": "success"}

    def put(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        id = data["id"]
        description = data["description"]
        is_global = data["global"]
        _, group = res
        if group != entities.group_admin:
            return err.not_allow_error
        score_classification_obj = model.Score_classification.query.get(id)
        score_classification_obj.description = description
        score_classification_obj.is_global = is_global
        model.db.session.commit()
        return {"status": "success"}

    def delete(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        id = data["id"]
        _, group = res
        if group != entities.group_admin:
            return err.not_allow_error
        model.Score_classification.query.filter_by(id=id).first().enabled = False
        model.db.session.commit()
        return {"status": "success"}


class set_scores(Resource):
    def post(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        changed = data["data"]
        _, group = res
        if group != entities.group_teacher:
            return err.not_allow_error
        for c in changed:
            if c["student_id"] != -1:
                student_id = int(c["student_id"])
                classification_id = int(c["classification_id"])
                score = float(c["score"])
                model.Scorequery.filter_by(
                    student_id=student_id, score_classification_id=classification_id
                ).delete()
                new_score = model.Score(
                    student_id=student_id,
                    score_classification_id=classification_id,
                    score=score,
                )
                model.db.session.add(new_score)
                model.db.session.commit()
            elif c["uuid"] != -1:
                uuid = c["uuid"]
                classification_id = int(c["classification_id"])
                score = float(c["score"])
                project_id = model.Project.query.filter_by(uuid=uuid).first().id
                model.Project_score.query.filter_by(
                    project_id=project_id, score_classification_id=classification_id
                ).delete()
                new_score = model.Project_score(
                    project_id=project_id,
                    score_classification_id=classification_id,
                    score=score,
                )
                model.db.session.add(new_score)
                model.db.session.commit()
            else:
                return err.not_allow_error
        return {"status": "success"}


class import_scores(Resource):
    def post(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        classification_id = data["id"]
        entities.group_data = data["entities.group_data"]
        score_data = data["score_data"]
        _, group = res
        if group != entities.group_admin:
            return err.not_allow_error
        for item in zip(entities.group_data, score_data):
            __group, __score = item
            if len(__group) * len(__score) == 0:
                continue
            project_id = model.Project.query.filter_by(uuid=__group).first().id
            model.Project_score.query.filter_by(
                project_id=project_id, score_classification_id=classification_id
            ).delete()
            new_score = model.Project_score(
                project_id=project_id,
                score_classification_id=classification_id,
                score=__score,
            )
            model.db.session.add(new_score)
            model.db.session.commit()
        entities.calculate_ranking()
        return {"status": "success"}


class export_scores(Resource):
    def post(self):
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        _, group = res
        if group != entities.group_admin:
            return err.not_allow_error
        parser = reqparse.RequestParser()
        parser.add_argument("year", type=int, required=True)
        args = parser.parse_args()
        year = args["year"]
        students = model.Student.query.filter(
            model.Student.username.ilike(f"{year}%")
        ).all()
        stu_obj = sorted(
            list(map(lambda x: x.to_detail_scores(), students)),
            key=lambda x: x["username"],
        )
        weight = entities.to_obj_list(model.Score_weight.query.filter_by(year=year))

        classification = entities.to_obj_list(
            model.Score_classification.query.filter_by(enabled=True)
        )

        csv_header = (
            ["組別編號", "班級", "座號", "姓名"]
            + [i["description"] for i in classification]
            + ["總成績", "指導老師"]
        )

        csv_header_weight = (
            ["權重", "", "", ""]
            + [
                list(filter(lambda x: x["score_classification_id"] == i["id"], weight))[
                    0
                ]["weight"]
                for i in classification
            ]
            + ["", ""]
        )

        csv_dir = "/tmp/"
        csv_file = f"{year}.csv"

        with open(f"{csv_dir}{csv_file}", "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)
            writer.writerow(csv_header_weight)
            for stu in stu_obj:
                try:
                    project_id = stu["project_id"]
                    if project_id > 0:
                        project = entities.to_detail_obj_list(
                            model.Project.query.filter_by(id=project_id)
                        )[0]
                        uuid = project["uuid"]
                    else:
                        uuid = ""
                    _class = ""
                    if stu["username"][3] == "a":
                        _class = "甲班"
                    elif stu["username"][3] == "b":
                        _class = "乙班"
                    else:
                        _class = "綜高"
                    num = int(stu["username"][-2:])
                    name = stu["name"]
                    csv_data = [uuid, _class, num, name]

                    if uuid != "":
                        for i in classification:
                            score_obj = (
                                project["score"] if i["global"] else stu["scores"]
                            )

                            __score = list(
                                filter(
                                    lambda x: x["score_classification_id"] == i["id"],
                                    score_obj,
                                )
                            )
                            if len(__score) > 0:
                                __score = __score[0]["score"]
                            else:
                                __score = -1
                            csv_data.append(__score)

                        bias = 4
                        adding = 0
                        sum_score = 0
                        sum_w = 0
                        for i, w in enumerate(csv_header_weight[4:-2]):
                            original_score = csv_data[i + bias]
                            if csv_header[i] == "貢獻度":
                                adding += original_score
                            sum_score += original_score * w
                            sum_w += w

                        weight_score = (sum_score / sum_w) + adding
                        csv_data.append("{:.2f}".format(weight_score))
                        csv_data.append(project["teacher"])
                    writer.writerow(csv_data)
                except Exception as e:
                    print(e)
                    continue
        return send_from_directory(csv_dir, csv_file, as_attachment=True)


api.add_resource(scores_weight, "/scores/weight")
api.add_resource(scores_classification, "/scores/classification")
api.add_resource(set_scores, "/scores")
api.add_resource(import_scores, "/import_scores")
api.add_resource(export_scores, "/export_scores")
app.register_blueprint(api_bp)
