# app/services/skills/reciclaje_skill.py
from __future__ import annotations
from typing import Dict, Any

INFO = (
    "♻️ Reciclaje básico:\n"
    "- Papel/cartón: limpios y secos.\n"
    "- Plásticos: enjuagados; mira el número (1–7).\n"
    "- Vidrio: sin tapas.\n"
    "- Metales: latas limpias.\n"
    "Consulta puntos limpios locales en la web municipal."
)

def handle(user_context, message: str) -> Dict[str, Any]:
    return {"response": INFO}
