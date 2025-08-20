
# 📈 PROGRESO — Liora (reformulado según DEBUG_GENERAL)

**Corte:** 2025-08-20 21:13 UTC  
**Alcance:** Core multi‑tenant + Webhook Meta + Catálogo + Skills (Ecommerce/Vida/Reciclaje)

---

## 1) Estado actual (semáforo ultra‑resumido)
- **Estructura y capas** (core/skills/integrations + controllers/views): 🟡 consistente, con pequeñas conexiones pendientes.
- **Modelos + Migración Alembic** (UUID/JSONB, índices/UNIQUE): 🟢 aplicadas (baseline OK, ver `f07744c1193c`).
- **Servicios** (core/domino/integraciones): 🟡 mayormente listos; falta conectar `router_service` y `policy_service`.
- **Controladores** (clientes/usuarios/waba/webhook/documentos/membresías): 🟢 homologados al envelope.
- **Vistas & Init** (`api_v1`, `errors_bp`, `/health`): 🟢 operativos.
- **Tests** (unit/functional): 🔴 por implementar.
- **Scraper/Agente**: 🚫 fuera del MVP (patrón definido).

---

## 2) Hitos logrados
1. **Migración Postgres + Alembic** con **UUID/JSONB** e índices por tenant → *OK* (upgrade a `head`).  
2. **Homologación HTTP**: envelope de respuestas y `api_v1` centralizado.  
3. **Modelo conversacional**: `ConvoState`, `ConversationLog` y catálogo (`CatalogActive/Snapshot`, `IngestLog`).  
4. **Integraciones base**: `whatsapp_service` (verify + firma HMAC) y `bitly_service` con UTM.  
5. **Skills** iniciales: *ecommerce*, *vida_sana*, *reciclaje* (placeholder).  
6. **DEBUG_GENERAL.md** unificado como única fuente de estado/bitácora.  

---

## 3) En curso inmediato (24–48 h)
- Conectar `router_service` al **POST /webhook/meta** y **persistir `slots_json`** luego de cada skill.  
- Implementar **`policy_service`** (flags/quotas por plan) y guardas en endpoints/skills.  
- **Seeds demo**: Cliente + Usuario owner + WABA sandbox/mock.  
- Documentar y afinar **catálogo** (`publish/activate` + opción de **rollback**).  
- **Tests mínimos**: `catalog_service`, `bitly_service`, `meta_webhook_controller` (verify+events).  

---

## 4) Riesgos y mitigaciones
- **Sin tests** aún → cubrir *happy path* y errores comunes antes del piloto.  
- **Multi‑tenant** (fugas de datos) → usar `resolve_tenant()` + `scoped_query()` en servicios/repos.  
- **Credenciales** (WABA/Bitly/OpenAI) → almacenar tokens cifrados, rotación y .env por entorno.  
- **Webhook firma** → validar `X-Hub-Signature-256`; registrar intentos fallidos para auditoría.  
- **Catálogo** (consistencia) → activar versión por transacción; mantener `checksum` y `source`.  

---

## 5) Definición de MVP (DoD ejecutable)
- Alta **Cliente/Usuario/WABA** (sandbox) por API.  
- Webhook verificado y **flujo conversacional** con 3 intents: `/catalogo`, `/vida`, `?`.  
- **Publicación de catálogo** (CSV) vía `/clientes/{id}/catalog/publish` + enlaces con **Bitly/UTM**.  
- **Logs** de conversación/ingesta consultables (últimos N eventos).  

---

## 6) Próximos entregables
- **Dockerfile + compose** (web + db) y healthchecks.  
- **Export** básico (`GET /clientes/{id}/export`) y métricas mínimas.  
- **Piloto** con 3–5 clientes y tablero simple de CTR/no‑match.  

---

### Referencias
- Estado y comandos: ver **DEBUG_GENERAL.md** (§0, §8, §11).

