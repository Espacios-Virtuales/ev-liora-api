from flask import g, request, abort
from app.models import Cliente, ClientContext

def resolve_tenant():
    raw = request.headers.get("X-Client-ID")
    if not raw:
        abort(400, "Missing X-Client-ID")
    try:
        cid = int(raw)
    except ValueError:
        abort(400, "X-Client-ID must be integer")

    cliente = Cliente.query.get(cid)
    if not cliente:
        abort(404, "Cliente not found")

    # cache en g
    g.cliente_id = cid
    g.cliente = cliente
    g.client_context = cliente.context  # puede ser None si aún no existe (lo crearemos al migrar/seeding)
    return cid
