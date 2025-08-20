
# 🐞 DEBUG_GENERAL.md — Liora API (Unificado)

> Propósito: consolidar en **un solo documento** el estado, decisiones, checklist de avance, bitácora de migración y pasos de prueba/despliegue del proyecto **Liora** (Core + Skills + Integraciones + Ingesta Catálogo).  
> **Última actualización:** 2025-08-20 21:10:23 UTC

---

## 0) Resumen ejecutivo (semáforo)
- **Estructura** (`services/core|skills|integrations`, controllers, views): 🟡 en progreso
- **Modelos** (Cliente, Usuario, WabaAccount, ConvoState, ConversationLog, Catalog* , IngestLog, UserContext, ClientContext): 🟡 definidos (UUID/JSONB), migración aplicada
- **Servicios** (dominio + core + integraciones): 🟡 listos en su mayoría; `router_service` y `policy_service` por conectar
- **Controladores** (clientes, usuarios, waba, webhook, documentos, membresías): 🟢 homologados al envelope
- **Vistas** (API v1 + manejador de errores): 🟢 listo
- **Init** (create_app + /health): 🟢 operativo
- **Migraciones Alembic**: 🟢 **aplicadas** (baseline UUID/JSONB) — rev `f07744c1193c`
- **Tests mínimos**: 🔴 pendiente (unit + functional + integración)
- **Scraper/Agente**: fuera de MVP (documentado el patrón para replicar)

---

## 1) Objetivo y alcance del MVP
- **Multi‑tenant simple** por `cliente_id` en tablas compartidas.
- **Webhook Meta** (GET verify / POST events) conectado a un **router** de intents con skills: *ecommerce*, *vida sana*, *reciclaje (placeholder)*.
- **Catálogo**: recepción de snapshot (CSV/API), validación, versionado y **activación atómica** en `CatalogActive`, con **Bitly/UTM** en enlaces hacia el sitio.
- **Observabilidad**: logs de conversación e ingesta, métricas mínimas.
- **Sin scraper ni agente** en esta primera iteración (se deja patrón replicable).

**Criterios de aceptación** (demo E2E):
1) Alta de Cliente + Usuario (owner).  
2) Registrar WABA (sandbox/mock) y verificar webhook.  
3) Publicar catálogo (CSV) vía `POST /clientes/{id}/catalog/publish`.  
4) Flujo de conversación con 3 intents: `/catalogo`, `/vida`, `?` (menú).  
5) Mostrar logs recientes y un enlace con Bitly.

---

## 2) Arquitectura y estructura del repo
```
app/
  models/                # SQLAlchemy (UUID/JSONB)
  services/
    core/                # context, router, policy, security
    skills/              # ecommerce, vida_sana, reciclaje
    integrations/        # whatsapp (Meta), bitly, nlp (OpenAI, opcional)
    catalog_service.py   # dominio catálogo (publish/activate)
  controllers/           # HTTP (no lógica de negocio)
  views/                 # responses.py, errors.py, api_view.py
  extensions.py          # db, naming convention, init
```
**Principios**: Controllers validan y devuelven *envelope*; Services orquestan; Repos/Providers adaptan DB/APIs; nada de `jsonify` en servicios. Patrón **Ports & Adapters** ligero.

---

## 3) Base de datos y migración
- **Motor**: PostgreSQL.
- **Tipos**: `UUID(as_uuid=True)` en PK/FK; **JSONB** en campos de estado/slots/métricas.
- **Baseline Alembic**: **OK** (rev `f07744c1193c`) con import explícito `from sqlalchemy.dialects import postgresql as pg`.
- **Relaciones clave**:
  - `Cliente` ↔ `WabaAccount` (**1:1** vía `waba_accounts.cliente_id UNIQUE` + `ondelete=CASCADE`).
  - `UserContext` (**1:1** con `Usuario`; scoping por `cliente_id`).
  - `ConvoState`: `UNIQUE(waba_account_id, user_msisdn)`.
  - `CatalogSnapshot`: `UNIQUE(cliente_id, version)`.
  - `CatalogActive`: `UNIQUE(cliente_id)`.
- **Índices**: `cliente_id` en tablas de alto tráfico; índices `{cliente_id, created_at}` para logs/snapshots.
- **Health**: `GET /health → { "ok": true, "service": "liora-api" }`.

**Comandos útiles**:
```bash
# Reset y baseline de migraciones (dev)
rm -f migrations/versions/*.py
alembic revision -m "init schema (uuid baseline)" --autogenerate
alembic upgrade head
```

