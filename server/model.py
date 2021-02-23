from entities import cjk_layout
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy


class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True


db = SQLAlchemy()


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Admin {self.username}>"


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    enable = db.Column(db.Boolean)
    projects = db.relationship("Project", backref="teacher", lazy=True)

    def __repr__(self):
        return f"<Teacher {self.id} {self.name}>"

    def to_obj(self):
        return {"id": self.id, "name": self.name, "description": self.description}

    def to_detail(self):
        return dict(
            self.to_obj(),
            **{
                "projects": [s.to_obj() for s in self.projects],
            },
        )


class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    score_classification_id = db.Column(
        db.Integer, db.ForeignKey("score_classification.id")
    )
    score = db.Column(db.Integer)

    def __repr__(self):
        return f"<Score {self.id}>"

    def to_obj(self):
        return {
            "id": self.id,
            "score_classification_id": self.score_classification_id,
            "score": self.score,
        }


class Score_classification(db.Model):
    __tablename__ = "score_classification"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    description = db.Column(db.String)

    def __repr__(self):
        return f"<Score {self.id}>"

    def to_obj(self):
        return {"id": self.id, "description": self.description}


class Score_weight(db.Model):
    __tablename__ = "score_weight"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    year = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    score_classification_id = db.Column(
        db.Integer, db.ForeignKey("score_classification.id")
    )

    def __repr__(self):
        return f"<Score {self.id}>"

    def to_obj(self):
        return {
            "id": self.id,
            "year": self.year,
            "weight": self.weight,
            "score_classification_id": self.score_classification_id,
        }


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    school_id = db.Column(db.String)
    name = db.Column(db.String, nullable=False)
    score = db.relationship("Score", backref="student", lazy=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    def __repr__(self):
        return f"<Stu {self.id} {self.name}>"

    def to_obj(self):
        return {
            "id": self.id,
            "name": self.name,
            "scores": [i.to_obj() for i in self.score],
        }


class Image(db.Model):
    __tablename__ = "projects_images"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    path = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

    def __repr__(self):
        return f"<Image {self.id}>"


class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    location = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<File {self.id}>"


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    uuid = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    presentation_order = db.Column(db.Integer)
    students = db.relationship("Student", backref="project", lazy=True)
    motivation = db.Column(db.String, nullable=True)
    faqs = db.Column(db.String, nullable=True)
    keywords = db.Column(db.JSON)
    classification = db.Column(db.String, nullable=True)
    arch_imgs_id = db.Column(db.JSON)
    cover_img_id = db.Column(db.Integer, nullable=True)
    members_imgs_id = db.Column(db.JSON)
    results_imgs_id = db.Column(db.JSON)
    videos_links = db.Column(db.JSON)
    report_file_id = db.Column(db.Integer, db.ForeignKey("files.id"))
    presentation_file_id = db.Column(db.Integer, db.ForeignKey("files.id"))
    program_file_id = db.Column(db.Integer, db.ForeignKey("files.id"))
    score = db.Column(db.Integer)

    def __repr__(self):
        return f"<Project {self.name}>"

    def to_obj(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "title": cjk_layout(self.name),
            "year": self.year,
            "description": cjk_layout(self.motivation),
            "cover": Image.query.get(self.cover_img_id).path
            if self.cover_img_id > 0
            else "",
            "keywords": self.keywords,
            "report_file": File.query.get(self.report_file_id).location
            if self.report_file_id > 0
            else "",
            "presentation_file": File.query.get(self.presentation_file_id).location
            if self.presentation_file_id > 0
            else "",
            "program_file": File.query.get(self.program_file_id).location
            if self.program_file_id > 0
            else "",
        }

    def to_detail(self):
        return dict(
            self.to_obj(),
            **{
                "students": [s.name for s in self.students],
                "teacher": self.teacher.name,
                "faqs": cjk_layout(self.faqs),
                "videos_links": [ytid for ytid in self.videos_links],
                "arch_imgs": [
                    Image.query.get(imgid).path for imgid in self.arch_imgs_id
                ],
                "members_imgs": [
                    Image.query.get(imgid).path for imgid in self.members_imgs_id
                ],
                "results_imgs": [
                    Image.query.get(imgid).path for imgid in self.results_imgs_id
                ],
            },
        )
