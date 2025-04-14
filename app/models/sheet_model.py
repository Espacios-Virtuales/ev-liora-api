import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_document_link(codigo):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("MisDocumentos").sheet1
    data = sheet.get_all_records()

    for row in data:
        if row["codigo"] == codigo:
            return row["enlace"]

    return "No encontré ese documento."
