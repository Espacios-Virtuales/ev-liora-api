from app.services.auth_service import validate_token
from app.services.sheet_service import load_sheet_data, procesar_pregunta

def process_request(data, token):
    user = validate_token(token)
    if not user:
        return "Token inválido"

    mensaje = data.get("message", "").lower()

    # Obtener el ID del documento asociado al usuario
    sheet_id = user.get("documento")  # Asegúrate de que 'documento' contiene el ID de la hoja

    if not sheet_id:
        return "No se encontró el documento asociado al usuario."

    try:
        # Cargar los datos de la hoja de cálculo
        datos_respuestas = load_sheet_data(sheet_id)
    except Exception as e:
        return f"Error al acceder al documento: {str(e)}"

    # Procesar la pregunta y obtener la respuesta
    respuesta = procesar_pregunta(mensaje, datos_respuestas)
    return respuesta
