# -*- encoding: utf8-*-
from flask_restful import Resource, request, reqparse
from model import *
import entities, err, werkzeug, os
from sqlalchemy.sql.expression import func

group_student = "stu"
group_teacher = "teacher"
group_admin = "admin"


class get_random_topics(Resource):
    def get(self):
        random_topics = (
            Project.query.filter(
                ~Project.name.ilike(""),
                ~Project.motivation.ilike(""),
            )
            .order_by(func.rand())
            .limit(12)
            .all()
        )
        return list(map(lambda x: x.to_simple(), random_topics))


class get_highlight_topics(Resource):
    def get(self):
        highlight = (
            Project.query.filter(
                ~Project.name.ilike(""),
                ~Project.motivation.ilike(""),
                Project.cover_img_id != 0,
            )
            .order_by(func.rand())
            .limit(5)
            .all()
        )
        return list(map(lambda x: x.to_simple(), highlight))

class get_topics_by_classification(Resource):
    def get(self, year, cid):
        projects = Project.query.filter_by(year=year).all()
        projects = sorted(projects, key=lambda x: list(filter(lambda s: s.score_classification_id == cid ,x.score))[0].score, reverse=True)
        return entities.to_obj_list(projects)[:8]


class login(Resource):
    def post(self):
        data = request.json
        try:
            username = data["username"]
            password = data["password"]
        except:
            return err.account_error
        if (
            Student.query.filter_by(username=username, password=password).first()
            != None
        ):
            return entities.generate_token(username, group=group_student)
        if (
            Teacher.query.filter_by(username=username, password=password).first()
            != None
        ):
            return entities.generate_token(username, group=group_teacher)
        if Admin.query.filter_by(username=username, password=password).first() != None:
            return entities.generate_token(username, group=group_admin)
        return err.account_error


class is_login(Resource):
    def post(self):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        return {"status": "success"}


class toipcs(Resource):
    def get(self, id=None, uuid=None):
        if id != None:
            result = Project.query.get(id)
            if result == None:
                return err.topic_not_found
            return result.to_detail()
        elif uuid != None:
            result = Project.query.filter_by(uuid=uuid).first()
            if result == None:
                return err.topic_not_found
            return result.to_detail()
        else:
            return list(map(lambda x: x.to_obj(), Project.query.all()))

    def post(self, id=None, uuid=None):
        data = request.json
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
            data = data["data"]
        except:
            return err.not_allow_error
        user, group = res
        if group != group_student:
            return err.account_error
        if uuid != None or id != None:
            return err.not_allow_error
        stu = Student.query.filter_by(username=user).first()
        stu_class = stu.username[:-2]
        if stu.project_id != -1:
            return err.not_allow_error
        try:
            uuid = data["uuid"]
            name = data["title"]
            if uuid == "" or name == "":
                return err.not_allow_error
            teacher = Teacher.query.filter_by(name=data["teacher"]).first()
            if teacher == None:
                return err.not_allow_error
            students = data["students"]
            teacher_id = teacher.id
        except:
            return err.not_allow_error
        new_project = Project(
            uuid=uuid,
            name=name,
            teacher_id=teacher_id,
            year=int(stu_class[:-1]),
            presentation_order=0,
            motivation="",
            faqs="",
            keywords=[],
            classification="",
            arch_imgs_id=[],
            cover_img_id=-1,
            members_imgs_id=[],
            results_imgs_id=[],
            videos_links=[],
            report_file_id=-1,
            presentation_file_id=-1,
            program_file_id=-1,
            score=0,
        )
        db.session.add(new_project)
        db.session.commit()
        print(new_project.id)
        for s in students:
            student = Student.query.get(s)
            student.project_id = new_project.id
            db.session.commit()
        return {"status": "success"}

    def put(self, id=None, uuid=None):
        data = request.json
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
            data = data["data"]
        except:
            return err.not_allow_error
        user, group = res
        if uuid != None:
            return err.not_allow_error
        elif id != None:
            if group == group_teacher or group == group_admin:
                pass
            elif Student.query.filter_by(username=user).first().project_id != id:
                return err.not_allow_error
            result = Project.query.get(id)
            if result == None:
                return err.topic_not_found
            try:
                if group != group_student:
                    result.uuid = data["uuid"]
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
                db.session.commit()
            except Exception as e:
                print(e)
                return err.not_allow_error
            return {"status": "success"}
        else:
            return err.not_allow_error


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
            return entities.to_obj_list(t.filter_by(enable=True).all())


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
            return entities.to_obj_list(results)


