# app/controllers/meta_webhook_controller.py
from flask import Blueprint, request, Response, g
import os, json

from app.views.responses import success, error
from app.services.integrations.whatsapp_service import verify_challenge, verify_signature, send_text
from app.services.core import router_service
from app.services.catalog_service import get_active_summary, search_active  # si importas funciones sueltas
from app.services.integrations.bitly_service import BitlyService
from app.services.integrations.nlp_service import NlpService

bp = Blueprint("meta_webhook", __name__)
META_VERIFY_TOKEN = os.getenv("WABA_VERIFY_TOKEN", "changeme")
META_APP_SECRET   = os.getenv("WABA_APP_SECRET", "changeme")
USE_OPENAI        = os.getenv("USE_OPENAI_FALLBACK","false").lower() == "true"

def verify():
    challenge = verify_challenge(request.args, META_VERIFY_TOKEN)
    if challenge is None:
        return error("verify_token inválido", code="FORBIDDEN", status=403)
    return Response(challenge, status=200, mimetype="text/plain")

def events():
    raw = request.get_data()
    sig = request.headers.get("X-Hub-Signature-256", "")
    if not verify_signature(META_APP_SECRET, raw, sig):
        return error("Firma inválida", code="FORBIDDEN", status=403)

    payload = request.get_json(force=True, silent=True) or {}
    # WhatsApp Cloud (forma típica):
    # entry[0].changes[0].value.messages[0]
    try:
        value = payload["entry"][0]["changes"][0]["value"]
        messages = value.get("messages", [])
        contacts = value.get("contacts", [])
        if not messages:
            return success({"received": True, "note": "no messages"})
        msg = messages[0]
        user_msisdn = msg.get("from")
        text = (msg.get("text",{}) or {}).get("body","").strip()
    except Exception:
        return error("Formato de payload no reconocido", code="BAD_REQUEST", status=400)

    # Resolver tenant (simplificado): si usas mapping por número destino
    destino = value.get("metadata",{}).get("phone_number_id")
    # TODO: context_service.resolve_tenant() por número destino → g.cliente_id
    # Por ahora asumimos que g.cliente_id ya fue fijado por middleware
    if not getattr(g, "cliente_id", None):
        # fallback de demo: cliente único
        g.cliente_id = os.getenv("DEMO_CLIENTE_ID")

    user_ctx = {"cliente_id": g.cliente_id, "user_msisdn": user_msisdn}


    deps = {
        "catalog_service": __import__("app.services.catalog_service", fromlist=["dummy"]),  # o instancia real
        "bitly_service": BitlyService(token=os.getenv("BITLY_TOKEN")),
        "nlp_service": NlpService(api_key=os.getenv("OPENAI_API_KEY")) if USE_OPENAI else None,
        "use_openai_fallback": USE_OPENAI,
    }

    resp = router_service.handle_incoming(user_context=user_ctx, message=text, deps=deps)

    if resp.get("type") == "text":
        # necesitas el phone_number_id/token de WABA (búscalo por cliente)
        send_text(
            to=user_msisdn,
            body=resp["body"],
            waba_account={
                "phone_number_id": destino,
                "access_token": os.getenv("META_ACCESS_TOKEN")
            }
        )
    return success({"ok": True})
