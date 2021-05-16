# -*- encoding: utf8-*-
from flask import Flask, Blueprint
from flask_restful import Api, Resource, reqparse, request
import model
import err
import entities


app = Flask(__name__)
api_bp = Blueprint("teahers", __name__, url_prefix="/api/teachers")
api = Api(api_bp)


class teachers(Resource):
    def get(self, id=None, name=None):
        parser = reqparse.RequestParser()
        parser.add_argument("all")
        args = parser.parse_args()
        t = model.Teacher.query
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
            if args["all"] == None:
                return entities.to_obj_list(t.filter_by(enable=True).all())
            else:
                return entities.to_obj_list(t.all())
    def put(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        _, group = res
        if group != entities.group_admin:
            return err.not_allow_error
        for change in data["data"]:
            t = model.Teacher.query.get(change["id"])
            try:    
                if change["description"] != None:
                    t.description = change["description"]
            except:
                pass
            try:
                if change["enable"] != None:
                    t.enable = change["enable"]
            except:
                pass
            model.db.session.commit()
        return {"status": "success"}


api.add_resource(
    teachers,
    "/",
    "/<int:id>",
    "/<string:name>",
)

app.register_blueprint(api_bp)