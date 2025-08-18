# 🧭 Ruta de Solución — Liora Core (Multi‑tenant) → Integraciones → MVP

> Objetivo: **reparar y unificar la visión**, completar **modelos/servicios/controladores/migraciones** y habilitar **integraciones externas (Meta, Bitly, OpenAI)** para un **prototipo mínimo (MVP)** funcional.

---

## 0) Reparación & Unificación (1/2 días)

**Meta:** Alinear estructura real del repo con la visión actual y fijar convenciones.

- [ ] Alinear estructura del proyecto con `/app/{models,services,controllers,views}`.
- [ ] Renombrar: `wsp_controller.py` → `meta_webhook_controller.py`.
- [ ] Crear `app/services/core/{context_service.py,router_service.py,policy_service.py}`.
- [ ] Eliminar/aislar código obsoleto (comentado o “dead code”) en `archive/`.
- [ ] Activar entorno local con `.env` y `docker-compose` (si aplica).
- [ ] Definir **convenciones**:
  - Nombres de tablas en snake_case.
  - Campo `cliente_id` como **tenant_id** canónico.
  - `created_at/updated_at` por `db.Column(db.DateTime, server_default=...)`.
- [ ] Documentar en `docs/CONVENCIONES.md`.

**Decisiones rápidas**  
- **Tipo de multi‑tenant:** una base compartida con `cliente_id` en tablas (simple y suficiente para MVP).  
- **Auth:** JWT con claims `{usuario_id, cliente_id, rol}`.  
- **Resolución de tenant:** header `X-Client-ID` (simple); luego JWT.


---

## 1) Modelos & Migraciones (Alembic)

**Meta:** Un _esquema mínimo_ consistente para conversación, catálogo y auditoría.

### 1.1 Modelos (mínimos)
- `Cliente`: `id, slug, name, plan, estado, created_at, updated_at`
- `Usuario`: `id, email, password_hash, nombre, estado, created_at`
- `UserCliente` (si usuario puede pertenecer a varios clientes): `usuario_id, cliente_id, rol, estado`
- `WabaAccount`: `id, cliente_id, waba_id, phone_number_id, access_token (cifrado), webhook_url, expiracion_token, estado`
- `ConvoState`: `id, cliente_id, waba_account_id, user_msisdn, last_intent, slots_json, updated_at`
- `ConversationLog`: `id, cliente_id, waba_account_id, user_msisdn, direction, intent, slots_json, message_type, message_body, created_at`
- `CatalogSnapshot`: `id, cliente_id, version, checksum, rows_count, source, created_at`
- `CatalogActive`: `id, cliente_id, version, rows_count, stock_pct, created_at`
- `IngestLog`: `id, cliente_id, snapshot_id, errors_json, divergences_json, metrics_json, created_at`

### 1.2 Migraciones
- [ ] Instalar Alembic y configurar `alembic.ini` + `env.py` para SQLAlchemy.
- [ ] **Migración inicial** con todas las tablas anteriores e índices por `cliente_id`.
- [ ] Seeds de desarrollo:
  - [ ] `Cliente Demo (slug=demo)`
  - [ ] `Usuario Owner (owner@demo)` + `UserCliente(rol='owner')`
  - [ ] `WabaAccount` *mock* (token de prueba).

**Comandos sugeridos**
```bash
alembic init migrations
alembic revision -m "init" --autogenerate
alembic upgrade head
```

**Definition of Done (DoD)**
- Listar tablas con `\dt` (Postgres) o pragma (SQLite) y verificar claves foráneas & índices.
- Crear/leer registros básicos desde un script de prueba o `flask shell`.

---

## 2) Servicios (Core & Dominios)

**Meta:** Encapsular la lógica y asegurar *scoping* por tenant.

### 2.1 Core
- `context_service.py`
  - `resolve_tenant(request)`: lee `X-Client-ID` o JWT → `cliente_id`.
  - `scoped_query(model)`: _helper_ que aplica filtro `model.cliente_id==ctx.cliente_id` si el modelo lo tiene.
- `router_service.py`
  - `handle_incoming(evento, estado)`: deriva a skills (`ecommerce`, `vida_sana`, `reciclaje`) o fallback menú.
