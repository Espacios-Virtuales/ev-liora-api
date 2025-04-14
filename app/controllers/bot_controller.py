from app.models.drive_model import DriveModel
from app.services.auth_service import validate_token

def process_request(data, token):
    user = validate_token(token)
    if not user:
        return "Token inválido"

    modelo = DriveModel(user["documento"])
    mensaje = data.get("message", "").lower()

    if "documento" in mensaje:
        return modelo.get_data("formato-123")
    return "No entendí tu mensaje."
