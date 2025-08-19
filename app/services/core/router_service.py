# app/services/core/router_service.py
from __future__ import annotations
from typing import Dict
from app.services.integrations import nlp_service
from app.services.skills import ecommerce_skill, vida_sana_skill, reciclaje_skill

def handle_incoming(user_context, message: str) -> Dict:
    det = nlp_service.detect_intent(message or "")
    intent = det.get("intent", "default")

    if intent.startswith("catalogo"):
        return ecommerce_skill.handle(user_context, message)
    if intent.startswith("vida_sana"):
        return vida_sana_skill.handle(user_context, message)
    if intent.startswith("reciclaje"):
        return reciclaje_skill.handle(user_context, message)

    # menú/fallback muy simple
    return {"response": "Puedo ayudarte con: catálogo, vida sana, reciclaje. ¿Cuál te interesa?"}
