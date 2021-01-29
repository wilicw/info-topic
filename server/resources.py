# -*- encoding: utf8-*-
from flask_restful import Resource, request, reqparse
from model import *
import schema, entities, err, werkzeug, os


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
            return entities.generate_token(username, group="stu")
        if (
            Teacher.query.filter_by(username=username, password=password).first()
            != None
        ):
            return entities.generate_token(username, group="teacher")
        if Admin.query.filter_by(username=username, password=password).first() != None:
            return entities.generate_token(username, group="admin")
        return err.account_error


class toipcs(Resource):
    def get(self, id=None, name=None):
        if id != None:
            result = Project.query.get(id)
            if result == None:
                return err.topic_not_found
            return result.to_detail()
        elif name != None:
            result = Project.query.filter_by(name=name).first()
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
        match_title = Project.query.filter(
            db.or_(
                Project.name.like(f"%{text}%"),
            )
        ).all()
        match_motivation = Project.query.filter(
            db.or_(
                Project.motivation.like(f"%{text}%"),
            )
        ).all()
        match_faqs = Project.query.filter(
            db.or_(
                Project.faqs.like(f"%{text}%"),
            )
        ).all()
        results = entities.remove_duplicates_preserving_order(
            match_title + match_motivation + match_faqs
        )
        return entities.to_detail_obj_list(results)


class file(Resource):
    def get(self, id):
        f = File.query.get(id)
        if f == None:
            return err.file_not_found
        return id


class upload(Resource):
    def post(self):
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
        return {"status": "success", "id": db_f.id}
