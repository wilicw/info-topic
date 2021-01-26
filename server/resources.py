# -*- encoding: utf8-*-
from flask_restful import Resource, reqparse
from flask import jsonify, request, send_from_directory


class Login(Resource):
    def get(self):
        return 123