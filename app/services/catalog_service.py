# app/services/catalog_service.py
from __future__ import annotations
from typing import Optional, Iterable, Dict, Any, Tuple
import hashlib, json
from datetime import datetime

from flask import g
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Cliente, CatalogSnapshot, CatalogActive

# -----------------------------------------------------------
# Helpers
# -----------------------------------------------------------

def _cid(explicit: Optional[int]) -> int:
    cid = explicit or getattr(g, "cliente_id", None)
    if cid is None:
        raise ValueError("cliente_id requerido (o llama a context_service.resolve_tenant() antes).")
    return cid

def _normalize_rows(rows: Iterable[Dict[str, Any]]) -> Tuple[list[Dict[str, Any]], int]:
    """
    Asegura lista de dicts; filtra None y normaliza claves.
    """
    if rows is None:
        return [], 0
    norm = []
    for r in rows:
        if not r:
            continue
        # normaliza claves a string y quita llaves vacías
        norm.append({str(k): v for k, v in r.items() if k is not None})
    return norm, len(norm)

def _checksum(obj: Any) -> str:
    """
    Checksum determinístico (sha256) del objeto JSON.
    """
    dumped = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(dumped.encode("utf-8")).hexdigest()

# -----------------------------------------------------------
# Validación de schema
# -----------------------------------------------------------

_REQUIRED_COLS = {"id", "titulo"}   # ajusta a tu realidad (sku, price, stock, etc.)
_OPTIONAL_COLS = {"descripcion", "precio", "stock", "url", "img"}

def validate_snapshot_rows(rows: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Valida columnas mínimas y retorna métricas simples.
    """
    problems = []
    count = 0
    for i, r in enumerate(rows):
        count += 1
        miss = _REQUIRED_COLS - set(r.keys())
        if miss:
            problems.append({"row": i, "missing": sorted(miss)})
    return {"rows_count": count, "problems": problems, "valid": len(problems) == 0}

# -----------------------------------------------------------
# Publicación de snapshot y activación
# -----------------------------------------------------------

def publish_snapshot(
    rows: Iterable[Dict[str, Any]],
    cliente_id: Optional[int] = None,
    source: str = "api",
    version: Optional[int] = None,
    extra_meta: Optional[Dict[str, Any]] = None,
) -> CatalogSnapshot:
    """
    Crea un CatalogSnapshot para el cliente. No lo activa (usa activate_snapshot()).
    `rows` debe ser iterable de dicts con columnas mínimas.
    """
    cid = _cid(cliente_id)
    cliente = Cliente.query.get(cid)
    if not cliente:
        raise ValueError("Cliente no encontrado.")

    rows_list, rows_count = _normalize_rows(rows)
    val = validate_snapshot_rows(rows_list)
    if not val["valid"]:
        raise ValueError(f"Snapshot inválido: faltan columnas en {len(val['problems'])} filas.")

    # Versión: si no viene, usamos (max(version)+1)
    if version is None:
        last = db.session.query(db.func.max(CatalogSnapshot.version)).filter_by(cliente_id=cid).scalar()
        version = int(last or 0) + 1

    payload = {
        "version": version,
        "rows_count": rows_count,
        "source": source,
        "meta": extra_meta or {},
        "rows": rows_list,  # si tu modelo NO guarda filas en JSON, omite esto
    }
    chksum = _checksum(payload)

    snap = CatalogSnapshot(
        cliente_id=cid,
        version=version,
        rows_count=rows_count,
        source=source,
        checksum=chksum,
        # Si tu modelo tiene campos JSON:
        # payload_json=payload,
        # o guarda sólo meta mínima si las filas van a otra tabla
    )

    try:
        db.session.add(snap)
        db.session.commit()
        return snap
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Conflicto al publicar snapshot: {e.orig}")

def activate_snapshot(
    version: Optional[int] = None,
    cliente_id: Optional[int] = None,
) -> CatalogActive:
    """
    Activa un snapshot del cliente (marca única en CatalogActive).
    Si no se pasa versión, toma la última (máxima).
    """
    cid = _cid(cliente_id)

    q = CatalogSnapshot.query.filter_by(cliente_id=cid)
    if version is None:
        snap = q.order_by(CatalogSnapshot.version.desc()).first()
    else:
        snap = q.filter_by(version=version).first()
    if not snap:
        raise ValueError("Snapshot no encontrado para activar.")

    active = CatalogActive.query.filter_by(cliente_id=cid).first()
    if not active:
        active = CatalogActive(
            cliente_id=cid,
            version=snap.version,
            rows_count=snap.rows_count,
            activated_at=datetime.utcnow(),
        )
        db.session.add(active)
    else:
        active.version = snap.version
        active.rows_count = snap.rows_count
        active.activated_at = datetime.utcnow()

    try:
        db.session.commit()
        return active
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Conflicto al activar snapshot: {e.orig}")

# -----------------------------------------------------------
# Lecturas
# -----------------------------------------------------------

def get_active(cliente_id: Optional[int] = None) -> Optional[CatalogActive]:
    cid = _cid(cliente_id)
    return CatalogActive.query.filter_by(cliente_id=cid).first()

def list_snapshots(cliente_id: Optional[int] = None, limit: int = 50) -> list[CatalogSnapshot]:
    cid = _cid(cliente_id)
    return (
        CatalogSnapshot.query
        .filter_by(cliente_id=cid)
        .order_by(CatalogSnapshot.version.desc())
        .limit(limit)
        .all()
    )
