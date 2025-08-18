# app/views/responses.py
from flask import jsonify

def success(data=None, meta=None, status=200):
    body = {"ok": True}
    if data is not None:
        body["data"] = data
    if meta:
        body["meta"] = meta
    return jsonify(body), status

def created(data=None, meta=None):
    return success(data=data, meta=meta, status=201)

def no_content():
    # mantiene el envelope si prefieres, o 204 sin body
    return jsonify({"ok": True}), 204

def error(message, code="BAD_REQUEST", details=None, status=400):
    body = {"ok": False, "error": {"code": code, "message": message}}
    if details:
        body["error"]["details"] = details
    return jsonify(body), status
