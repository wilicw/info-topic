from flask_marshmallow import Marshmallow

ma = Marshmallow()


class AuthSchema(ma.Schema):
    username = ma.Str(required=True)
    password = ma.Str(required=True)
