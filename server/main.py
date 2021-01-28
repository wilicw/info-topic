#!.env/bin/python
from flask import Flask, render_template
from flask_restful import Api
import resources, model
from entities import config
from schema import ma
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"{config.db_protocol}://{config.db_user}:{config.db_pass}@{config.db_host}:{config.db_port}/{config.db_name}"
app.config["MAX_CONTENT_LENGTH"] = 300 * 1024 * 1024

model.db.init_app(app)
CORS(app)
api = Api(app)
ma.init_app(app)

api.add_resource(resources.login, "/api/auth")
api.add_resource(
    resources.toipcs,
    "/api/topic",
    "/api/topic/",
    "/api/topics",
    "/api/topics/",
    "/api/topic/<int:id>",
    "/api/topic/<string:name>",
)
api.add_resource(
    resources.teacher,
    "/api/teacher",
    "/api/teacher/",
    "/api/teacher/<int:id>",
    "/api/teacher/<string:name>",
)
api.add_resource(
    resources.toipcs_by_year, "/api/year", "/api/year/", "/api/year/<int:y>"
)
api.add_resource(resources.toipcs_by_keywords, "/api/keyword/<string:word>")
api.add_resource(resources.search, "/api/search/<string:text>")
api.add_resource(resources.file, "/api/file/<int:id>")
api.add_resource(resources.upload, "/api/upload", "/api/upload/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)