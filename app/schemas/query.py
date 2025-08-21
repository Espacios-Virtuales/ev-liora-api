from marshmallow import Schema, fields
class PageQuery(Schema):
    page = fields.Integer(load_default=1, metadata={"example": 1})
    page_size = fields.Integer(load_default=20, metadata={"example": 20})
