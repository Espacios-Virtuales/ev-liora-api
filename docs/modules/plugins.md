# 🧩 Plugins & Skills — Liora

Liora está diseñada como un **core abstracto** extensible mediante *skills* (internos o externos).  
Cada *plugin* se registra en el **router conversacional**, que decide a qué skill enviar el intent.

---

## 1. ¿Qué es un plugin?

Un **plugin** es una extensión que agrega capacidades (skills) a Liora.  
Puede ser:

- **Interno** → implementado en `app/services/skills/<mi_skill>.py`.
- **Externo** → microservicio aparte en `apps_external/<mi_skill>/`, consumido vía HTTP desde un *wrapper*.

Ejemplos:
- 📲 Ecommerce (interno)  
- 🌱 Vida Sana (interno con opción de agente externo)  
- ♻️ Reciclaje (interno simple)  
- 💻 Código (interno, uso futuro)  
- 🧩 Scraper (externo, publica snapshots de catálogos)  

---

## 2. Estructura de Plugins

```
ev-liora-api/
├── app/
│   └── services/
│       ├── skills/
│       │   ├── ecommerce_skill.py
│       │   ├── vida_sana_skill.py
│       │   ├── reciclaje_skill.py
│       │   └── <mi_skill>.py         # NUEVO (interno)
└── apps_external/
    └── <mi_skill>/
        ├── README.md
        └── src/server.py             # NUEVO (externo opcional)
```

---

## 3. Contrato de un Skill

Todo skill expone:

```python
def handle_intent(event, state, ctx) -> dict:
    """
    event: dict → evento entrante (texto, tipo, etc.)
    state: dict → estado conversacional (slots, last_intent, …)
    ctx: dict   → contexto resuelto (cliente_id, plan, usuario)
    return: {
      "reply": str | list[dict],
      "state_patch": dict,
      "logs": dict,
      "handoff": bool
    }
    """
```

- `reply`: texto o mensajes enriquecidos.  
- `state_patch`: valores a persistir en `ConvoState/UserContext`.  
- `logs`: metadatos para `ConversationLog`.  
- `handoff`: si corresponde derivar a humano.

---

## 4. Registro en el Router

```python
# app/services/core/router_service.py
from app.services.skills import ecommerce_skill, vida_sana_skill
from app.services.skills import viajes_skill  # nuevo skill

SKILL_REGISTRY = {
    "catalogo": ecommerce_skill,
    "vida_sana": vida_sana_skill,
    "viajes": viajes_skill,
}

def handle_incoming(event, state, ctx):
    intent = detect_intent(event, state, ctx)
    category = intent.split(".", 1)[0]
    skill = SKILL_REGISTRY.get(category)
    return skill.handle_intent(event, state, ctx) if skill else fallback_reply(event)
```

---

## 5. Ejemplo de Skill Interno

```python
# app/services/skills/viajes_skill.py
def handle_intent(event, state, ctx):
    text = (event.get("text") or "").lower()
    intent = "viajes.busqueda" if "hotel" in text else "viajes.info"

    reply = "Puedo ayudarte a buscar hoteles ✈️"
    state_patch = {"last_intent": intent}
    logs = {"intent": intent, "query": text}
    return {"reply": reply, "state_patch": state_patch, "logs": logs, "handoff": False}
```

---

## 6. Ejemplo de Skill Externo

`apps_external/viajes_skill/src/server.py`:

```python
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    return jsonify({
        "results": [
            {"name": "Hotel Andino", "price": "$50.000"},
            {"name": "Hostal Puerto", "price": "$30.000"}
        ],
        "meta": {"took_ms": 120}
    })
```

`app/services/skills/viajes_skill.py` (wrapper):

```python
import requests

def handle_intent(event, state, ctx):
    try:
        r = requests.post(
            ctx["VIAJES_API_URL"] + "/search",
            json={"query": event["text"], "cliente_id": ctx["cliente_id"]},
            timeout=4
        )
        results = r.json().get("results", [])
        reply = "\n".join([f"• {x['name']} – {x['price']}" for x in results[:3]])
    except Exception:
        reply = "No pude obtener resultados ahora."

    return {"reply": reply, "state_patch": {"last_intent": "viajes.busqueda"}, "logs": {}, "handoff": False}
```

---

## 7. Seguridad & Políticas

- Cada plugin debe validar **flags** en `ClientContext` (ej. `features.viajes=true`).  
- Tokens o claves externas → `.env` (`VIAJES_API_KEY`).  
- Validar contenido recibido (no confiar en plugins externos).  
- Observabilidad: log de tiempos, errores y CTR.  

---

## 8. Checklist para agregar un Plugin

1. Crear archivo en `app/services/skills/` con `handle_intent`.  
2. Registrar en `router_service.SKILL_REGISTRY`.  
3. (Opcional) Crear microservicio en `apps_external/`.  
4. Añadir variables en `.env`.  
5. Escribir tests unitarios y funcionales.  
6. Documentar en este archivo (`docs/plugins.md`).  

---

## 9. Variables de entorno (ejemplo)

```env
# Plugin Viajes
VIAJES_API_URL=https://viajes-skill.internal
VIAJES_API_KEY=changeme
FEATURE_VIAJES=true
```

---

## 10. Preguntas Frecuentes

- **¿Un plugin puede ser solo local?**  
  Sí, no es obligatorio tener microservicio.  

- **¿Cómo manejo slots (talla, fecha, ciudad)?**  
  Usar `state_patch["slots_json"]`.  

- **¿Qué pasa si falla el microservicio?**  
  El skill debe retornar un fallback seguro.  
