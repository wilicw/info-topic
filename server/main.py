#!.env/bin/python
from flask import Flask, render_template
from flask_restful import Api
from configparser import ConfigParser
import resources, model
from flask_cors import CORS

conf = ConfigParser()
conf.read("config.ini", encoding="utf-8")
db_config = conf["db"]
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"{db_config['protocol']}://{db_config['user']}:{db_config['pass']}@{db_config['host']}:{db_config['port']}/{db_config['db_name']}"

model.db.init_app(app)
CORS(app)
api = Api(app)

api.add_resource(resources.Login, "/api/auth")
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)