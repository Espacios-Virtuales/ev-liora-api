from typing import Dict, Any, List
from app.services.core.plugin_contracts import SkillPlugin

class EcommercePlugin:
    name = "ecommerce"
    version = "0.1.0"
    intents: List[str] = ["catalogo.ver", "catalogo.buscar"]

    def can_handle(self, intent: str) -> bool:
        return intent in self.intents

    def handle(self, *, intent: str, message: str, ctx: Dict[str, Any], deps: Dict[str, Any]) -> Dict[str, Any]:
        catalog = deps["catalog_service"]
        bitly = deps["bitly_service"]
        cliente_id = ctx["cliente_id"]

        if intent == "catalogo.buscar":
            q = message.split(" ", 1)[-1].strip() if " " in message else ""
            items = catalog.search_active(cliente_id=cliente_id, q=q, limit=5)
            title = f"🔎 Resultados para “{q}”" if q else "🔎 Resultados"
        else:
            items = catalog.get_active_summary(cliente_id=cliente_id, limit=5)
            title = "🛍️ Catálogo"

        if not items:
            return {"type": "text", "body": "No encontré productos activos."}

        lines = []
        for it in items:
            url = it.get("url")
            short = bitly.shorten(url, {"utm_source":"wa","utm_medium":"bot","utm_campaign":"catalogo","utm_content":cliente_id}) if url else url
            price = f" — ${it['price']:,}".replace(",", ".") if it.get("price") else ""
            lines.append(f"• {it.get('name','Producto')}{price} → {short or url or ''}")
        body = f"{title}:\n" + "\n".join(lines)
        return {"type": "text", "body": body}

def get_plugin():
    return EcommercePlugin()
