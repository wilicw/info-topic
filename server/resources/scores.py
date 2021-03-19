# -*- encoding: utf8-*-
from flask import Flask, Blueprint
from flask_restful import Api, Resource, request
import model
import err
import entities


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
        return {"status": "success", "data": weight_data}

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
            score_obj.weight = weight
            model.db.session.commit()
        entities.calculate_ranking()
        return {"status": "success"}


class scores_classification(Resource):
    def get(self):
        classification_data = entities.to_obj_list(
            model.Score_classification.query.filter_by(enabled=True).all()
        )
        return {"status": "success", "data": classification_data}

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


api.add_resource(scores_weight, "/scores/weight")
api.add_resource(scores_classification, "/scores/classification")
api.add_resource(set_scores, "/scores")
api.add_resource(import_scores, "/import_scores")
app.register_blueprint(api_bp)