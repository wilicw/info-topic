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
api.add_resource(resources.get_teacher, "/api/teacher")
api.add_resource(resources.get_toipcs_by_keywords, "/api/keyword/<string:word>")
api.add_resource(
    resources.get_toipcs_by_year, "/api/year", "/api/year/", "/api/year/<int:y>"
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)