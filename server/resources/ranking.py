# -*- encoding: utf8-*-
from flask import Flask, Blueprint
from flask_restful import Api, Resource, reqparse
import model
import entities
import scipy.stats as ss


app = Flask(__name__)
api_bp = Blueprint("ranking", __name__, url_prefix="/api/ranking")
api = Api(api_bp)


class ranking(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("year", type=int)
        parser.add_argument("sort", type=int, required=True)
        args = parser.parse_args()
        results = model.Project.query
        if args["year"] != None:
            year = int(args["year"])
            results = results.filter_by(year=year)
        if args["sort"] != None:
            cid = args["sort"]
            results = list(
                filter(
                    lambda x: list(
                        filter(lambda s: s.score_classification_id == cid, x.score)
                    )[0].score
                    != 0,
                    results.all(),
                )
            )
            if len(results) == 0:
                return []
            score = [
                list(filter(lambda s: s.score_classification_id == cid, p.score))[
                    0
                ].score
                for p in results
            ]
            score = list(map(lambda x: max(score) - x, score))
            results = entities.to_simple_obj_list(results)
            res = []
            for i, rank in enumerate(ss.rankdata(score, method="min")):
                if rank <= 8:
                    results[i]["rank"] = int(rank)
                    res.append(results[i])
        return res


api.add_resource(ranking, "/")
app.register_blueprint(api_bp)