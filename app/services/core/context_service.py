from flask import request, g, abort

def resolve_tenant():
    cliente_id = request.headers.get("X-Client-ID")
    if not cliente_id:
        abort(400, "Missing X-Client-ID")
    g.cliente_id = cliente_id
    return cliente_id
