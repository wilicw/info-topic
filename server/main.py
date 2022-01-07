#!.env/bin/python
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify
from flask_restful import Api
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
app.url_map.strict_slashes = False

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"message": str(e)}), 400


from resources import basic, projects, ranking, scores, students, teachers, years

app.register_blueprint(basic.api_bp)
app.register_blueprint(projects.api_bp)
app.register_blueprint(ranking.api_bp)
app.register_blueprint(scores.api_bp)
app.register_blueprint(students.api_bp)
app.register_blueprint(teachers.api_bp)
app.register_blueprint(years.api_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
