# app/services/integrations/whatsapp_service.py
from __future__ import annotations
from typing import Optional, Dict, Any
import hmac, hashlib, json
import requests

from app.extensions import db
from app.models import WabaAccount, Cliente

# ---------------------------
# CRUD de WabaAccount (scope global)
# ---------------------------

REQUIRED_CREATE = ["waba_id", "phone_number_id", "numero_e164", "access_token", "verify_token", "app_secret"]

def create_waba_account(data: Dict[str, Any]) -> WabaAccount:
    missing = [k for k in REQUIRED_CREATE if not data.get(k)]
    if missing:
        raise ValueError(f"Faltan campos obligatorios: {', '.join(missing)}")

    # Unicidad básica por IDs de Meta / número e164
    if WabaAccount.query.filter_by(waba_id=data["waba_id"]).first():
        raise ValueError("Ya existe una WabaAccount con ese waba_id.")
    if WabaAccount.query.filter_by(phone_number_id=data["phone_number_id"]).first():
        raise ValueError("Ya existe una WabaAccount con ese phone_number_id.")
    if WabaAccount.query.filter_by(numero_e164=data["numero_e164"]).first():
        raise ValueError("Ya existe una WabaAccount con ese número (E.164).")

    w = WabaAccount(
        name=data.get("name"),
        waba_id=data["waba_id"],
        phone_number_id=data["phone_number_id"],
        numero_e164=data["numero_e164"],
        access_token=data["access_token"],   # TIP: cifrar con Fernet/KMS (futuro)
        verify_token=data["verify_token"],
        app_secret=data["app_secret"],
        estado=data.get("estado", "activo"),
    )
    db.session.add(w)
    db.session.commit()
    return w


def update_waba_account(waba_id: int, patch: Dict[str, Any]) -> Optional[WabaAccount]:
    w = WabaAccount.query.get(waba_id)
    if not w:
        return None

    # Campos permitidos
    for k in ["name", "numero_e164", "access_token", "verify_token", "app_secret", "estado", "webhook_url"]:
        if k in patch and patch[k] is not None:
            setattr(w, k, patch[k])

    db.session.commit()
    return w


def get_waba_account(waba_id: int) -> Optional[WabaAccount]:
    return WabaAccount.query.get(waba_id)


def list_waba_accounts() -> list[WabaAccount]:
    return WabaAccount.query.order_by(WabaAccount.id.desc()).all()


def delete_waba_account(waba_id: int) -> bool:
    """
    Elimina solo si NO está asignada a clientes.
    """
    w = WabaAccount.query.get(waba_id)
    if not w:
        return False
    if w.clientes and len(w.clientes) > 0:
        raise ValueError("No se puede eliminar: la WabaAccount está asignada a uno o más clientes.")
    db.session.delete(w)
    db.session.commit()
    return True


# ---------------------------
# Vinculación Cliente ↔ WABA (tenant)
# ---------------------------

def attach_waba_to_cliente(cliente_id: int, waba_account_id: int) -> Cliente:
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        raise ValueError("Cliente no encontrado.")
    w = WabaAccount.query.get(waba_account_id)
    if not w:
        raise ValueError("WabaAccount no encontrada.")

    cliente.waba_account_id = w.id
    db.session.commit()
    return cliente


def detach_waba_from_cliente(cliente_id: int) -> Cliente:
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        raise ValueError("Cliente no encontrado.")
    cliente.waba_account_id = None
    db.session.commit()
    return cliente


# ---------------------------
# Webhook helpers (Meta)
# ---------------------------

def verify_challenge(params: Dict[str, Any], expected_verify_token: str) -> Optional[str]:
    """
    Para GET /webhook/meta:
    Devuelve hub.challenge si verify_token coincide; None si no.
    """
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    if mode == "subscribe" and token == expected_verify_token:
        return challenge
    return None


def verify_signature(app_secret: str, payload_bytes: bytes, x_hub_sig_256: str) -> bool:
    """
    Valida X-Hub-Signature-256 con app_secret (HMAC SHA-256).
    """
    if not x_hub_sig_256:
        return False
    try:
        algo, given = x_hub_sig_256.split("=")
    except ValueError:
        return False
    if algo.lower() != "sha256":
        return False
    digest = hmac.new(app_secret.encode("utf-8"), msg=payload_bytes, digestmod=hashlib.sha256).hexdigest()
    # Comparación segura
    return hmac.compare_digest(given, digest)


# ---------------------------
# Envío de mensajes (Meta)
# ---------------------------

META_GRAPH_BASE = "https://graph.facebook.com/v19.0"

def _headers(access_token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

def send_text(waba: WabaAccount, to_e164: str, body: str) -> Dict[str, Any]:
    """
    Envía un mensaje de texto simple usando la cuenta WABA provista.
    """
    url = f"{META_GRAPH_BASE}/{waba.phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to_e164,
        "type": "text",
        "text": {"preview_url": False, "body": body},
    }

    resp = requests.post(url, headers=_headers(waba.access_token), data=json.dumps(payload), timeout=15)
    try:
        data = resp.json()
    except Exception:
        data = {"raw": resp.text}

    if resp.status_code >= 400:
        # aquí podrías mapear errores y lanzar excepción si prefieres
        return {"ok": False, "status": resp.status_code, "data": data}

    return {"ok": True, "status": resp.status_code, "data": data}