- `policy_service.py`
  - Límite de tasa por plan (`free/basic/pro`), cuotas, flags de features.

### 2.2 Dominios
- `whatsapp_service.py`: envío de mensajes (Meta API), validación de firma webhook.
- `catalog_service.py`: validación snapshot, `checksum`, `activar` versión → `CatalogActive`.
- `bitly_service.py`: acortado + UTM.
- `nlp_service.py` (opcional): fallback a OpenAI para *no‑match* o respuesta breve.
- *Skills* (`services/skills/`):
  - `ecommerce_skill.py`: intents `catalogo.*`, slot‑filling, enlaces Bitly.
  - `vida_sana_skill.py`: intents `vida_sana.*` (planes/bitácoras mínimas).
  - `reciclaje_skill.py`: intents `reciclaje.*` (placeholder MVP).

**DoD**
- Servicios desacoplados, sin circular imports.
- Pruebas unitarias mínimas para `catalog_service` (checksum/activar) y `bitly_service` (mock).

---

## 3) Controladores (API v1)

**Meta:** Superficie mínima y segura para operar tenants, usuarios y WABA.

- **Auth**
  - `POST /auth/login` → JWT `{usuario_id, cliente_id, rol}`
  - `GET  /me` → perfil + tenants/roles
- **Clientes**
  - `POST /clientes` (owner/admin) → crear
  - `GET  /clientes/:id` → detalle
- **Usuarios por cliente**
  - `POST /clientes/:id/usuarios` (invitar/rol)
  - `PATCH /clientes/:id/usuarios/:uid` (cambiar rol/estado)
- **WABA**
  - `GET  /clientes/:id/waba` (listar)
  - `POST /clientes/:id/waba` (registrar/actualizar token/webhook)
- **Webhooks Meta**
  - `GET  /webhook/meta` (challenge/verify)
  - `POST /webhook/meta` (eventos) → `router_service`
- **Catálogo**
  - `POST /clientes/:id/catalog/publish` (push externo con HMAC)
  - `GET  /clientes/:id/logs` (conversación/ingesta, paginado)

**DoD**
- Decoradores `@requires_tenant` y `@requires_role` funcionando (403/401 correctos).
- Respuestas JSON con códigos de estado claros y error handling homogéneo.


---

## 4) Seguridad & Config

**Variables .env**
```
FLASK_ENV=development
DATABASE_URL=sqlite:///liora.db  # o postgres
JWT_SECRET=changeme
ENCRYPTION_KEY=changeme           # cifrado tokens WABA
WABA_VERIFY_TOKEN=changeme
META_ACCESS_TOKEN=mock            # provisoria para dev
BITLY_TOKEN=mock
OPENAI_API_KEY=mock
ALLOWED_ORIGINS=*
```

**Medidas**
- Cifrado `WabaAccount.access_token` (Fernet/KMS).
- Validación de firma `X-Hub-Signature-256` en `POST /webhook/meta`.
- Rate limiting por IP/tenant/endpoint.
- CORS + CSRF (si cookies).


---

## 5) Integraciones externas

### 5.1 Meta Cloud API (WhatsApp)
- [ ] `GET /webhook/meta` → responder `hub.challenge` validando `hub.verify_token`.
- [ ] `POST /webhook/meta` → validar firma HMAC SHA-256 (clave app secret).
- [ ] `whatsapp_service.send_text(to, body, waba_account)`:
  - URL base `https://graph.facebook.com/v19.0/{phone_number_id}/messages`
  - Headers `Authorization: Bearer <access_token>`
  - Body mínimo `{ messaging_product: "whatsapp", to, type: "text", text: { body } }`
- [ ] Manejo de errores y reintentos (429/5xx).

### 5.2 Bitly
- [ ] `shorten(url, utm_dict)` y `append_utm(url, utm_dict)`.
- [ ] Taggear links por `cliente_id` y `intent` para CTR.

### 5.3 OpenAI (fallback NL)
- [ ] `nlp_service.reply(prompt, ctx)` → llamada simple a `chat.completions` o `responses` API.
- [ ] Uso **solo** para fallback `no‑match` y copys breves, con `max_tokens` bajo.
- [ ] Respetar cuotas según `policy_service`.

