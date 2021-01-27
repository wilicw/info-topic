from configparser import ConfigParser
import jwt

conf = ConfigParser()
conf.read("config.ini", encoding="utf-8")


class config:
    db_config = conf["db"]
    jwt_config = conf["jwt"]
    db_protocol = db_config["protocol"]
    db_user = db_config["user"]
    db_pass = db_config["pass"]
    db_host = db_config["host"]
    db_port = db_config["port"]
    db_name = db_config["db_name"]
    secret = jwt_config["secret"]


def remove_duplicates_preserving_order(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def to_simple_obj_list(ll):
    return list(map(lambda x: x.to_obj(), ll))


def to_detail_obj_list(ll):
    return list(map(lambda x: x.to_detail(), ll))


def generate_token(username):
    return jwt.encode({"username": str(username)}, config.secret, algorithm="HS256")


def decode_token(token):
    try:
        user = jwt.decode(token, config.secret, algorithms=["HS256"])["username"]
    except:
        user = -1
    return user