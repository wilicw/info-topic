# -*- encoding: utf8-*-
from flask_restful import Resource, reqparse
from flask import jsonify, request, send_from_directory
import model


class Login(Resource):
    def get(self):
        s = model.Student.query.filter_by(username="110b17").first()
        mi = s.project.keywords[0]
        print(mi)
        return 123