class toipcs_by_keywords(Resource):
    def get(self, word):
        utf8_word = "".join(["\\\\u%04x" % (ord(c)) for c in word])
        results = Project.query.filter(
            db.or_(
                Project.keywords.ilike(f"%{word}%"),
                Project.keywords.ilike(f"%{utf8_word}%"),
            )
        ).all()
        return entities.to_simple_obj_list(results)


class search(Resource):
    def get(self, text):
        match_uuid = Project.query.filter(
            db.or_(
                Project.uuid.ilike(f"{text}"),
            )
        ).all()
        match_title = Project.query.filter(
            db.or_(
                Project.name.ilike(f"%{text}%"),
            )
        ).all()
        match_motivation = Project.query.filter(
            db.or_(
                Project.motivation.ilike(f"%{text}%"),
            )
        ).all()
        match_faqs = Project.query.filter(
            db.or_(
                Project.faqs.ilike(f"%{text}%"),
            )
        ).all()
        results = entities.remove_duplicates_preserving_order(
            match_uuid + match_title + match_motivation + match_faqs
        )
        return entities.to_simple_obj_list(results)


class upload(Resource):
    def post(self):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        parse = reqparse.RequestParser()
        parse.add_argument(
            "file", type=werkzeug.datastructures.FileStorage, location="files"
        )
        args = parse.parse_args()
        if args["file"] == None:
            return err.upload_error
        f = args["file"]
        fn = f.filename
        if entities.filename_validation(fn) == False:
            return err.upload_error
        fn = entities.make_unique(fn)
        fn = werkzeug.utils.secure_filename(fn)
        path = os.path.join(
            os.path.abspath(__file__ + "/.."),
            "..",
            entities.config.upload_path,
            fn,
        )
        f.save(path)
        fn = entities.config.url_prefix + fn
        db_f = File(location=fn)
        db.session.add(db_f)
        db.session.commit()
        return {"status": "success", "link": fn}


class upload_img(Resource):
    def post(self):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        parse = reqparse.RequestParser()
        parse.add_argument(
            "image", type=werkzeug.datastructures.FileStorage, location="files"
        )
        parse.add_argument("title")
        args = parse.parse_args()
        if args["image"] == None or args["title"] == None:
            return err.upload_error
        f = args["image"]
        fn = args["title"] + f.filename
        if entities.filename_validation(fn) == False:
            return err.upload_error
        fn = entities.make_unique(fn)
        fn = werkzeug.utils.secure_filename(fn)
        path = os.path.join(
            os.path.abspath(__file__ + "/.."),
            "..",
            entities.config.upload_path,
            fn,
        )
        f.save(path)
        fn = entities.config.url_prefix + fn
        db_f = Image(path=fn, description="")
        db.session.add(db_f)
        db.session.commit()
        return {"status": "success", "link": fn}


class change_password(Resource):
    def post(self):
        data = request.json
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        user, _ = res
        try:
            o_pass = data["original_pass"]
            password = data["pass"]
        except:
            return err.not_allow_error
        if (
            obj := Student.query.filter_by(username=user, password=o_pass).first()
        ) != None:
            obj.password = password
            db.session.commit()
            return {"status": "success"}
        if (
            obj := Teacher.query.filter_by(username=user, password=o_pass).first()
        ) != None:
            obj.password = password
            db.session.commit()
            return {"status": "success"}
        if (
            obj := Admin.query.filter_by(username=user, password=o_pass).first()
        ) != None:
            obj.password = password
            db.session.commit()
            return {"status": "success"}
        return err.account_error


class get_topic_by_token(Resource):
    def post(self):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        user, group = res
        if group == group_student:
            stu_obj = Student.query.filter_by(username=user).first()
            return {"status": "success", "id": stu_obj.project_id}
        elif group == group_teacher:
            topics = Project.query.filter_by(
                teacher_id=Teacher.query.filter_by(username=user).first().id
            ).all()
            topics = entities.to_detail_obj_list(topics)
            return {"status": "success", "data": topics}
        else:
            return err.not_allow_error


class get_students_by_topic(Resource):
    def get(self, uuid):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        user, group = res
        if group != group_teacher:
            return err.not_allow_error
        stu_obj = list(
            map(
                lambda x: x.to_detail_scores(),
                Project.query.filter_by(uuid=uuid).first().students,
            )
        )
        return {"status": "success", "data": stu_obj}


