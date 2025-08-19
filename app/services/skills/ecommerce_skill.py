# app/services/skills/ecommerce_skill.py
from __future__ import annotations
from typing import Dict, Any, List
from app.models import CatalogActive, CatalogSnapshot
from app.services.integrations.bitly_service import shorten

def _summarize_items(snapshot: CatalogSnapshot, limit: int = 3) -> List[Dict[str, Any]]:
    """
    Asume que el snapshot tiene filas en alguna tabla asociada o json.
    Aquí dejamos placeholder que devuelva títulos si existieran.
    """
    # TODO: implementar lectura real de ítems del snapshot
    return [{"titulo": f"Item {i+1}"} for i in range(limit)]

def handle(user_context, message: str) -> Dict[str, Any]:
    """
    user_context: instancia de UserContext (tiene cliente_id).
    """
    cid = getattr(user_context, "cliente_id", None)
    if not cid:
        return {"response": "No encuentro el cliente asociado. ¿Puedes intentar nuevamente?"}

    active = CatalogActive.query.filter_by(cliente_id=cid).first()
    if not active:
        return {"response": "Aún no tengo catálogo publicado para este cliente. ¿Te ayudo con otra cosa?"}

    # link “público” del catálogo: arma el que uses (sheet, web, etc.)
    base_url = f"https://app.ejemplo.com/catalogo/{cid}/v/{active.version}"
    link = shorten(base_url, cliente_id=cid, utm={"utm_source": "whatsapp", "utm_campaign": f"catalogo_v{active.version}"})

    items = _summarize_items(active)  # placeholder
    nombres = ", ".join([i["titulo"] for i in items])
    text = f"Catálogo v{active.version}: {nombres}.\nMíralo aquí: {link}"
    return {"response": text, "link": link, "items": items}
