from typing import Dict, Any, List
from app.services.core.plugin_contracts import SkillPlugin

HELP_VIDA = (
    "🌱 *Vida Sana*\n"
    "• Escribe: *vida* → menú\n"
    "• *vida tips* → 3 hábitos rápidos\n"
    "• *vida bitácora* → registrar cómo te sientes hoy"
)

class VidaSanaPlugin:
    name = "vida_sana"
    version = "0.1.0"
    intents: List[str] = ["vida_sana.menu", "vida_sana.tips", "vida_sana.bitacora"]

    def can_handle(self, intent: str) -> bool:
        return intent in self.intents

    def handle(self, *, intent: str, message: str, ctx: Dict[str, Any], deps: Dict[str, Any]) -> Dict[str, Any]:
        if intent == "vida_sana.menu":
            body = HELP_VIDA
        elif intent == "vida_sana.tips":
            body = (
                "🌿 *3 hábitos simples*\n"
                "1) Un vaso de agua al despertar.\n"
                "2) 5 min de respiración (inhala 4, exhala 6).\n"
                "3) Caminar 10–15 min al sol."
            )
        else:  # vida_sana.bitacora
            mood = _extract_after(message, "vida bitácora") or _extract_after(message, "vida bitacora")
            if mood:
                # opcional: guardar en ctx['slots_json'] si tu core lo persiste
                slots = ctx.get("slots_json", {})
                slots["vida_mood"] = mood
                ctx["slots_json"] = slots
                body = f"📝 Registrado: *{mood}*. Gracias por compartir. (Puedes ver *vida* para más opciones)."
            else:
                body = "📝 Escribe: *vida bitácora <cómo te sientes hoy>*.\nEj: _vida bitácora agradecido y en calma_."
        return {"type": "text", "body": body}

def _extract_after(text: str, prefix: str) -> str:
    t = (text or "").strip().lower()
    p = prefix.strip().lower()
    if t.startswith(p):
        return text[len(prefix):].strip()
    return ""

def get_plugin():
    return VidaSanaPlugin()
