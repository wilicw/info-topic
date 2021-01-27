# -*- encoding: utf8-*-
from flask_restful import Resource, reqparse
from flask import jsonify, request, send_from_directory
from model import *


class Login(Resource):
    def post(self):
        return 123


class get_teacher(Resource):
    def get(self):
        return 123


class get_toipcs_by_year(Resource):
    def get(self):
        return 123


class get_toipcs_by_keywords(Resource):
    def get(self, word):
        results = Project.query.filter(Project.keywords.contains(word)).all()
        return jsonify(list(map(lambda x: x.to_obj(), results)))
