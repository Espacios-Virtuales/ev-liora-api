from app.models.sheet_model import get_document_link

def process_message(mensaje):
    mensaje = mensaje.lower()
    if "documento" in mensaje:
        return get_document_link("formato-123")
    elif "hola" in mensaje:
        return "¡Hola! Soy Liora. ¿En qué te puedo ayudar?"
    else:
        return "No entendí tu mensaje. ¿Puedes reformularlo?"
