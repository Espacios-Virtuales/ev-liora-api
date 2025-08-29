# app/services/drive_csv_service.py (refactor compacto y seguro)
from __future__ import annotations
import os, io, csv, re
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials

GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "data-liora.json")
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# ------------- Helpers -------------
def _drive():
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
    # cache_discovery=False evita warnings de pickling en algunos entornos
    return build("drive", "v3", credentials=creds, cache_discovery=False)

def _q(value: str) -> str:
    """
    Escapa un valor para usar en queries de Google Drive (entre comillas simples).
    Reglas: escapar backslash y comilla simple:  \  -> \\   |   ' -> \'
    """
    s = (value or "")
    s = s.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{s}'"

def _download_bytes(file_id: str) -> bytes:
    svc = _drive()
    req = svc.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    dl = MediaIoBaseDownload(buf, req)
    done = False
    while not done:
        _, done = dl.next_chunk()
    buf.seek(0)
    return buf.read()

def _parse_csv(data: bytes, sep: str | None = None, has_header: bool = True) -> List[Dict[str, str]]:
    # Detección de encoding común
    text: Optional[str] = None
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            text = data.decode(enc)
            break
        except Exception:
            pass
    if text is None:
        raise RuntimeError("No se pudo decodificar el CSV (utf-8/latin-1).")

    # Detección de separador si no viene dado
    if sep is None:
        try:
            sample = text[:4096]
            dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"])
            sep = dialect.delimiter
        except Exception:
            sep = ","

    f = io.StringIO(text)
    if has_header:
        return list(csv.DictReader(f, delimiter=sep))

    rows = list(csv.reader(f, delimiter=sep))
    if not rows:
        return []
    headers = [f"col_{i+1}" for i in range(len(rows[0]))]
    return [dict(zip(headers, r)) for r in rows]

def file_id_from_drive_url(url: str) -> Optional[str]:
    # Soporta URLs tipo https://drive.google.com/file/d/<id>/view
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url or "")
    return m.group(1) if m else None

# ------------- API de alto nivel -------------
def csv_from_folder_and_name(folder_name: str, filename: str, sep: str | None = None) -> List[Dict[str, str]]:
    """
    Busca una carpeta por nombre exacto (primer match no borrado),
    luego un archivo dentro de esa carpeta por nombre exacto, valida mimetype y retorna el CSV parseado.
    """
    svc = _drive()

    # 1) ID de carpeta
    q_folder = f"mimeType='application/vnd.google-apps.folder' and trashed=false and name={_q(folder_name)}"
    folders = svc.files().list(q=q_folder, fields="files(id,name)", pageSize=50).execute().get("files", [])
    if not folders:
        raise FileNotFoundError(f"Carpeta '{folder_name}' no encontrada.")
    folder_id = folders[0]["id"]

    # 2) Archivo dentro de la carpeta (nombre exacto, no borrado)
    q_file = f"{_q(folder_id)} in parents and trashed=false and name={_q(filename)}"
    files = svc.files().list(q=q_file, fields="files(id,name,mimeType,size)", pageSize=50).execute().get("files", [])
    if not files:
        raise FileNotFoundError(f"Archivo '{filename}' no encontrado en '{folder_name}'.")

    file = files[0]
    mime = file.get("mimeType", "")

    # 3) Validación mínima de tipo CSV (Drive suele marcar 'text/csv' o 'application/vnd.ms-excel' para CSV)
    allowed = {"text/csv", "application/vnd.ms-excel", "application/octet-stream", "text/plain"}
    if mime not in allowed:
        raise TypeError(f"No es un CSV compatible (mimeType={mime}).")

    # 4) Descargar y parsear
    raw = _download_bytes(file["id"])
    return _parse_csv(raw, sep=sep, has_header=True)

def csv_from_file_id_or_url(file_id_or_url: str, sep: str | None = None) -> List[Dict[str, str]]:
    """
    Acepta un fileId puro o una URL de Drive con '/d/<id>/'.
    """
    fid = file_id_from_drive_url(file_id_or_url) or file_id_or_url
    raw = _download_bytes(fid)
    return _parse_csv(raw, sep=sep, has_header=True)
