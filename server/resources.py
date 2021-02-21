# -*- encoding: utf8-*-
from flask.globals import session
from flask_restful import Resource, request, reqparse
from flask import send_from_directory
from model import *
import schema, entities, err, werkzeug, os

group_student = "stu"
group_teacher = "teacher"
group_admin = "admin"


class login(Resource):
    def post(self):
        data = request.json
        auth_schema = schema.AuthSchema()
        try:
            res = auth_schema.load(data)
        except:
            return err.account_error
        username = res["username"]
        password = res["password"]
        if (
            Student.query.filter_by(username=username, password=password).first()
            != None
        ):
            return entities.generate_token(username, group=group_student)
        if (
            Teacher.query.filter_by(username=username, password=password).first()
            != None
        ):
            return entities.generate_token(username, group=group_teacher)
        if Admin.query.filter_by(username=username, password=password).first() != None:
            return entities.generate_token(username, group=group_admin)
        return err.account_error


class is_login(Resource):
    def post(self):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        return {"status": "success"}


class toipcs(Resource):
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
            return list(map(lambda x: x.to_obj(), Project.query.all()))


class teacher(Resource):
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
            return list(map(lambda x: x.to_obj(), t.filter_by(enable=True).all()))


class toipcs_by_year(Resource):
    def get(self, y=None):
        if y == None:
            years = list(
                map(
                    lambda x: int(x[0]),
                    Project.query.with_entities(Project.year)
                    .group_by(Project.year)
                    .all(),
                )
            )
            return years
        else:
            results = Project.query.filter_by(year=y)
            return entities.to_detail_obj_list(results)


class toipcs_by_keywords(Resource):
    def get(self, word):
        results = Project.query.filter(Project.keywords.contains(word)).all()
        return entities.to_detail_obj_list(results)


class search(Resource):
    def get(self, text):
        match_uuid = Project.query.filter(
            db.or_(
                Project.uuid.ilike(f"{text}"),
            )
        ).all()
        match_title = Project.query.filter(
            db.or_(
                Project.name.ilike(f"%{text}%"),
            )
        ).all()
        match_motivation = Project.query.filter(
            db.or_(
                Project.motivation.ilike(f"%{text}%"),
            )
        ).all()
        match_faqs = Project.query.filter(
            db.or_(
                Project.faqs.ilike(f"%{text}%"),
            )
        ).all()
        results = entities.remove_duplicates_preserving_order(
            match_uuid + match_title + match_motivation + match_faqs
        )
        return entities.to_detail_obj_list(results)


class upload(Resource):
    def post(self):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        parse = reqparse.RequestParser()
        parse.add_argument(
            "file", type=werkzeug.datastructures.FileStorage, location="files"
        )
        args = parse.parse_args()
        if args["file"] == None:
            return err.upload_error
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
        db_f = File(location=fn)
        db.session.add(db_f)
        db.session.commit()
        return {"status": "success", "link": entities.config.url_prefix + fn}


class upload_img(Resource):
    def post(self):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        parse = reqparse.RequestParser()
        parse.add_argument(
            "image", type=werkzeug.datastructures.FileStorage, location="files"
        )
        parse.add_argument("title")
        args = parse.parse_args()
        if args["image"] == None or args["title"] == None:
            return err.upload_error
        f = args["image"]
        fn = args["title"] + f.filename
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
        db_f = Image(path=fn)
        db.session.add(db_f)
        db.session.commit()
        return {"status": "success", "link": entities.config.url_prefix + fn}


class change_password(Resource):
    def post(self):
        data = request.json
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        user, _ = res
        try:
            o_pass = data["original_pass"]
            password = data["pass"]
        except:
            return err.not_allow_error
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


class get_topic_by_token(Resource):
    def post(self):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        user, group = res
        if group != group_student:
            return err.not_allow_error
        stu_obj = Student.query.filter_by(username=user).first()
        project_uuid = stu_obj.project.uuid
        return {"status": "success", "uuid": project_uuid}


class score_weight(Resource):
    def get(self):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        weight_data = list(map(lambda x: x.to_obj(), Score_weight.query.all()))
        return {"status": "success", "data": weight_data}

    def post(self):
        data = request.json
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
            changed = data["data"]
        except:
            return err.not_allow_error
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
        return {"status": "success"}


class score_classification(Resource):
    def get(self):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        classification_data = list(
            map(lambda x: x.to_obj(), Score_classification.query.all())
        )
        return {"status": "success", "data": classification_data}
