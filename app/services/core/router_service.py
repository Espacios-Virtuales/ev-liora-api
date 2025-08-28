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

def handle_incoming(*args, **kwargs) -> Dict[str, Any]:
    """
    Soporta dos firmas:
      1) handle_incoming(evento, estado, deps)            # tests / controller
      2) handle_incoming(user_context, message, deps)     # firma nueva
    """
    if "evento" in kwargs or "estado" in kwargs:
        evento = kwargs.get("evento") or (args[0] if len(args) > 0 else {}) or {}
        estado = kwargs.get("estado") or (args[1] if len(args) > 1 else {}) or {}
        deps   = kwargs.get("deps")   or (args[2] if len(args) > 2 else {}) or {}
        message = (evento or {}).get("text") or kwargs.get("message") or ""
        user_context = estado
    else:
        # firma nueva
        user_context = args[0] if len(args) > 0 else kwargs.get("user_context") or {}
        message      = args[1] if len(args) > 1 else kwargs.get("message") or ""
        deps         = args[2] if len(args) > 2 else kwargs.get("deps") or {}

    # ... a partir de aquí queda tu lógica actual:
    intent = _infer_intent(message)
    if intent == "no_match":
        try:
            det = nlp_service.detect_intent(message or "")
            intent = det.get("intent", "no_match")
        except Exception:
            pass

    candidates = _registry.find_for_intent(intent)
    if not candidates:
        if deps.get("use_openai_fallback") and deps.get("nlp_service"):
            body = deps["nlp_service"].reply(message, user_context)
            return {"type": "text", "body": f"{body}\n\n{HELP}"}
        return {"type": "text", "body": f"No entendí.\n{HELP}"}

    plugin = candidates[0]
    return plugin.handle(intent=intent, message=message, ctx=user_context, deps=deps)