**DoD**
- Pruebas de integración simuladas con **mocks** (no golpear servicios en CI).
- Variable‑flag `USE_OPENAI_FALLBACK=true|false`.


---

## 6) Flujo Conversacional (MVP)

1) Usuario envía texto → **Meta** → `POST /webhook/meta`.  
2) `context_service` resuelve `cliente_id` (por número destino o mapping).  
3) `ConvoState.get_or_create(user_msisdn, cliente_id)`.  
4) `router_service.handle_incoming(...)`:
   - Si `catalogo.*` → `ecommerce_skill` → `catalog_service` → links Bitly → `whatsapp_service.send_text`.
   - Si `vida_sana.*` → respuestas breves + registro en `ConversationLog`.
   - Si no‑match → `nlp_service` (si habilitado) o menú de ayuda.
5) Log de conversación y métricas básicas (latencia, intent, CTR).

**DoD**
- Demostración con **Cliente Demo**: 3 intents (`/catalogo`, `/vida`, `?`) y respuesta efectiva por WhatsApp Sandbox.


---

## 7) Entrega de MVP

**Criterios de Aceptación**
- [ ] Crear Cliente, Invitar Usuario, Registrar WABA (mock real o sandbox).
- [ ] Recibir y responder mensaje real en WhatsApp (sandbox).
- [ ] Publicar snapshot de catálogo (CSV) vía `POST /clientes/:id/catalog/publish`.
- [ ] Enviar al menos 1 link acortado por Bitly y registrar CTR (simulado).
- [ ] Export básico de logs a CSV/JSON (`GET /clientes/:id/export` opcional).

**Demo Script (5–7 min)**
1. Alta Cliente + Usuario owner (via API).
2. Configurar WABA sandbox y verificar webhook.
3. Publicar catálogo (CSV de 5–10 ítems).
4. Conversación: “ver catálogo”, “vida sana”, “ayuda”.
5. Mostrar logs (últimos 10 eventos) y tiempos de respuesta.


---

## 8) QA & Monitoreo

- [ ] Tests unitarios: `catalog_service`, `bitly_service`, `context_service`, `meta_webhook_controller` (verify+events).
- [ ] Tests funcionales: flujo `catalogo.*` y `vida_sana.*` (mock WhatsApp).
- [ ] Load test suave del webhook (100–300 req/min en dev).
- [ ] Métricas mínimas: `requests_count`, `error_rate`, `avg_latency_ms` por endpoint/tenant.


---

## 9) Despliegue (dev → staging)

- [ ] `Dockerfile` + `docker-compose.yml` (web + db).
- [ ] Variables por entorno: `development`, `staging`, `production`.
- [ ] Healthchecks `/health` y readiness `/ready`.
- [ ] Backups de DB y rotación de logs.
- [ ] Monitoreo (uptime + alerta 5xx).


---

## 10) Backlog inmediato (orden sugerido)

1. Migración inicial Alembic + seeds (Cliente/Usuario/WABA).  
2. `context_service` + decoradores `@requires_tenant` / `@requires_role`.  
3. Controladores: `clientes`, `usuarios`, `waba`.  
4. Webhook Meta (GET/POST) + validación de firma.  
5. `catalog_service` + endpoint `publish`.  
6. `ecommerce_skill` (resumen catálogo + links Bitly).  
7. `vida_sana_skill` (3 respuestas guionadas).  
8. `nlp_service` (toggle).  
9. Observabilidad mínima + export básico.  
10. Demo E2E (sandbox).


---

### Anexos

**Tablas con índices por tenant**  
- `ConvoState`: `unique(user_msisdn, cliente_id)`  
- `CatalogActive`: `unique(cliente_id)`  
- `ConversationLog`: índice `{cliente_id, created_at}`  
- `CatalogSnapshot`: índice `{cliente_id, version}`

**Códigos de error estándar**  
- `401` no autenticado · `403` sin rol · `404` no existe · `409` conflicto de versión · `422` validación · `429` rate limit · `5xx` upstream/servidor.

---

> Con esta ruta cubrimos: **reparación + unificación**, **modelos/servicios/controladores/migraciones**, **integraciones (Meta/Bitly/OpenAI)** y un **MVP demostrable**. Siguiente paso: ejecutar el punto **1** (migraciones + seeds) y validar ambiente local.