class get_students_by_year(Resource):
    def get(self, year):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        __, _ = res
        students = Student.query.filter(Student.username.ilike(f"{year}%")).all()
        stu_obj = entities.to_obj_list(students)
        return {"status": "success", "data": stu_obj}


class score_weight(Resource):
    def get(self):
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
        except:
            return err.not_allow_error
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        weight_data = entities.to_obj_list(Score_weight.query.all())
        return {"status": "success", "data": weight_data}

    def put(self):
        data = request.json
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
            changed = data["data"]
        except:
            return err.not_allow_error
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        for c in changed:
            year = int(c["year"])
            classification_id = int(c["classification_id"])
            weight = int(c["weight"])
            score_obj = Score_weight.query.filter_by(
                year=year, score_classification_id=classification_id
            ).first()
            score_obj.weight = weight
            db.session.commit()
        entities.calculate_ranking()
        return {"status": "success"}


class score_classification(Resource):
    def get(self):
        classification_data = entities.to_obj_list(
            Score_classification.query.filter_by(enabled=True).all()
        )
        return {"status": "success", "data": classification_data}

    def post(self):
        data = request.json
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
            description = data["description"]
            is_global = bool(data["global"])
        except:
            return err.not_allow_error
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        score_classification_obj = Score_classification(
            description=description, is_global=is_global, enabled=True
        )
        db.session.add(score_classification_obj)
        db.session.commit()
        return {"status": "success"}

    def put(self):
        data = request.json
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
            id = data["id"]
            description = data["description"]
            is_global = data["global"]
        except:
            return err.not_allow_error
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        score_classification_obj = Score_classification.query.get(id)
        score_classification_obj.description = description
        score_classification_obj.is_global = is_global
        db.session.commit()
        return {"status": "success"}

    def delete(self):
        data = request.json
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
            id = data["id"]
        except:
            return err.not_allow_error
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        Score_classification.query.filter_by(id=id).first().enabled = False
        db.session.commit()
        return {"status": "success"}


class set_score(Resource):
    def post(self):
        data = request.json
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
            changed = data["data"]
        except:
            return err.not_allow_error
        _, group = res
        if group != group_teacher:
            return err.not_allow_error
        for c in changed:
            if c["student_id"] != -1:
                student_id = int(c["student_id"])
                classification_id = int(c["classification_id"])
                score = int(c["score"])
                Score.query.filter_by(
                    student_id=student_id, score_classification_id=classification_id
                ).delete()
                new_score = Score(
                    student_id=student_id,
                    score_classification_id=classification_id,
                    score=score,
                )
                db.session.add(new_score)
                db.session.commit()
            elif c["uuid"] != -1:
                uuid = c["uuid"]
                classification_id = int(c["classification_id"])
                score = int(c["score"])
                project_id = Project.query.filter_by(uuid=uuid).first().id
                Project_score.query.filter_by(
                    project_id=project_id, score_classification_id=classification_id
                ).delete()
                new_score = Project_score(
                    project_id=project_id,
                    score_classification_id=classification_id,
                    score=score,
                )
                db.session.add(new_score)
                db.session.commit()
            else:
                return err.not_allow_error
        return {"status": "success"}


class import_student(Resource):
    def post(self):
        data = request.json
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
            name = data["name"]
            account = data["account"]
            school_id = data["school_id"]
        except:
            return err.not_allow_error
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        for item in zip(name, account, school_id):
            __name, __account, __school_id= item
            if len(__name) * len(__account) * len(__school_id) == 0:
                continue
            new_stu = Student(
                username=__account,
                password=__school_id,
                school_id=__school_id,
                name=__name,
                project_id=-1,
            )
            db.session.add(new_stu)
            db.session.commit()
        return {"status": "success"}

class import_score(Resource):
    def post(self):
        data = request.json
        try:
            res = entities.check_token(request.headers["Authorization"])
            if res == None:
                raise Exception("invalid token")
            classification_id = data["id"]
            group_data = data["group_data"]
            score_data = data["score_data"]
        except:
            return err.not_allow_error
        _, group = res
        if group != group_admin:
            return err.not_allow_error
        for item in zip(group_data, score_data):
            __group, __score = item
            if len(__group) * len(__score) == 0:
                continue
            project_id = Project.query.filter_by(uuid=__group).first().id
            Project_score.query.filter_by(
                project_id=project_id, score_classification_id=classification_id
            ).delete()
            new_score = Project_score(
                project_id=project_id,
                score_classification_id=classification_id,
                score=__score,
            )
            db.session.add(new_score)
            db.session.commit()
        entities.calculate_ranking()
        return {"status": "success"}
