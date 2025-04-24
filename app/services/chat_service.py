import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.models import EntradaChat
from app.models import Documento

def extraer_sheet_id(enlace):
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", enlace)
    return match.group(1) if match else None

def cargar_entradas_desde_sheet(documento_id, nombre_hoja="respuestas"):
    documento = Documento.query.get(documento_id)
    if not documento:
        raise ValueError("Documento no encontrado.")
    sheet_id = extraer_sheet_id(documento.enlace)
    print(sheet_id)
    registros = cargar_datos_hoja (sheet_id)
    return [EntradaChat.from_dict(row) for row in registros]


def cargar_datos_hoja(sheet_id, nombre_hoja="respuestas"):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("data-liora-dbc243002267.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).worksheet(nombre_hoja)
        return sheet.get_all_records()
    except Exception as e:
        print(f"Error al cargar la hoja: {e}")
        raise


def buscar_respuesta(pregunta, entradas):
    pregunta = pregunta.strip().lower()
    for entrada in entradas:
        if entrada.pregunta in pregunta:
            return entrada.respuesta
    return None
