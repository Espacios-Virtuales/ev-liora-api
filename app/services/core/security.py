from functools import wraps
from flask import g, abort

def requires_tenant(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not getattr(g, "cliente_id", None):
            abort(400, "Tenant not resolved")
        return f(*args, **kwargs)
    return wrapper
