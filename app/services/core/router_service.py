# app/services/core/router_service.py
from __future__ import annotations
from typing import Dict, Any, List
import os

from .plugin_registry import PluginRegistry
from app.services.integrations import nlp_service  # solo para intent detect / fallback

# --- init de registro (una sola vez) ---
_registry = PluginRegistry()
_registry.load([
    "app.plugins.ecommerce.plugin",
    "app.plugins.vida_sana.plugin",
    "app.plugins.reciclaje.plugin",
])

HELP = "Puedo ayudarte con: *catalogo* (lista), *buscar <texto>*, *vida*, *reciclaje*."

def _infer_intent(text: str) -> str:
    t = (text or "").strip().lower()
    if t.startswith("catalogo") or t.startswith("catálogo"):
        return "catalogo.ver"
    if t.startswith("buscar "):
        return "catalogo.buscar"
    if t.startswith("vida"):
        return "vida_sana.menu"
    if t.startswith("reciclaje"):
        return "reciclaje.menu"
    return "no_match"

def handle_incoming(user_context: Dict[str, Any], message: str, deps: Dict[str, Any]) -> Dict[str, Any]:
    """
    user_context: {cliente_id, user_msisdn, slots_json? ...}
    deps: {'catalog_service','bitly_service','whatsapp_service','nlp_service','use_openai_fallback',...}
    """
    # 1) Intent: primero reglas rápidas, luego detector NLP si quieres enriquecer
    intent = _infer_intent(message)
    if intent == "no_match":
        det = nlp_service.detect_intent(message or "")
        intent = det.get("intent", "no_match")

    # 2) Buscar plugin que lo maneje
    candidates = _registry.find_for_intent(intent)
    if not candidates:
        # Fallback NLP a texto si está habilitado
        if deps.get("use_openai_fallback") and deps.get("nlp_service"):
            body = deps["nlp_service"].reply(message, user_context)
            return {"type": "text", "body": f"{body}\n\n{HELP}"}
        return {"type": "text", "body": f"No entendí.\n{HELP}"}

    # 3) Prioridad simple: primero registrado (puedes agregar ranking por manifiesto)
    plugin = candidates[0]
    return plugin.handle(intent=intent, message=message, ctx=user_context, deps=deps)
