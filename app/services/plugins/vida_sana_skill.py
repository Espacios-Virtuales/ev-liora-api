# app/services/skills/vida_sana_skill.py
from __future__ import annotations
from typing import Dict, Any

TIPS = [
    "Hidrátate: 6–8 vasos de agua al día.",
    "Camina 20–30 minutos. ¡Cuenta pasos!",
    "Incluye verduras y frutas en tus comidas.",
    "Duerme 7–8 horas para recuperar energía.",
]

def handle(user_context, message: str) -> Dict[str, Any]:
    # Ejemplo: podríamos rotar tips con un contador simple en user_context.slots_json
    slots = user_context.slots_json or {}
    idx = int(slots.get("vida_tip_idx", 0)) % len(TIPS)
    tip = TIPS[idx]
    slots["vida_tip_idx"] = idx + 1
    user_context.slots_json = slots
    # persistencia la haría el caller (router) si corresponde
    return {"response": f"Consejo de vida sana:\n• {tip}"}
