from marshmallow import Schema, fields

class LevelSpec(Schema):
    levelspec = fields.String(required=True)
