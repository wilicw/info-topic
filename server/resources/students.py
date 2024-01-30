# -*- encoding: utf8-*-
from flask import Flask, Blueprint
from flask_restful import Api, Resource, reqparse, request
import model
import err
import entities


app = Flask(__name__)
api_bp = Blueprint("students", __name__, url_prefix="/api/students")
api = Api(api_bp)


class Students(Resource):
    def get(self):
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        __, _ = res
        parser = reqparse.RequestParser()
        parser.add_argument("year", type=int, required=True)
        args = parser.parse_args()
        year = args["year"]
        students = model.Student.query.filter(
            model.Student.username.ilike(f"{year}%")
        ).all()
        stu_obj = entities.to_obj_list(students)
        return stu_obj

    def post(self):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        selected_class = data["selected_class"]
        year = data["year"]
        name = data["name"]
        seat_num = data["seat_num"]
        school_id = data["school_id"]
        _, group = res
        if group != entities.group_admin:
            return err.not_allow_error
        for item in zip(name, seat_num, school_id):
            __name, __seat_num, __school_id = item
            if len(__name) * len(__seat_num) * len(__school_id) == 0:
                continue
            __seat_num = "{:02d}".format(int(__seat_num))
            new_stu = model.Student(
                username=f"{year}{selected_class}{__seat_num}",
                password=__school_id,
                school_id=__school_id,
                name=__name,
                project_id=-1,
            )
            model.db.session.add(new_stu)
            model.db.session.commit()
        return {"status": "success"}


api.add_resource(Students, "/")

app.register_blueprint(api_bp)