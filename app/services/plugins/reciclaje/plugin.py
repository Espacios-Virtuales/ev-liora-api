from typing import Dict, Any, List
from app.services.core.plugin_contracts import SkillPlugin

HELP_REC = (
    "♻️ *Reciclaje*\n"
    "• Escribe: *reciclaje* → menú\n"
    "• *reciclaje puntos* → cómo ubicar puntos limpios\n"
    "• *reciclaje separar* → tips de separación"
)

class ReciclajePlugin:
    name = "reciclaje"
    version = "0.1.0"
    intents: List[str] = ["reciclaje.menu", "reciclaje.puntos", "reciclaje.separar"]

    def can_handle(self, intent: str) -> bool:
        return intent in self.intents

    def handle(self, *, intent: str, message: str, ctx: Dict[str, Any], deps: Dict[str, Any]) -> Dict[str, Any]:
        if intent == "reciclaje.menu":
            body = HELP_REC
        elif intent == "reciclaje.puntos":
            body = (
                "📍 Para ubicar puntos limpios cercanos:\n"
                "1) Busca en Google Maps: *punto limpio + tu comuna*.\n"
                "2) Revisa municipalidad/ONG locales.\n"
                "3) Pregunta por *reciclaje separar* para empezar desde casa."
            )
        else:  # reciclaje.separar
            body = (
                "🧩 *Separación básica en casa*\n"
                "• Papel/Cartón: limpio y seco.\n"
                "• Plásticos PET/PEAD: enjuagados (sin restos).\n"
                "• Vidrio: botellas y frascos limpios, sin tapas.\n"
                "• Latas: enjuagadas y aplastadas.\n"
                "• Orgánicos: composteras o tachos diferenciados."
            )
        return {"type": "text", "body": body}

def get_plugin():
    return ReciclajePlugin()