---

## 4) Modelos (ER simplificado)
- **WabaAccount**: credenciales y número (`phone_number_id`), token (cifrar con Fernet/KMS en prod).
- **Cliente**: `slug`, `plan`, `estado`, `waba_account_id` (si aplica).
- **Usuario**: datos básicos + relación 1:1 con `UserContext`.
- **ConvoState**: último intent, `slots_json`, `context_json` (scoped por `cliente_id`).
- **ConversationLog**: dirección in/out, intent, cuerpo, CTRs, handoff.
- **CatalogSnapshot**: versión, checksum, source (scraper/bitcommerce/manual), rows.
- **CatalogActive**: última versión activa por cliente.
- **IngestLog**: errores/divergencias/métricas por corrida.
- **ClientContext/UserContext**: configuración y estado 1:1 por tenant/usuario.

---

## 5) Servicios (Core, Dominios e Integraciones)
**Core**
- `context_service`: `resolve_tenant()` y `scoped_query()`.
- `security`: decoradores `@requires_tenant` y (futuro) roles por JWT.
- `router_service`: enruta intents hacia skills (pendiente de conectar a POST webhook).
- `policy_service`: flags/quotas según plan (pendiente).

**Dominios**
- `catalog_service`: validar snapshot, `checksum`, `activar` versión y exponer *get/list*.
- `chat_service`/`sheet_service`: extracción de registros cuando aplique.

**Integraciones**
- `whatsapp_service`: **verify**/firma HMAC para `POST /webhook/meta` + `send_text` (Meta v19 URL base `https://graph.facebook.com/v19.0/{phone_number_id}/messages`).
- `bitly_service`: `shorten(url, utm)` + tagging por `cliente_id`/intent.
- `nlp_service` (opcional): fallback para *no‑match* con límites.

**Skills**
- `ecommerce_skill`: consulta `CatalogActive`, slot‑filling (talla/color), links Bitly.
- `vida_sana_skill`: respuestas guionadas + bitácoras.
- `reciclaje_skill`: placeholder MVP.

---

## 6) API v1 — Endpoints mínimos
- **Auth** (pendiente completo): `POST /auth/login`, `GET /me`.
- **Clientes**: `POST /clientes`, `GET /clientes/:id`.
- **Usuarios**: `POST /clientes/:id/usuarios`, `PATCH /clientes/:id/usuarios/:uid`.
- **WABA**: `GET/POST /waba`, `PATCH/DELETE /waba`, `POST/DELETE /clientes/:id/waba` (attach/detach).
- **Webhook Meta**: `GET /webhook/meta` (challenge/verify), `POST /webhook/meta` (events → router).
- **Catálogo**: `POST /clientes/:id/catalog/publish` (HMAC + esquema), `GET /clientes/:id/logs` (paginado).

**Envelope de respuesta**:  
Éxito → `{ "ok": true, "data": ..., "meta": ... }` · Error → `{ "ok": false, "error": { code, message, details } }`.

---

## 7) Variables de entorno (.env)
```env
FLASK_ENV=development
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/liora
JWT_SECRET=changeme
ENCRYPTION_KEY=changeme           # cifrado WABA access_token
WABA_VERIFY_TOKEN=changeme
META_ACCESS_TOKEN=mock
BITLY_TOKEN=mock
OPENAI_API_KEY=mock
ALLOWED_ORIGINS=*
LOG_LEVEL=DEBUG
SQLALCHEMY_ECHO=1
SQLALCHEMY_ECHO_POOL=1
```

---

## 8) Pruebas manuales rápidas (curl)
```bash
# Crear cliente
curl -s -X POST http://localhost:5000/api/v1/clientes   -H "Content-Type: application/json"   -d '{"nombre":"Tienda Andina","slug":"tienda-andina"}' | jq

# Crear usuario del cliente (id=...)
curl -s -X POST http://localhost:5000/api/v1/clientes/<CLIENTE_ID>/usuarios   -H "Content-Type: application/json" -H "X-Client-ID: <CLIENTE_ID>"   -d '{"nombre":"Alice","email":"alice@andina.cl","membresia_id":1}' | jq

# WABA: crear
curl -s -X POST http://localhost:5000/api/v1/waba -H "Content-Type: application/json" -d '{"name":"Sandbox","waba_id":"123","phone_number_id":"999","numero_e164":"+56900000000","access_token":"EAAG...","verify_token":"changeme","app_secret":"secret"}' | jq

# Attach WABA al cliente
curl -s -X POST http://localhost:5000/api/v1/clientes/<CLIENTE_ID>/waba -H "Content-Type: application/json" -d '{"waba_account_id":"<WABA_ID>"}' | jq

# Webhook verify
curl -s "http://localhost:5000/api/v1/webhook/meta?hub.mode=subscribe&hub.verify_token=changeme&hub.challenge=123"
```

