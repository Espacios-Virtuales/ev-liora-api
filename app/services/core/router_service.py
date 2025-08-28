# app/services/core/router_service.py
from __future__ import annotations
from typing import Dict, Any
from .plugin_registry import PluginRegistry
from app.services.integrations import nlp_service

_REGISTRY: PluginRegistry | None = None

def _ensure_registry() -> PluginRegistry:
    global _REGISTRY
    if _REGISTRY is not None:
        return _REGISTRY
    reg = PluginRegistry()
    try:
        reg.load([
            "app.plugins.ecommerce.plugin",
            "app.plugins.vida_sana.plugin",
            "app.plugins.reciclaje.plugin",
        ])
    except Exception:
        # no abortes el import — permite que el API se registre
        pass
    _REGISTRY = reg
    return reg

HELP = "Puedo ayudarte con: *catalogo* (lista), *buscar <texto>*, *vida*, *reciclaje*."

def _infer_intent(text: str) -> str:
    t = (text or "").strip().lower()
    if t.startswith(("catalogo", "catálogo")): return "catalogo.ver"
    if t.startswith("buscar "):                return "catalogo.buscar"
    if t.startswith("vida"):                   return "vida_sana.menu"
    if t.startswith("reciclaje"):              return "reciclaje.menu"
    return "no_match"

def handle_incoming(user_context: Dict[str, Any], message: str, deps: Dict[str, Any]) -> Dict[str, Any]:
    registry = _ensure_registry()

    intent = _infer_intent(message)
    if intent == "no_match":
        det = nlp_service.detect_intent(message or "")
        intent = det.get("intent", "no_match")

    candidates = registry.find_for_intent(intent)
    if not candidates:
        if deps.get("use_openai_fallback") and deps.get("nlp_service"):
            body = deps["nlp_service"].reply(message, user_context)
            return {"type": "text", "body": f"{body}\n\n{HELP}"}
        return {"type": "text", "body": f"No entendí.\n{HELP}"}

    plugin = candidates[0]
    return plugin.handle(intent=intent, message=message, ctx=user_context, deps=deps)
