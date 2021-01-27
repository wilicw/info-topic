#!.env/bin/python
from flask import Flask, render_template
from flask_restful import Api
import resources, model
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = ""
model.db.init_app(app)
CORS(app)
api = Api(app)
api.add_resource(resources.Login, "/api/auth")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)