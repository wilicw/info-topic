# -*- encoding: utf8-*-
from flask import Flask, Blueprint
from flask_restful import Api, Resource
import model
import err
import entities


app = Flask(__name__)
api_bp = Blueprint("teahers", __name__, url_prefix="/api/teachers")
api = Api(api_bp)


class teachers(Resource):
    def get(self, id=None, name=None):
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
            return entities.to_obj_list(t.filter_by(enable=True).all())


api.add_resource(
    teachers,
    "/",
    "/<int:id>",
    "/<string:name>",
)

app.register_blueprint(api_bp)