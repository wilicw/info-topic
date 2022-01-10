# -*- encoding: utf8-*-
from flask import Flask, Blueprint
from flask_restful import Api, Resource, request, reqparse
import model
import entities
import err
from sqlalchemy.sql.expression import func


app = Flask(__name__)
api_bp = Blueprint("projects", __name__, url_prefix="/api/projects")
api = Api(api_bp)


class projects(Resource):
    def get(self, id=None, uuid=None):
        if id != None:
            result = model.Project.query.get(id)
            if result == None:
                return err.topic_not_found
            return result.to_detail()
        elif uuid != None:
            result = model.Project.query.filter_by(uuid=entities.normilize_uuid(uuid)).first()
            if result == None:
                return err.topic_not_found
            return result.to_detail()
        else:
            parser = reqparse.RequestParser()
            parser.add_argument("random")
            parser.add_argument("highlight")
            parser.add_argument("keyword")
            parser.add_argument("year", type=int)
            parser.add_argument("search")
            parser.add_argument("token")
            args = parser.parse_args()
            if args["random"] != None:
                random_topics = (
                    model.Project.query.filter(
                        ~model.Project.name.ilike(""),
                        ~model.Project.motivation.ilike(""),
                    )
                    .order_by(func.rand())
                    .limit(12)
                    .all()
                )
                return list(map(lambda x: x.to_simple(), random_topics))
            if args["highlight"] != None:
                highlight = (
                    model.Project.query.filter(
                        ~model.Project.name.ilike(""),
                        ~model.Project.motivation.ilike(""),
                        model.Project.cover_img_id != 0,
                    )
                    .order_by(func.rand())
                    .limit(5)
                    .all()
                )
                return list(map(lambda x: x.to_simple(), highlight))
            if args["token"] != None:
                token = args["token"]
                res = entities.check_token(token)
                if res == None:
                    raise Exception("invalid token")
                user, group = res
                if group == entities.group_student:
                    stu_obj = model.Student.query.filter_by(username=user).first()
                    return {"id": stu_obj.project_id}
                elif group == entities.group_teacher:
                    topics = model.Project.query.filter_by(
                        teacher_id=model.Teacher.query.filter_by(username=user)
                        .first()
                        .id
                    ).all()
                    topics = entities.to_detail_obj_list(topics)
                    return topics
                else:
                    return err.not_allow_error
            # filters
            results = model.Project.query
            if args["keyword"] != None:
                word = args["keyword"]
                utf8_word = "".join(["\\\\u%04x" % (ord(c)) for c in word])
                results = results.filter(
                    model.db.or_(
                        model.Project.keywords.ilike(f"%{word}%"),
                        model.Project.keywords.ilike(f"%{utf8_word}%"),
                    )
                )
            if args["year"] != None:
                y = int(args["year"])
                results = results.filter_by(year=y)
            if args["search"] != None:
                text = str(args["search"])
                results = results.filter(
                    model.db.or_(
                        model.Project.uuid.ilike(f"{text}"),
                        model.Project.name.ilike(f"%{text}%"),
                        model.Project.motivation.ilike(f"%{text}%"),
                        model.Project.faqs.ilike(f"%{text}%"),
                    )
                )
            return entities.to_obj_list(results.all())

    def post(self, id=None, uuid=None):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        data = data["data"]
        user, group = res
        if group != entities.group_student:
            return err.account_error
        if uuid != None or id != None:
            return err.not_allow_error
        stu = model.Student.query.filter_by(username=user).first()
        stu_class = stu.username[:-2]
        if stu.project_id != -1:
            return err.not_allow_error
        uuid = entities.normilize_uuid(data["uuid"])
        name = data["title"]
        if uuid == "" or name == "":
            return err.not_allow_error
        teacher = model.Teacher.query.filter_by(name=data["teacher"]).first()
        if teacher == None:
            return err.not_allow_error
        students = data["students"]
        teacher_id = teacher.id
        new_project = model.Project(
            uuid=uuid,
            name=name,
            teacher_id=teacher_id,
            year=int(stu_class[:-1]),
        )
        model.db.session.add(new_project)
        model.db.session.commit()
        print(new_project.id)
        for s in students:
            student = model.Student.query.get(s)
            student.project_id = new_project.id
            model.db.session.commit()
        return {"status": "success"}

    def put(self, id=None, uuid=None):
        data = request.json
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        data = data["data"]
        user, group = res
        if uuid != None:
            return err.not_allow_error
        elif id != None:
            if group == entities.group_teacher or group == entities.group_admin:
                pass
            elif model.Student.query.filter_by(username=user).first().project_id != id:
                return err.not_allow_error
            result = model.Project.query.get(id)
            if result == None:
                return err.topic_not_found
            if group != entities.group_student:
                result.uuid = entities.normilize_uuid(data["uuid"])
            result.name = data["title"]
            result.keywords = [
                f"{entities.utf8_str_to_normal(k)}" for k in data["keywords"]
            ]
            result.motivation = data["description"]
            result.faqs = data["faqs"]
            result.videos_links = data["videos_links"]
            result.cover_img_id = entities.links_to_imgs([data["cover"]])[0]
            result.arch_imgs_id = entities.links_to_imgs(data["arch_imgs"])
            result.results_imgs_id = entities.links_to_imgs(data["results_imgs"])
            result.members_imgs_id = entities.links_to_imgs(data["members_imgs"])
            result.report_file_id = (
                entities.links_to_files([data["report_file"]])[0]
                if data["report_file"] != ""
                else -1
            )
            result.presentation_file_id = (
                entities.links_to_files([data["presentation_file"]])[0]
                if data["presentation_file"] != ""
                else -1
            )
            result.program_file_id = (
                entities.links_to_files([data["program_file"]])[0]
                if data["program_file"] != ""
                else -1
            )
            model.db.session.commit()
            return {"status": "success"}
        else:
            return err.not_allow_error


class get_students_by_project(Resource):
    def get(self, uuid):
        res = entities.check_token(request.headers["Authorization"])
        if res == None:
            raise Exception("invalid token")
        user, group = res
        if group != entities.group_teacher:
            return err.not_allow_error
        stu_obj = list(
            map(
                lambda x: x.to_detail_scores(),
                model.Project.query.filter_by(uuid=entities.normilize_uuid(uuid).first().students,
            )
        )
        return stu_obj


api.add_resource(projects, "/", "/<int:id>", "/<string:uuid>")
api.add_resource(get_students_by_project, "/<string:uuid>/students")
app.register_blueprint(api_bp)
