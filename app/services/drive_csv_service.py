# app/services/drive_csv_service.py
from __future__ import annotations
import io, csv, os
from typing import List, Dict, Optional, Tuple
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials

# ENV esperados (puedes ajustarlos a tu gusto)
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "data-liora.json")
# Si ya sabes el ID de la carpeta, ponlo; si no, buscaremos por nombre.
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")  # opcional

# Scopes mínimos para leer Drive
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def _build_drive():
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
    return build("drive", "v3", credentials=creds, cache_discovery=False)

def _find_folder_by_name(drive, folder_name: str) -> Optional[str]:
    """Devuelve folderId del primer match por nombre (no busca recursivo)."""
    q = (
        "mimeType='application/vnd.google-apps.folder' and "
        f"name = '{folder_name.replace(\"'\", \"\\'\")}' and trashed = false"
    )
    res = drive.files().list(q=q, fields="files(id, name)").execute()
    files = res.get("files", [])
    return files[0]["id"] if files else None

def _find_file_in_folder(drive, folder_id: str, filename: str) -> Optional[Dict]:
    """Busca un archivo por nombre exacto dentro de una carpeta dada."""
    q = (
        f"'{folder_id}' in parents and "
        "trashed = false and "
        f"name = '{filename.replace(\"'\", \"\\'\")}'"
    )
    res = drive.files().list(
        q=q,
        fields="files(id, name, mimeType, modifiedTime, size)",
        orderBy="modifiedTime desc"
    ).execute()
    files = res.get("files", [])
    return files[0] if files else None

def _find_latest_csv_in_folder(drive, folder_id: str) -> Optional[Dict]:
    """Devuelve el CSV más reciente por modifiedTime dentro de la carpeta."""
    q = (
        f"'{folder_id}' in parents and trashed = false and "
        "(mimeType='text/csv' or mimeType='application/vnd.ms-excel')"
    )
    res = drive.files().list(
        q=q,
        fields="files(id, name, mimeType, modifiedTime, size)",
        orderBy="modifiedTime desc",
        pageSize=1
    ).execute()
    files = res.get("files", [])
    return files[0] if files else None

def _download_file_bytes(drive, file_id: str) -> bytes:
    request = drive.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    buf.seek(0)
    return buf.read()

def _parse_csv_bytes(data: bytes, sep: str | None = None, has_header: bool = True) -> List[Dict]:
    # Intento de encodings comunes
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            text = data.decode(enc)
            break
        except Exception:
            text = None
    if text is None:
        raise RuntimeError("No se pudo decodificar el CSV (utf-8/latin-1).")

    # Detectar separador si no se indica
    if sep is None:
        sample = text[:4096]
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"])
            sep = dialect.delimiter
        except Exception:
            sep = ","

    f = io.StringIO(text)
    if has_header:
        reader = csv.DictReader(f, delimiter=sep)
        return list(reader)
    else:
        reader = csv.reader(f, delimiter=sep)
        rows = list(reader)
        if not rows:
            return []
        headers = [f"col_{i+1}" for i in range(len(rows[0]))]
        return [dict(zip(headers, r)) for r in rows]

def load_csv_from_drive_by_name(
    folder_name: Optional[str],
    file_name: str,
    sep: str | None = None,
    has_header: bool = True
) -> List[Dict]:
    """
    Lee un CSV en Google Drive por 'nombre de archivo' dentro de 'nombre de carpeta'.
    Si GOOGLE_DRIVE_FOLDER_ID está seteado, usa ese folder directamente.
    """
    drive = _build_drive()
    folder_id = GOOGLE_DRIVE_FOLDER_ID
    if not folder_id:
        if not folder_name:
            raise ValueError("Falta folder_name y no hay GOOGLE_DRIVE_FOLDER_ID en el entorno.")
        folder_id = _find_folder_by_name(drive, folder_name)
        if not folder_id:
            raise FileNotFoundError(f"No se encontró la carpeta '{folder_name}' en Drive.")

    file_meta = _find_file_in_folder(drive, folder_id, file_name)
    if not file_meta:
        raise FileNotFoundError(f"No se encontró el archivo '{file_name}' en la carpeta.")

    if file_meta["mimeType"] not in ("text/csv", "application/vnd.ms-excel"):
        # Si accidentalmente subieron un Google Sheet con ese nombre, podrías exportarlo.
        # Pero el requerimiento dice CSV; aquí validamos y fallamos para ser explícitos.
        raise TypeError(f"El archivo encontrado no es CSV. mimeType={file_meta['mimeType']}")

    data = _download_file_bytes(drive, file_meta["id"])
    return _parse_csv_bytes(data, sep=sep, has_header=has_header)

def load_latest_csv_from_drive(
    folder_name: Optional[str],
    sep: str | None = None,
    has_header: bool = True
) -> Tuple[str, List[Dict]]:
    """
    Devuelve (file_name, rows) del CSV más reciente en la carpeta.
    Útil cuando el cliente sube periódicamente 'export_YYYYMMDD.csv'.
    """
    drive = _build_drive()
    folder_id = GOOGLE_DRIVE_FOLDER_ID
    if not folder_id:
        if not folder_name:
            raise ValueError("Falta folder_name y no hay GOOGLE_DRIVE_FOLDER_ID en el entorno.")
        folder_id = _find_folder_by_name(drive, folder_name)
        if not folder_id:
            raise FileNotFoundError(f"No se encontró la carpeta '{folder_name}' en Drive.")

    file_meta = _find_latest_csv_in_folder(drive, folder_id)
    if not file_meta:
        raise FileNotFoundError("No hay CSVs en la carpeta designada.")

    data = _download_file_bytes(drive, file_meta["id"])
    rows = _parse_csv_bytes(data, sep=sep, has_header=has_header)
    return file_meta["name"], rows