---

## 9) Observabilidad y estilo
- Logs con `cliente_id` y `usuario_id` cuando aplique.
- Métricas mínimas: `requests_count`, `error_rate`, `avg_latency_ms` por endpoint.
- Export opcional: `GET /clientes/:id/export` (CSV/JSON).
- Códigos estándar: `401, 403, 404, 409, 422, 429, 5xx`.

---

## 10) Checklist de desarrollo (unificado)
### Base
- [x] Estructura del repo ordenada (core/skills/integrations).
- [x] `.env` base y conexión a Postgres.
- [x] Migración inicial Alembic (UUID/JSONB) — **OK**.
- [ ] Seeds demo (Cliente/Usuario/WABA).

### Integración Meta & Routing
- [x] `GET /webhook/meta` (verify).
- [x] `POST /webhook/meta` (firma HMAC verificada).
- [ ] Conectar `router_service` y persistir `UserContext.slots_json` tras skill.
- [ ] `policy_service` y guardas por plan.

### Catálogo + Ecommerce
- [x] `catalog_service` con publish/activate/get/list.
- [x] Validadores (talla/color) y `checksum`.
- [x] Bitly/UTM en enlaces de salida.
- [ ] Rollback de versiones.

### Skills
- [x] `ecommerce` (resumen catálogo + links).
- [x] `vida_sana` (tips/bitácora mínima).
- [x] `reciclaje` (placeholder).

### QA y Piloto
- [ ] Unit tests (catalog, bitly, context, webhook verify).
- [ ] Functional (catalogo.*, vida_sana.* con mock WhatsApp).
- [ ] Ingesta snapshot real (CSV Bitcommerce).
- [ ] Piloto 3–5 clientes.

### Despliegue/Operación
- [ ] Dockerfile + compose (web + db).
- [ ] Backups DB + rotación de logs.
- [ ] Monitoreo uptime + alertas (ingesta fallida, no‑match alto).
- [ ] Plan de escalado y soporte.

---

## 11) Bitácora de migración y cambios
- 2025‑08‑20 — Migración a Postgres; baseline Alembic `f07744c1193c` con `pg.UUID/pg.JSONB`; índices y UNIQUEs clave.
- 2025‑08‑20 — `extensions.py`: naming convention estable para constraints/índices.
- 2025‑08‑20 — `__init__.py`: patrón import‑safe, logging de SQL y healthcheck.
- 2025‑08‑20 — Limpieza de `NumeroWhatsApp` legacy; `wsp_controller` → `meta_webhook_controller`.
- 2025‑08‑20 — `alembic upgrade head` ejecutado **OK** (dev).

---

## 12) “Grep checklist” (higiene de código)
```bash
git grep -n "from app import db"             # → debe ser app.extensions
git grep -n "NumeroWhatsApp"                 # legacy removido
git grep -n "wsp_controller"                 # legacy
git grep -n "jsonify(" app/services app/controllers  # no en services
git grep -n "api_bp"                         # migrado a api_v1
git grep -n "whatsapp_service.py" app/services       # debe vivir en integrations/
```

---

## 13) Próximos pasos (orden sugerido)
1. Conectar `router_service` en `POST /webhook/meta` y persistencia de slots por skill.
2. Implementar `policy_service` por plan (+ guardas en endpoints/skills).
3. Endpoints de catálogo completamente documentados (publish/activate/rollback).
4. Sembrado demo + pruebas unitarias/funcionales.
5. Docker + despliegue de dev → staging.

---

## 14) Anexo — Patrón replicable (módulos nuevos, p.ej. scraper)
- **Capas**: Controller → Service → [Repository | Provider].
- **Providers** con timeouts y retry/backoff; **Repositories** sin Flask.
- **Checklist**: Service + Repo + Provider + Controller + View + Tests.

---

> **Nota**: este documento reemplaza los debug parciales anteriores. Toda nueva actividad debe registrarse aquí (estado semáforo, checklist, bitácora).
