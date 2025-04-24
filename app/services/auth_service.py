# app/services/auth_service.py

from app.models import Usuario, Membresia, Documento

def crear_usuario(nombre, email, membresia_id, documento_id=None):
    # Verificar existencia de la membresía
    membresia = Membresia.query.get(membresia_id)
    if not membresia:
        raise ValueError("Membresía no encontrada.")

    # Verificar existencia del documento si se proporciona
    documento = None
    if documento_id:
        documento = Documento.query.get(documento_id)
        if not documento:
            raise ValueError("Documento no encontrado.")

    # Crear y guardar el nuevo usuario
    nuevo_usuario = Usuario(
        nombre=nombre,
        email=email,
        membresia_id=membresia_id,
        documento_id=documento_id if documento else None
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario

def obtener_todos_usuarios():
    return Usuario.query.all()
