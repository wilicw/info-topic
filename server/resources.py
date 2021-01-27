# -*- encoding: utf8-*-
from re import match
from flask_restful import Resource, request
from model import *
import schema
import entities
import err


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
            == None
        ):
            return err.account_error
        return entities.generate_token(username)


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