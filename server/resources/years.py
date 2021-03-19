# -*- encoding: utf8-*-
from flask import Flask, Blueprint
from flask_restful import Api, Resource
import model


app = Flask(__name__)
api_bp = Blueprint("years", __name__, url_prefix="/api/years")
api = Api(api_bp)


class years(Resource):
    def get(self):
        years = list(
            map(
                lambda x: int(x[0]),
                model.Project.query.with_entities(model.Project.year)
                .group_by(model.Project.year)
                .all(),
            )
        )
        return years


api.add_resource(years, "/")

app.register_blueprint(api_bp)