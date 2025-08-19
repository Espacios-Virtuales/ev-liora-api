# app/services/sheet_service.py
from __future__ import annotations
import os, re
from typing import List, Dict
import gspread
from oauth2client.service_account import ServiceAccountCredentials

GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def extract_sheet_id(url: str) -> str | None:
    m = re.search(r"/d/([a-zA-Z0-9-_]+)", url or "")
    return m.group(1) if m else None

def load_sheet_records(sheet_id: str, sheet_name: str = "respuestas") -> List[Dict]:
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, SCOPE)
        client = gspread.authorize(creds)
        ws = client.open_by_key(sheet_id).worksheet(sheet_name)
        return ws.get_all_records()
    except Exception as e:
        # En producción: log estructurado
        raise RuntimeError(f"Error al cargar Google Sheet '{sheet_id}/{sheet_name}': {e}")
