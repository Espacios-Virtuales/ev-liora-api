import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.models import Documento

def extraer_id_hoja(enlace):
    patron = r'/d/([a-zA-Z0-9-_]+)'
    coincidencia = re.search(patron, enlace)
    if coincidencia:
        return coincidencia.group(1)
    return None

def cargar_datos_hoja(documento_id, nombre_hoja="respuestas"):
    # Obtener el documento desde la base de datos
    documento = Documento.query.get(documento_id)
    if not documento:
        raise ValueError("Documento no encontrado.")

    # Extraer el ID de la hoja de cálculo desde el enlace
    sheet_id = extraer_id_hoja(documento.enlace)
    if not sheet_id:
        raise ValueError("ID de hoja de cálculo no válido.")

    # Configurar las credenciales y el cliente de gspread
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("data-liora-dbc243002267.json", scope)
    client = gspread.authorize(creds)

    # Abrir la hoja de cálculo y la hoja específica
    sheet = client.open_by_key(sheet_id).worksheet(nombre_hoja)

    # Obtener todos los registros de la hoja
    data = sheet.get_all_records()
    return data

def procesar_pregunta(pregunta, sheet_data):
    pregunta = pregunta.strip().lower()
    for fila in sheet_data:
        if fila["pregunta"].strip().lower() in pregunta:
            return fila["respuesta"]
    return "No estoy segura de cómo responder eso aún. ¿Quieres hablar con un humano?"
