
# BASE_MULTI_TENANT.md — Flujo de actividades para refactor y estructura base (según ev-liora-api.zip)

> Objetivo: **refactorizar** y **completar** la base multi-tenant alineando estructura, modelos (incl. contexto por usuario), servicios en subcarpetas y controladores, para habilitar las siguientes fases del MVP.

---

## 0) Punto de partida y convenciones

**Referencia de estructura esperada** (models, services/core|skills|integrations, controllers, views) está definida en los docs del repo【structure.md】.  
Adoptaremos estas convenciones:
- **Multi-tenant por `cliente_id`** en tablas compartidas.
- **Un contexto por usuario** (1:1 `Usuario` ↔ `UserContext`).
- Nombres de tablas en `snake_case`, timestamps `created_at`, `updated_at`.
- Autenticación por **JWT** con claims `{usuario_id, cliente_id, rol}`.
- Resolución de tenant: header `X-Client-ID` (rápido) y, en paralelo, JWT.

---

## 1) Refactor de estructura de carpetas

**Meta:** un layout coherente que soporte Core + Skills + Integraciones.

**Desde** (zip actual): `app/{models,controllers,services,views}`  
**Hacia** (organización final):
```
app/
  models/
    __init__.py
    cliente.py
    usuario.py
    user_context.py        # NUEVO (contexto 1:1 para usuario)
    waba_account.py
    convo_state.py
    conversation_log.py
    catalog_active.py
    catalog_snapshot.py
    ingest_log.py
  services/
    core/                  # núcleo
      context_service.py
      router_service.py
      policy_service.py
      security.py          # JWT, roles, decoradores
    skills/                # capacidades
      ecommerce_skill.py
      vida_sana_skill.py
      reciclaje_skill.py
    integrations/          # integraciones externas
      whatsapp_service.py  # Meta Cloud API
      bitly_service.py
      nlp_service.py       # OpenAI fallback (opcional)
    catalog_service.py     # (puede quedar aquí o en dominio propio)
  controllers/
    auth_controller.py
    clientes_controller.py
    usuarios_controller.py
    waba_controller.py
    meta_webhook_controller.py
    catalog_controller.py
  views/
    api_view.py
    whatsapp_view.py
```

**Actividades**
- [ ] Crear subcarpetas `services/core`, `services/skills`, `services/integrations` y mover archivos.
- [ ] Renombrar `wsp_controller.py` → `meta_webhook_controller.py`.
- [ ] Revisar imports y rutas (evitar ciclos).  
- [ ] Añadir `__init__.py` donde falte.

---

## 2) Modelos — completar base + contexto por usuario

**Meta:** levantar los modelos mínimos multi-tenant + **UserContext** (1:1).

### 2.1 Snippets propuestos (SQLAlchemy)

```python
# app/models/usuario.py
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    nombre = db.Column(db.String(100))
    estado = db.Column(db.String(20), default="activo")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación 1:1 con UserContext
    context = db.relationship("UserContext", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
```

```python
# app/models/user_context.py
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class UserContext(db.Model):
    __tablename__ = "user_contexts"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"), unique=True, nullable=False)
    cliente_id = db.Column(UUID(as_uuid=True), db.ForeignKey("clientes.id"), nullable=False)  # tenant scope
    msisdn = db.Column(db.String(30))                 # número WhatsApp del usuario (si aplica)
    last_intent = db.Column(db.String(50))
    slots_json = db.Column(db.JSON, default={})
    context_json = db.Column(db.JSON, default={})
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = db.relationship("Usuario", back_populates="context")
```

```python
# app/models/cliente.py
class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    plan = db.Column(db.String(20), default="free")
    estado = db.Column(db.String(20), default="activo")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

```python
# app/models/waba_account.py
class WabaAccount(db.Model):
    __tablename__ = "waba_accounts"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = db.Column(UUID(as_uuid=True), db.ForeignKey("clientes.id"), nullable=False, index=True)
    waba_id = db.Column(db.String(100), nullable=False)
    phone_number_id = db.Column(db.String(100), nullable=False)
    access_token = db.Column(db.Text, nullable=False)  # cifrar con Fernet/KMS en servicio
    webhook_url = db.Column(db.String(255))
    expiracion_token = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default="activo")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

> Nota: En tablas de conversación/catalogar, agrega `cliente_id` e índices por tenant.  
> Unicidades recomendadas: `UserContext.usuario_id` (1:1), `CatalogActive.cliente_id` (1:1).

### 2.2 Migraciones (Alembic)
- [ ] Configurar Alembic.
- [ ] `revision --autogenerate` con tablas nuevas y campos `cliente_id` en tablas clave.
- [ ] Seeds de desarrollo:
  - Cliente Demo + Usuario Owner (+ UserContext vacío).
  - WabaAccount de sandbox o mock.

**Comandos**
```bash
alembic init migrations
alembic revision -m "init multi-tenant with user_context" --autogenerate
alembic upgrade head
```

---

## 3) Servicios — reordenar y completar

**Meta:** separar núcleo, skills e integraciones; y cubrir casos base.

