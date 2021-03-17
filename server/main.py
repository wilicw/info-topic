#!.env/bin/python
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify
from flask_restful import Api
import resources
import model
from entities import config
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"{config.db_protocol}://{config.db_user}:{config.db_pass}@{config.db_host}:{config.db_port}/{config.db_name}"
app.config["MAX_CONTENT_LENGTH"] = 300 * 1024 * 1024
app.config["PROPAGATE_EXCEPTIONS"] = True
model.db.init_app(app)
CORS(app)
api = Api(app)


# @app.errorhandler(Exception)
# def handle_exception(e):
#     return jsonify({"message": str(e)}), 400


api.add_resource(resources.login, "/api/auth")
api.add_resource(resources.upload, "/api/upload")
api.add_resource(resources.change_password, "/api/change_password")
api.add_resource(resources.scores_weight, "/api/scores/weight")
api.add_resource(resources.scores_classification, "/api/scores/classification")
api.add_resource(resources.set_scores, "/api/scores")
api.add_resource(resources.import_scores, "/api/import_scores")

api.add_resource(resources.projects, "/api/projects",
                 "/api/projects/<int:id>", "/api/projects/<string:uuid>")
api.add_resource(resources.ranking, "/api/ranking")
api.add_resource(resources.get_students_by_project,
                 "/api/projects/<string:uuid>/students")
api.add_resource(
    resources.teachers,
    "/api/teachers",
    "/api/teachers/<int:id>",
    "/api/teachers/<string:name>",
)
api.add_resource(resources.students, "/api/students")
api.add_resource(resources.years, "/api/years")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
