# app/services/integrations/bitly_service.py
from __future__ import annotations
import os, json
from typing import Optional, Dict
import requests

BITLY_TOKEN = os.getenv("BITLY_TOKEN", "").strip()
BITLY_API = "https://api-ssl.bitly.com/v4/shorten"
DEFAULT_TIMEOUT = 8  # segundos

def append_utm(url: str, utm: Optional[Dict[str, str]] = None) -> str:
    if not utm:
        return url
    from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl
    parts = list(urlsplit(url))
    q = dict(parse_qsl(parts[3]))
    q.update({k: v for k, v in utm.items() if v})
    parts[3] = urlencode(q)
    return urlunsplit(parts)

def shorten(url: str, cliente_id: Optional[int] = None, utm: Optional[Dict[str, str]] = None) -> str:
    """
    Devuelve una versión acortada si hay BITLY_TOKEN; si no, retorna la URL (posiblemente con UTM).
    """
    long_url = append_utm(url, utm)
    if not BITLY_TOKEN:
        return long_url

    headers = {"Authorization": f"Bearer {BITLY_TOKEN}", "Content-Type": "application/json"}
    payload = {"long_url": long_url}
    # Puedes setear "domain": "bit.ly" u otro branded si lo tienes.

    try:
        resp = requests.post(BITLY_API, headers=headers, data=json.dumps(payload), timeout=DEFAULT_TIMEOUT)
        data = resp.json() if resp.content else {}
        if resp.status_code // 100 == 2 and "link" in data:
            return data["link"]
        # si Bitly falla, devolvemos la original para no romper flujo
        return long_url
    except requests.RequestException:
        return long_url