### 3.1 Core
```python
# app/services/core/context_service.py
from flask import request, g, abort

def resolve_tenant():
    cliente_id = request.headers.get("X-Client-ID")
    if not cliente_id:
        abort(400, "Missing X-Client-ID")
    g.cliente_id = cliente_id
    return cliente_id

def scoped_query(model):
    # si el modelo tiene cliente_id, aplica filtro por el tenant resuelto
    q = model.query
    if hasattr(model, "cliente_id") and hasattr(g, "cliente_id"):
        q = q.filter_by(cliente_id=g.cliente_id)
    return q
```

```python
# app/services/core/security.py
from functools import wraps
from flask import g, request, abort

def requires_tenant(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not getattr(g, "cliente_id", None):
            abort(400, "Tenant not resolved")
        return f(*args, **kwargs)
    return wrapper
```

### 3.2 Integrations
- `services/integrations/whatsapp_service.py`: envío de mensajes, validación de firma webhook (Meta).
- `services/integrations/bitly_service.py`: `shorten(url, utm)` + tagging por cliente/intent.
- `services/integrations/nlp_service.py` (opcional OpenAI).

### 3.3 Skills
- `skills/ecommerce_skill.py`: intents `catalogo.*`, lectura de `CatalogActive` y respuesta con links Bitly.
- `skills/vida_sana_skill.py`: intents `vida_sana.*` (MVP: 3 respuestas guionadas).
- `skills/reciclaje_skill.py`: placeholder (MVP).

---

## 4) Controladores — mínimos por dominio

**Auth**
```python
# app/controllers/auth_controller.py
@bp.route("/auth/login", methods=["POST"])
def login():
    # validar credenciales, devolver JWT con {usuario_id, cliente_id, rol}
    ...
```

**Clientes**
```python
# app/controllers/clientes_controller.py
@bp.route("/clientes", methods=["POST"])
@requires_tenant
def crear_cliente():
    # crear cliente (solo rol 'admin' global) o separar en backoffice
    ...
```

**Usuarios**
```python
# app/controllers/usuarios_controller.py
@bp.route("/clientes/<uuid:cliente_id>/usuarios", methods=["POST"])
@requires_tenant
def invitar_usuario(cliente_id):
    # crear usuario y vincular contexto
    ...
```

**WABA**
```python
# app/controllers/waba_controller.py
@bp.route("/clientes/<uuid:cliente_id>/waba", methods=["POST"])
@requires_tenant
def registrar_waba(cliente_id):
    # persistir datos y cifrar token en servicio
    ...
```

**Webhook Meta**
```python
# app/controllers/meta_webhook_controller.py
@bp.route("/webhook/meta", methods=["GET"])
def verify():
    # responder hub.challenge
    ...
@bp.route("/webhook/meta", methods=["POST"])
def events():
    # validar firma y enrutar a router_service
    ...
```

**Catálogo**
```python
# app/controllers/catalo g_controller.py
@bp.route("/clientes/<uuid:cliente_id>/catalog/publish", methods=["POST"])
@requires_tenant
def publish_snapshot(cliente_id):
    # validar HMAC + esquema, crear CatalogSnapshot y activar
    ...
```

---

## 5) Orden sugerido de actividades (E2E)

1. **Estructura**: crear subcarpetas y mover servicios a `core/`, `skills/`, `integrations/`.  
2. **Modelos**: agregar `UserContext` y completar campos `cliente_id` en tablas clave.  
3. **Alembic**: migración inicial + seeds (Cliente/Usuario/Waba/Context).  
4. **Core**: `context_service`, `security` (decoradores) y `router_service` (skeleton).  
5. **Controladores**: auth, clientes, usuarios, waba, catálogo y webhook Meta.  
6. **Integraciones**: WhatsApp (verify+send), Bitly (shorten), OpenAI (toggle).  
7. **Skills**: `ecommerce` (resumen catálogo + link), `vida_sana` (MVP), `reciclaje` (placeholder).  
8. **Pruebas**: unitarias de `catalog_service` y `bitly_service`; functional de webhook.  
9. **Demo**: sandbox de WhatsApp; flujo `catalogo.*` y `vida_sana.*`.  

---

## 6) Definition of Done (para esta fase)

- Tablas y migraciones aplicadas; `UserContext` 1:1 operativo.  
- Servicios reubicados en `core/`, `skills/`, `integrations/` sin imports circulares.  
- Controladores mínimos respondiendo (200/4xx) y protegidos por `requires_tenant`.  
- Webhook Meta verificado y capaz de registrar un evento en logs.  
- Publicación de catálogo a `CatalogActive` y respuesta con enlace Bitly en conversación.  

---

## 7) Próximos pasos (post base)

- JWT completo y roles (`owner`, `admin`, `agent`).  
- Cifrado de `access_token` WABA (Fernet/KMS).  
- Métricas y export (`GET /clientes/:id/logs`).  
- Router por intents con AIMD (backoff) para no-match.  

---

> Con este flujo tendrás la **base refactorizada** (modelos + contexto 1:1, servicios ordenados, controladores mínimos) y lista para integrar WhatsApp/Bitly/OpenAI en tu MVP.
