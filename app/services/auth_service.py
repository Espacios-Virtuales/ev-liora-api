def validate_token(token):
    usuarios = {
        "abc123": {"usuario": "David", "documento": "doc_espacios_virtuales"},
        "xyz789": {"usuario": "Ana", "documento": "doc_cursos"}
    }
    return usuarios.get(token)
