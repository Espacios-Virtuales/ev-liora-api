# app/services/csv_service.py
from __future__ import annotations
import csv, io, re
from typing import List, Dict, Iterable, Optional, Union
from contextlib import contextmanager

try:
    import requests  # opcional, solo si leerás CSV por URL
except Exception:
    requests = None

def _is_url(src: str) -> bool:
    return isinstance(src, str) and src.startswith(("http://", "https://"))

def _drive_id_from_url(url: str) -> Optional[str]:
    # Ej: https://drive.google.com/file/d/FILE_ID/view?usp=sharing
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    return m.group(1) if m else None

def _drive_download_url(url: str) -> Optional[str]:
    file_id = _drive_id_from_url(url)
    if file_id:
        # Link directo de descarga
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return None

@contextmanager
def _open_text_source(source: Union[str, io.BytesIO, io.StringIO],
                      encoding: Optional[str] = None):
    """
    Abre el 'source' como stream de texto.
    - source: ruta local, URL http(s), o file-like.
    - encoding: si None intenta utf-8-sig -> utf-8 -> latin-1.
    """
    # 1) Si ya es StringIO, úsalo directo
    if isinstance(source, io.StringIO):
        yield source
        return

    # 2) Si es BytesIO, envolvemos con TextIOWrapper
    if isinstance(source, io.BytesIO):
        encs = [encoding] if encoding else ["utf-8-sig", "utf-8", "latin-1"]
        last_err = None
        for enc in encs:
            try:
                source.seek(0)
                wrapper = io.TextIOWrapper(source, encoding=enc, newline="")
                # Probar lectura mínima para validar
                _ = wrapper.read(0)
                wrapper.seek(0)
                yield wrapper
                return
            except Exception as e:
                last_err = e
        raise RuntimeError(f"No se pudo decodificar BytesIO: {last_err}")

    # 3) Si es string: ruta o URL
    if isinstance(source, str):
        if _is_url(source):
            if requests is None:
                raise RuntimeError("La dependencia 'requests' no está disponible para leer URLs.")
            # Ajuste para Google Drive
            dl_url = _drive_download_url(source) or source
            with requests.get(dl_url, stream=True, timeout=30) as r:
                r.raise_for_status()
                raw = io.BytesIO(r.content)
                # Reutilizamos la rama BytesIO
                with _open_text_source(raw, encoding=encoding) as txt_io:
                    yield txt_io
                    return
        else:
            # Ruta local
            encs = [encoding] if encoding else ["utf-8-sig", "utf-8", "latin-1"]
            last_err = None
            for enc in encs:
                try:
                    f = open(source, "r", encoding=enc, newline="")
                    try:
                        yield f
                    finally:
                        f.close()
                    return
                except Exception as e:
                    last_err = e
            raise RuntimeError(f"No se pudo abrir '{source}' con encodings {encs}: {last_err}")

    raise TypeError("Fuente de CSV no soportada. Usa ruta, URL, StringIO o BytesIO.")

def load_csv_records(
    source: Union[str, io.BytesIO, io.StringIO],
    sep: Optional[str] = None,
    has_header: bool = True,
    encoding: Optional[str] = None,
    limit: Optional[int] = None,
) -> List[Dict]:
    """
    Lee un CSV y devuelve lista de dicts.
    - source: path, URL, o file-like
    - sep: separador (si None, se intenta detectar)
    - has_header: True -> usa primera fila como cabecera
    - encoding: fuerza un encoding; si None, auto
    - limit: máximo de filas de datos (excluye cabecera)
    """
    with _open_text_source(source, encoding=encoding) as f:
        sample = f.read(4096)
        f.seek(0)

        delimiter = sep
        if delimiter is None:
            try:
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample, delimiters=[",", ";", "\t", "|"])
                delimiter = dialect.delimiter
            except Exception:
                delimiter = ","  # fallback estándar

        if has_header:
            reader = csv.DictReader(f, delimiter=delimiter)
            rows: List[Dict] = []
            for i, row in enumerate(reader):
                rows.append(row)
                if limit is not None and i + 1 >= limit:
                    break
            return rows
        else:
            reader = csv.reader(f, delimiter=delimiter)
            rows_raw = []
            header_gen = None
            for i, row in enumerate(reader):
                if header_gen is None:
                    header_gen = [f"col_{j+1}" for j in range(len(row))]
                rows_raw.append(dict(zip(header_gen, row)))
                if limit is not None and i + 1 >= limit:
                    break
            return rows_raw

def iter_csv_rows(
    source: Union[str, io.BytesIO, io.StringIO],
    sep: Optional[str] = None,
    has_header: bool = True,
    encoding: Optional[str] = None,
) -> Iterable[Dict]:
    """
    Generador de filas (dict) para procesamiento/streaming.
    """
    with _open_text_source(source, encoding=encoding) as f:
        sample = f.read(4096); f.seek(0)
        delimiter = sep
        if delimiter is None:
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"])
                delimiter = dialect.delimiter
            except Exception:
                delimiter = ","
        if has_header:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                yield row
        else:
            reader = csv.reader(f, delimiter=delimiter)
            header_gen = None
            for row in reader:
                if header_gen is None:
                    header_gen = [f"col_{j+1}" for j in range(len(row))]
                yield dict(zip(header_gen, row))
