# -*- encoding: utf8-*-
from flask import Flask, Blueprint
from flask_restful import Api, Resource, request, reqparse
import model
import entities
import err
import werkzeug
import os

app = Flask(__name__)
api_bp = Blueprint("basic", __name__, url_prefix="/api")
api = Api(api_bp)


class Login(Resource):
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
            model.Student.query.filter_by(username=username, password=password).first()
            != None
        ):
            return entities.generate_token(username, group=entities.group_student)
        if (
            model.Teacher.query.filter_by(username=username, password=password).first()
            != None
        ):
            return entities.generate_token(username, group=entities.group_teacher)
        if (
            model.Admin.query.filter_by(username=username, password=password).first()
            != None
        ):
            return entities.generate_token(username, group=entities.group_admin)
        return err.account_error


class ChangePassword(Resource):
    def post(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        user, _ = res
        o_pass = data["original_pass"]
        password = data["pass"]
        if (
            obj := model.Student.query.filter_by(username=user, password=o_pass).first()
        ) != None:
            obj.password = password
            model.db.session.commit()
            return {"status": "success"}
        if (
            obj := model.Teacher.query.filter_by(username=user, password=o_pass).first()
        ) != None:
            obj.password = password
            model.db.session.commit()
            return {"status": "success"}
        if (
            obj := model.Admin.query.filter_by(username=user, password=o_pass).first()
        ) != None:
            obj.password = password
            model.db.session.commit()
            return {"status": "success"}
        return err.account_error


class Upload(Resource):
    def post(self):
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        user, group = res
        if group != entities.group_student:
            uuid = user
        else:
            stu_obj = model.Student.query.filter_by(username=user).first()
            uuid = stu_obj.project.uuid
        parser = reqparse.RequestParser()
        parser.add_argument(
            "file",
            type=werkzeug.datastructures.FileStorage,
            location="files",
            required=True,
        )
        parser.add_argument("type", required=True)
        args = parser.parse_args()
        f = args["file"]
        fn = f.filename
        if entities.filename_validation(fn) == False:
            return err.upload_error
        fn = entities.make_unique(fn)
        fn = werkzeug.utils.secure_filename(fn)
        folder = os.path.join(
            os.path.abspath(__file__ + "/.."),
            "../..",
            entities.Config.upload_path,
            uuid,
        )
        if not os.path.exists(folder):
            os.mkdir(folder)
        path = os.path.join(folder, fn)
        f.save(path)
        fn = os.path.join(entities.Config.url_prefix, f"./{uuid}/", fn)
        db_f = None
        if args["type"] == "file":
            db_f = model.File(location=fn)
        elif args["type"] == "image":
            db_f = model.Image(path=fn, description="")
        else:
            raise Exception("Type not define")
        model.db.session.add(db_f)
        model.db.session.commit()
        return {"status": "success", "link": fn}


api.add_resource(Login, "/auth")
api.add_resource(Upload, "/upload")
api.add_resource(ChangePassword, "/change_password")
app.register_blueprint(api_bp)
