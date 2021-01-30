from configparser import ConfigParser
from uuid import uuid4
import jwt, pangu

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


def remove_duplicates_preserving_order(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def to_simple_obj_list(ll):
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