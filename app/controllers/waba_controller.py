# app/controllers/waba_controller.py
from __future__ import annotations
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from app.views.responses import success, created, error
from app.views.serializers import waba_account_to_dict
from app.services.integrations.whatsapp_service import (
    create_waba_account, update_waba_account, get_waba_account,
    list_waba_accounts, delete_waba_account,
    attach_waba_to_cliente, detach_waba_from_cliente,
)

bp = Blueprint("waba", __name__)

def post_waba():
    data = request.get_json(silent=True) or {}
    try:
        w = create_waba_account(data)
        return created(waba_account_to_dict(w))
    except ValueError as ve:
        return error(str(ve), code="VALIDATION_ERROR", status=400)
    except IntegrityError as ie:
        return error("Conflicto de integridad", code="CONFLICT", details=str(ie.orig), status=409)
    except Exception as e:
        return error("Error no controlado al crear WABA", code="INTERNAL_ERROR", details=str(e), status=500)

def get_waba_list():
    ws = list_waba_accounts()
    return success([waba_account_to_dict(w) for w in ws])

def get_waba_detail(waba_id: int):
    w = get_waba_account(waba_id)
    if not w:
        return error("WABA no encontrada", code="NOT_FOUND", status=404)
    return success(waba_account_to_dict(w))

def patch_waba(waba_id: int):
    data = request.get_json(silent=True) or {}
    w = update_waba_account(waba_id, data)
    if not w:
        return error("WABA no encontrada", code="NOT_FOUND", status=404)
    return success(waba_account_to_dict(w))

def delete_waba(waba_id: int):
    try:
        ok = delete_waba_account(waba_id)
        if not ok:
            return error("WABA no encontrada", code="NOT_FOUND", status=404)
        return success({"deleted": True})
    except ValueError as ve:
        return error(str(ve), code="CONFLICT", status=409)

def attach_cliente_waba(cliente_id: int):
    data = request.get_json(silent=True) or {}
    if not data.get("waba_account_id"):
        return error("Datos inválidos", code="VALIDATION_ERROR", details={"missing": ["waba_account_id"]}, status=422)
    try:
        c = attach_waba_to_cliente(cliente_id=cliente_id, waba_account_id=data["waba_account_id"])
        return success({"cliente_id": c.id, "waba_account_id": c.waba_account_id})
    except ValueError as ve:
        return error(str(ve), code="VALIDATION_ERROR", status=400)

def detach_cliente_waba(cliente_id: int):
    try:
        c = detach_waba_from_cliente(cliente_id=cliente_id)
        return success({"cliente_id": c.id, "waba_account_id": c.waba_account_id})
    except ValueError as ve:
        return error(str(ve), code="VALIDATION_ERROR", status=400)
