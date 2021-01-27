# -*- encoding: utf8-*-
from flask_restful import Resource
from model import *


class Login(Resource):
    def post(self):
        return 123


class get_teacher(Resource):
    def get(self):
        return 123


class get_toipcs_by_year(Resource):
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
            return list(map(lambda x: x.to_obj(), results))


class get_toipcs_by_keywords(Resource):
    def get(self, word):
        results = Project.query.filter(Project.keywords.contains(word)).all()
        return list(map(lambda x: x.to_obj(), results))
