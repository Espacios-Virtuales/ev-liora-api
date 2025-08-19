# app/services/integrations/nlp_service.py
from __future__ import annotations
import os, re
from typing import Dict

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

_RULES = [
    (re.compile(r"\b(cat[aá]logo|productos?|ver\s+cat[aá]logo)\b", re.I), "catalogo.ver"),
    (re.compile(r"\b(vida\s+sana|salud|consej[oa]s?)\b", re.I), "vida_sana.tip"),
    (re.compile(r"\b(recicla[rg]|reciclaje|ecolog[íi]a|sustentable)\b", re.I), "reciclaje.info"),
    (re.compile(r"\b(ayuda|menu|inicio|opciones)\b", re.I), "menu"),
]

def _rule_based(text: str) -> Dict:
    for rx, intent in _RULES:
        if rx.search(text or ""):
            return {"intent": intent, "confidence": 0.8}
    return {"intent": "default", "confidence": 0.2}

def detect_intent(message: str) -> Dict:
    """
    Primero reglas rápidas; si hay OPENAI_API_KEY podrías expandir con LLM (pendiente).
    """
    return _rule_based(message or "")
