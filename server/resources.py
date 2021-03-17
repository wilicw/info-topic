# -*- encoding: utf8-*-
from flask.signals import request_started
from flask_restful import Resource, request, reqparse
from model import *
import entities
import err
import werkzeug
import os
from sqlalchemy.sql.expression import func
import scipy.stats as ss

group_student = "stu"
group_teacher = "teacher"
group_admin = "admin"


class ranking(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("year", type=int)
        parser.add_argument("sort", type=int, required=True)
        args = parser.parse_args()
        results = Project.query
        if args["year"] != None:
            year = int(args["year"])
            results = results.filter_by(year=year)
        if args["sort"] != None:
            cid = args["sort"]
            results = list(filter(lambda x: list(filter(
                lambda s: s.score_classification_id == cid, x.score))[0].score != 0, results.all()))
            if len(results) == 0:
                return []
            score = [list(filter(lambda s: s.score_classification_id == cid, p.score))[
                0].score for p in results]
            score = list(map(lambda x: max(score)-x, score))
            results = entities.to_simple_obj_list(results)
            res = []
            for i, rank in enumerate(ss.rankdata(score, method='min')):
                if rank <= 8:
                    results[i]["rank"] = int(rank)
                    res.append(results[i])
        return res


class login(Resource):
    def get(self):
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        return {"status": "success"}

    def post(self):
        data = request.json
        username = data["username"]
        password = data["password"]
        if (
            Student.query.filter_by(
                username=username, password=password).first()
            != None
        ):
            return entities.generate_token(username, group=group_student)
        if (
            Teacher.query.filter_by(
                username=username, password=password).first()
            != None
        ):
            return entities.generate_token(username, group=group_teacher)
        if Admin.query.filter_by(username=username, password=password).first() != None:
            return entities.generate_token(username, group=group_admin)
        return err.account_error


class projects(Resource):
    def get(self, id=None, uuid=None):
        if id != None:
            result = Project.query.get(id)
            if result == None:
                return err.topic_not_found
            return result.to_detail()
        elif uuid != None:
            result = Project.query.filter_by(uuid=uuid).first()
            if result == None:
                return err.topic_not_found
            return result.to_detail()
        else:
            parser = reqparse.RequestParser()
            parser.add_argument("random")
            parser.add_argument("highlight")
            parser.add_argument("keyword")
            parser.add_argument("year", type=int)
            parser.add_argument("search")
            parser.add_argument("token")
            args = parser.parse_args()
            if args["random"] != None:
                random_topics = (
                    Project.query.filter(
                        ~Project.name.ilike(""),
                        ~Project.motivation.ilike(""),
                    )
                    .order_by(func.rand())
                    .limit(12)
                    .all()
                )
                return list(map(lambda x: x.to_simple(), random_topics))
            if args["highlight"] != None:
                highlight = (
                    Project.query.filter(
                        ~Project.name.ilike(""),
                        ~Project.motivation.ilike(""),
                        Project.cover_img_id != 0,
                    )
                    .order_by(func.rand())
                    .limit(5)
                    .all()
                )
                return list(map(lambda x: x.to_simple(), highlight))
            if args["token"] != None:
                token = args["token"]
                res = entities.check_token(token)
                if res == None:
                    raise Exception("invalid token")
                user, group = res
                if group == group_student:
                    stu_obj = Student.query.filter_by(username=user).first()
                    return {"id": stu_obj.project_id}
                elif group == group_teacher:
                    topics = Project.query.filter_by(
                        teacher_id=Teacher.query.filter_by(
                            username=user).first().id
                    ).all()
                    topics = entities.to_detail_obj_list(topics)
                    return topics
                else:
                    return err.not_allow_error
            # filters
            results = Project.query
            if args["keyword"] != None:
                word = args["keyword"]
                utf8_word = "".join(["\\\\u%04x" % (ord(c)) for c in word])
                results = results.filter(
                    db.or_(
                        Project.keywords.ilike(f"%{word}%"),
                        Project.keywords.ilike(f"%{utf8_word}%"),
                    )
                )
            if args["year"] != None:
                y = int(args["year"])
                results = results.filter_by(year=y)
            if args["search"] != None:
                text = str(args["search"])
                results = results.filter(
                    db.or_(
                        Project.uuid.ilike(f"{text}"),
                        Project.name.ilike(f"%{text}%"),
                        Project.motivation.ilike(f"%{text}%"),
                        Project.faqs.ilike(f"%{text}%"),
                    )
                )
            return entities.to_obj_list(results.all())

    def post(self, id=None, uuid=None):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        data = data["data"]
        user, group = res
        if group != group_student:
            return err.account_error
        if uuid != None or id != None:
            return err.not_allow_error
        stu = Student.query.filter_by(username=user).first()
        stu_class = stu.username[:-2]
        if stu.project_id != -1:
            return err.not_allow_error
        uuid = data["uuid"]
        name = data["title"]
        if uuid == "" or name == "":
            return err.not_allow_error
        teacher = Teacher.query.filter_by(name=data["teacher"]).first()
        if teacher == None:
            return err.not_allow_error
        students = data["students"]
        teacher_id = teacher.id
        new_project = Project(
            uuid=uuid,
            name=name,
            teacher_id=teacher_id,
            year=int(stu_class[:-1]),
            presentation_order=0,
            motivation="",
            faqs="",
            keywords=[],
            classification="",
            arch_imgs_id=[],
            cover_img_id=-1,
            members_imgs_id=[],
            results_imgs_id=[],
            videos_links=[],
            report_file_id=-1,
            presentation_file_id=-1,
            program_file_id=-1,
            score=0,
        )
        db.session.add(new_project)
        db.session.commit()
        print(new_project.id)
        for s in students:
            student = Student.query.get(s)
            student.project_id = new_project.id
            db.session.commit()
        return {"status": "success"}

    def put(self, id=None, uuid=None):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        data = data["data"]
        user, group = res
        if uuid != None:
            return err.not_allow_error
        elif id != None:
            if group == group_teacher or group == group_admin:
                pass
            elif Student.query.filter_by(username=user).first().project_id != id:
                return err.not_allow_error
            result = Project.query.get(id)
            if result == None:
                return err.topic_not_found
            if group != group_student:
                result.uuid = data["uuid"]
            result.name = data["title"]
            result.keywords = [
                f"{entities.utf8_str_to_normal(k)}" for k in data["keywords"]
            ]
            result.motivation = data["description"]
            result.faqs = data["faqs"]
            result.videos_links = data["videos_links"]
            result.cover_img_id = entities.links_to_imgs([data["cover"]])[0]
            result.arch_imgs_id = entities.links_to_imgs(data["arch_imgs"])
            result.results_imgs_id = entities.links_to_imgs(
                data["results_imgs"])
            result.members_imgs_id = entities.links_to_imgs(
                data["members_imgs"])
            result.report_file_id = (
                entities.links_to_files([data["report_file"]])[0]
                if data["report_file"] != ""
                else -1
            )
            result.presentation_file_id = (
                entities.links_to_files([data["presentation_file"]])[0]
                if data["presentation_file"] != ""
                else -1
            )
            result.program_file_id = (
                entities.links_to_files([data["program_file"]])[0]
                if data["program_file"] != ""
                else -1
            )
            db.session.commit()
            return {"status": "success"}
        else:
            return err.not_allow_error


class years(Resource):
    def get(self):
        years = list(
            map(
                lambda x: int(x[0]),
                Project.query.with_entities(Project.year)
                .group_by(Project.year)
                .all(),
            )
        )
        return years


class teachers(Resource):
    def get(self, id=None, name=None):
        t = Teacher.query
        if id != None:
            result = t.get(id)
            if result == None:
                return err.teacher_not_found
            return result.to_detail()
        elif name != None:
            result = t.filter_by(name=name).first()
            if result == None:
                return err.teacher_not_found
            return result.to_detail()
        else:
            return entities.to_obj_list(t.filter_by(enable=True).all())


class upload(Resource):
    def post(self):
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        parser = reqparse.RequestParser()
        parser.add_argument(
            "file", type=werkzeug.datastructures.FileStorage, location="files", required=True
        )
        parser.add_argument("type", required=True)
        args = parser.parse_args()
        f = args["file"]
        fn = f.filename
        if entities.filename_validation(fn) == False:
            return err.upload_error
        fn = entities.make_unique(fn)
        fn = werkzeug.utils.secure_filename(fn)
        path = os.path.join(
            os.path.abspath(__file__ + "/.."),
            "..",
            entities.config.upload_path,
            fn,
        )
        f.save(path)
        fn = entities.config.url_prefix + fn
        db_f = None
        if args["type"] == "file":
            db_f = File(location=fn)
        elif args["type"] == "image":
            db_f = Image(path=fn, description="")
        else:
            raise Exception("Type not define")
        db.session.add(db_f)
        db.session.commit()
        return {"status": "success", "link": fn}


class change_password(Resource):
    def post(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        user, _ = res
        o_pass = data["original_pass"]
        password = data["pass"]
        if (
            obj := Student.query.filter_by(username=user, password=o_pass).first()
        ) != None:
            obj.password = password
            db.session.commit()
            return {"status": "success"}
        if (
            obj := Teacher.query.filter_by(username=user, password=o_pass).first()
        ) != None:
            obj.password = password
            db.session.commit()
            return {"status": "success"}
        if (
            obj := Admin.query.filter_by(username=user, password=o_pass).first()
        ) != None:
            obj.password = password
            db.session.commit()
            return {"status": "success"}
        return err.account_error


class get_students_by_project(Resource):
    def get(self, uuid):
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        user, group = res
        if group != group_teacher:
            return err.not_allow_error
        stu_obj = list(
            map(
                lambda x: x.to_detail_scores(),
                Project.query.filter_by(uuid=uuid).first().students,
            )
        )
        return stu_obj


class students(Resource):
    def get(self):
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        __, _ = res
        parser = reqparse.RequestParser()
        parser.add_argument("year", type=int, required=True)
        args = parser.parse_args()
        year = args["year"]
        students = Student.query.filter(
            Student.username.ilike(f"{year}%")).all()
        stu_obj = entities.to_obj_list(students)
        return stu_obj

    def post(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        selected_class = data["selected_class"]
        year = data["year"]
        name = data["name"]
        seat_num = data["seat_num"]
        school_id = data["school_id"]
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        for item in zip(name, seat_num, school_id):
            __name, __seat_num, __school_id = item
            if len(__name) * len(__seat_num) * len(__school_id) == 0:
                continue
            __seat_num = "{:2d}".format("__seat_num")
            new_stu = Student(
                username=f"{year}{selected_class}{__seat_num}",
                password=__school_id,
                school_id=__school_id,
                name=__name,
                project_id=-1,
            )
            db.session.add(new_stu)
            db.session.commit()
        return {"status": "success"}


class scores_weight(Resource):
    def get(self):
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        weight_data = entities.to_obj_list(Score_weight.query.all())
        return {"status": "success", "data": weight_data}

    def put(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        changed = data["data"]
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        for c in changed:
            year = int(c["year"])
            classification_id = int(c["classification_id"])
            weight = int(c["weight"])
            score_obj = Score_weight.query.filter_by(
                year=year, score_classification_id=classification_id
            ).first()
            score_obj.weight = weight
            db.session.commit()
        entities.calculate_ranking()
        return {"status": "success"}


class scores_classification(Resource):
    def get(self):
        classification_data = entities.to_obj_list(
            Score_classification.query.filter_by(enabled=True).all()
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
        if group != group_admin:
            return err.not_allow_error
        score_classification_obj = Score_classification(
            description=description, is_global=is_global, enabled=True
        )
        db.session.add(score_classification_obj)
        db.session.commit()
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
        if group != group_admin:
            return err.not_allow_error
        score_classification_obj = Score_classification.query.get(id)
        score_classification_obj.description = description
        score_classification_obj.is_global = is_global
        db.session.commit()
        return {"status": "success"}

    def delete(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        id = data["id"]
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        Score_classification.query.filter_by(id=id).first().enabled = False
        db.session.commit()
        return {"status": "success"}


class set_scores(Resource):
    def post(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        changed = data["data"]
        _, group = res
        if group != group_teacher:
            return err.not_allow_error
        for c in changed:
            if c["student_id"] != -1:
                student_id = int(c["student_id"])
                classification_id = int(c["classification_id"])
                score = float(c["score"])
                Score.query.filter_by(
                    student_id=student_id, score_classification_id=classification_id
                ).delete()
                new_score = Score(
                    student_id=student_id,
                    score_classification_id=classification_id,
                    score=score,
                )
                db.session.add(new_score)
                db.session.commit()
            elif c["uuid"] != -1:
                uuid = c["uuid"]
                classification_id = int(c["classification_id"])
                score = float(c["score"])
                project_id = Project.query.filter_by(uuid=uuid).first().id
                Project_score.query.filter_by(
                    project_id=project_id, score_classification_id=classification_id
                ).delete()
                new_score = Project_score(
                    project_id=project_id,
                    score_classification_id=classification_id,
                    score=score,
                )
                db.session.add(new_score)
                db.session.commit()
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
        group_data = data["group_data"]
        score_data = data["score_data"]
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        for item in zip(group_data, score_data):
            __group, __score = item
            if len(__group) * len(__score) == 0:
                continue
            project_id = Project.query.filter_by(uuid=__group).first().id
            Project_score.query.filter_by(
                project_id=project_id, score_classification_id=classification_id
            ).delete()
            new_score = Project_score(
                project_id=project_id,
                score_classification_id=classification_id,
                score=__score,
            )
            db.session.add(new_score)
            db.session.commit()
        entities.calculate_ranking()
        return {"status": "success"}
