from configparser import ConfigParser
from uuid import uuid4
import jwt, pangu, json
import threading
import scipy.stats as ss

conf = ConfigParser()
conf.read("config.ini", encoding="utf-8")


class config:
    db_config = conf["db"]
    jwt_config = conf["jwt"]
    upload_config = conf["upload"]
    db_protocol = db_config["protocol"]
    db_user = db_config["user"]
    db_pass = db_config["pass"]
    db_host = db_config["host"]
    db_port = db_config["port"]
    db_name = db_config["db_name"]
    secret = jwt_config["secret"]
    upload_path = upload_config["path"]
    allow_file_type = upload_config["allow_file_type"].split(",")
    url_prefix = upload_config["url_prefix"]


def remove_duplicates_preserving_order(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def to_simple_obj_list(ll):
    return list(map(lambda x: x.to_simple(), ll))


def to_obj_list(ll):
    return list(map(lambda x: x.to_obj(), ll))


def to_detail_obj_list(ll):
    return list(map(lambda x: x.to_detail(), ll))


def generate_token(username, group):
    return jwt.encode(
        {"username": str(username), "group": group}, config.secret, algorithm="HS256"
    )


def decode_token(token):
    try:
        obj = jwt.decode(token, config.secret, algorithms=["HS256"])
        user = obj["username"]
        group = obj["group"]
    except:
        user = -1
        group = -1
    return user, group


def filename_validation(fn):
    fn = str(fn)
    if fn.split(".")[-1] not in config.allow_file_type:
        return False
    else:
        return True


def make_unique(fn):
    ident = uuid4().__str__()[:8]
    return f"{ident}-{fn}"


def cjk_layout(text):
    return pangu.spacing_text(text)


def check_token(token):
    try:
        user, group = decode_token(token)
        if user == -1:
            return None
    except:
        return None
    return user, group


def links_to_imgs(links):
    from model import Image

    return [Image.query.filter_by(path=link).first().id for link in links]


def links_to_files(links):
    from model import File

    return [File.query.filter_by(location=link).first().id for link in links]


def utf8_str_to_normal(a):
    return json.loads(json.dumps({"a": a}))["a"]


def calculate_ranking():
    t = threading.Thread(target=_calculate_ranking)
    t.start()


def _calculate_ranking():
    from main import app

    with app.app_context():
        from model import Project, Score_weight, db

        year = Project.query.with_entities(Project.year).group_by(Project.year).all()
        for y in year:
            y = y[0]
            projects = to_obj_list(Project.query.filter_by(year=y).all())
            score_weight = to_obj_list(Score_weight.query.filter_by(year=y).all())
            score_weight = list(
                map(
                    lambda x: ({str(x["score_classification_id"]): x["weight"]}),
                    score_weight,
                )
            )
            score_weight = {k: v for d in score_weight for k, v in d.items()}
            score = list(
                map(
                    lambda x: 
                        sum(
                            [
                                (
                                    i["score"]
                                    * score_weight[str(i["score_classification_id"])]
                                )
                                for i in x["score"]
                            ]
                        ),
                    projects,
                )
            )
            score = list(map(lambda x: max(score)-x, score))
            rank = ss.rankdata(score, method="min")
            for i, r in enumerate(rank):
                Project.query.get(projects[i]["id"]).rank = r
                db.session.commit()
    print("Ranking complete")
