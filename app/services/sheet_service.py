import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_sheet_data(sheet_id, nombre_hoja="respuestas"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).worksheet(nombre_hoja)
    data = sheet.get_all_records()
    return data

def procesar_pregunta(pregunta, sheet_data):
    pregunta = pregunta.strip().lower()
    for fila in sheet_data:
        if fila["pregunta"].strip().lower() in pregunta:
            return fila["respuesta"]
    return "No estoy segura cómo responder eso aún, ¿quieres hablar con un humano?"
