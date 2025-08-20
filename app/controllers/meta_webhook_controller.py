# app/controllers/meta_webhook_controller.py
from __future__ import annotations
from flask import Blueprint, request, Response
import os

from app.views.responses import success, error
from app.services.integrations.whatsapp_service import verify_challenge, verify_signature

bp = Blueprint("meta_webhook", __name__)
META_VERIFY_TOKEN = os.getenv("WABA_VERIFY_TOKEN", "changeme")
META_APP_SECRET   = os.getenv("WABA_APP_SECRET", "changeme")

def verify():
    # GET /webhook/meta
    challenge = verify_challenge(request.args, META_VERIFY_TOKEN)
    if challenge is None:
        return error("verify_token inválido", code="FORBIDDEN", status=403)
    # Respuesta en texto plano como exige Meta
    return Response(challenge, status=200, mimetype="text/plain")

def events():
    # POST /webhook/meta
    raw = request.get_data()
    sig = request.headers.get("X-Hub-Signature-256", "")
    if not verify_signature(META_APP_SECRET, raw, sig):
        return error("Firma inválida", code="FORBIDDEN", status=403)

    # TODO: parsear y despachar al router_service (intents/skills)
    # payload = request.get_json(silent=True) or {}
    # ... manejar eventos ...
    return success({"received": True})
