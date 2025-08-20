# app/schemas/common.py
from marshmallow import Schema, fields

class ErrorSchema(Schema):
    code = fields.Integer(required=True, description="HTTP status code (ej: 404)")
    status = fields.String(required=True, description="Nombre del error (ej: Not Found)")
    message = fields.String(required=True, description="Mensaje legible para humanos")
    errors = fields.Dict(keys=fields.String(), values=fields.Raw(), description="Detalle por campo u otros datos")

class PaginationMetadata(Schema):
    total = fields.Integer(required=True, description="Total de elementos")
    total_pages = fields.Integer(required=True, description="Cantidad total de páginas")
    first_page = fields.Integer(required=True, description="Número de página inicial (normalmente 1)")
    last_page = fields.Integer(required=True, description="Número de página final")
    page = fields.Integer(required=True, description="Página actual")
    previous_page = fields.Integer(allow_none=True, description="Página anterior o null")
    next_page = fields.Integer(allow_none=True, description="Página siguiente o null")
