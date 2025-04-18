class EntradaChat:
    def __init__(self, pregunta, respuesta, contexto=None, categoria=None, prioridad=None):
        self.pregunta = pregunta.strip().lower()
        self.respuesta = respuesta
        self.contexto = contexto
        self.categoria = categoria
        self.prioridad = prioridad

    @staticmethod
    def from_dict(data):
        return EntradaChat(
            pregunta=data.get("pregunta"),
            respuesta=data.get("respuesta"),
            contexto=data.get("contexto"),
            categoria=data.get("categoria"),
            prioridad=data.get("prioridad")
        )
