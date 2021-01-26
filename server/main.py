#!env/bin/python
from flask import Flask, render_template
from flask_restful import Api
import resources
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(resources.Login, "/api/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
