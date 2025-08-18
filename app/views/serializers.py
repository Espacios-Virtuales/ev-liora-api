# app/views/serializers.py
def usuario_to_dict(u):
    return {
        "id": u.id,
        "nombre": u.nombre,
        "email": u.email,
        "cliente_id": u.cliente_id,
    }

def cliente_to_dict(c):
    return {
        "id": c.id,
        "slug": c.slug,
        "nombre": c.nombre,
        "estado": c.estado,
    }

def waba_account_to_dict(w):
    return {
        "id": w.id,
        "waba_id": w.waba_id,
        "phone_number_id": w.phone_number_id,
        "webhook_url": w.webhook_url,
        "estado": w.estado,
        "cliente_ids": [c.id for c in w.clientes] if hasattr(w, "clientes") else None
    }
