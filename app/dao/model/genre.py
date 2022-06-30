from marshmallow import Schema, fields
from app.setup_db import db


# SQLAclhemy модель
class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


# Marshmallow схема
class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

