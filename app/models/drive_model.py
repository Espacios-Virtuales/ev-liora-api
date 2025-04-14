from app.models.base_model import BaseModel

class DriveModel(BaseModel):
    def __init__(self, doc_id):
        self.doc_id = doc_id
        # Aquí conectarías con gspread o API de Google Drive

    def get_data(self, codigo):
        # Simulación de búsqueda
        return f"Simulación de búsqueda para '{codigo}' en documento '{self.doc_id}'"
