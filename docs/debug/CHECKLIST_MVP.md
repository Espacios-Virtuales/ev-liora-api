# ✅ Checklist — Liora MVP (Skill Ecommerce con Bitly + GPT-mini + Meta + CSV)

**Objetivo:** tener un prototipo mínimo que responda en WhatsApp (sandbox) con:
- **Catálogo Ecommerce** (cargado vía CSV → `CatalogSnapshot` → `CatalogActive`).
- **Links acortados** con Bitly (con UTM).
- **Fallback GPT-mini** para intents no reconocidos.
- **Webhook Meta** operativo con ngrok/local.

---

## 1) Base del Proyecto
- [x] Estructura repo ordenada (`services/core`, `services/skills`, `services/integrations`, `controllers`, `views`).
- [x] `.env` con claves mínimas:
  ```ini
  FLASK_ENV=development
  DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/liora_db
  WABA_VERIFY_TOKEN=changeme
  META_ACCESS_TOKEN=mock_or_sandbox
  BITLY_TOKEN=mock_or_real
  OPENAI_API_KEY=sk-...
  USE_OPENAI_FALLBACK=true
  ```
- [x] Migración inicial Alembic aplicada (UUID/JSONB).
- [ ] Seeds demo: **Cliente Demo**, **Usuario Owner**, **WABA Sandbox** (mock si no hay sandbox).

---

## 2) Integración Meta (WhatsApp)
- [x] `GET /webhook/meta` → responder `hub.challenge`.
- [x] `POST /webhook/meta` → validar firma HMAC (`X-Hub-Signature-256`).
- [ ] Conectar `router_service` al POST webhook.
- [ ] Probar con **ngrok**:
  ```bash
  flask run --port=5000
  ngrok http 5000
  # Usar: https://<subdominio>.ngrok-free.app/api/v1/webhook/meta
  ```
- [ ] Configurar en Meta Dashboard: Callback URL + Verify Token.

---

## 3) Catálogo + Ecommerce
- [x] `catalog_service.publish()` → validar CSV y calcular `checksum`.
- [x] Escribir `CatalogSnapshot` + activar `CatalogActive` atómicamente.
- [ ] Endpoint: `POST /clientes/{id}/catalog/publish` (archivo CSV + HMAC opcional).
- [ ] `skills/ecommerce_skill.py` consulta `CatalogActive` y arma respuesta.
- [ ] Respuesta incluye 3–5 productos (nombre + precio opcional) y **links Bitly**.

### CSV mínimo (ejemplo)
```csv
sku,name,url,price,stock,color,size
A001,Polera Andina,https://tienda.cl/polera-andina,12990,12,negro,M
A002,Polera Puna,https://tienda.cl/polera-puna,13990,8,blanco,L
```
Campos obligatorios: `name`, `url`. Recomendados: `price`, `stock`, `color`, `size`.

---

## 4) Integración Bitly
- [x] `bitly_service.shorten(url, utm_dict)` con fallback mock si no hay token.
- [ ] Usar token real desde `.env` y manejar errores 4xx/5xx con reintentos suaves.
- [ ] Adjuntar UTM por intent (ej.: `utm_source=wa`, `utm_medium=bot`, `utm_campaign=catalogo`, `utm_content=<cliente>/<intent>`).

---

## 5) Fallback GPT-mini (NLP Service)
- [ ] `nlp_service.reply(prompt, ctx)` usando modelo liviano (ej. `gpt-4o-mini`).
- [ ] Integrar en `router_service`: si **no-match** → llamar a `nlp_service`.
- [ ] Limitar consumo (p. ej., `max_tokens=60`, temperatura moderada).
- [ ] Flag configurable: `USE_OPENAI_FALLBACK=true|false`.

---

## 6) Logs y Observabilidad mínima
- [ ] `ConversationLog`: registrar `cliente_id`, `user_msisdn`, `intent`, `message_type`, `message_body`, `link_ctrs_json` (si aplica).
- [ ] `IngestLog`: métricas de carga (filas, errores, divergencias).
- [ ] Endpoint: `GET /clientes/{id}/logs?type=conversation|ingest&limit=50` (paginado simple).

---

## 7) QA rápido (Demo E2E)
1. **Publicar CSV** (5–10 productos) → `CatalogActive` actualizado.
2. Desde WhatsApp sandbox: enviar `catalogo` → recibir lista con **links Bitly**.
3. Enviar texto no reconocido → respuesta breve **GPT-mini** + menú.
4. Verificar `GET /clientes/{id}/logs` → aparecen eventos recientes.

---

## 8) Criterios de Aceptación (Done)
- [ ] Alta Cliente Demo + Usuario Owner + WABA (sandbox).
- [ ] Webhook Meta verificado (GET/POST).
- [ ] Catálogo publicado desde CSV y **activado**.
- [ ] Mensaje “ver catálogo” devuelve 3–5 ítems con **links acortados**.
- [ ] Mensaje no reconocido recibe **fallback GPT-mini**.
- [ ] Logs consultables por endpoint.

---

## 9) Riesgos y Controles
- **Cambio URL ngrok** → usar subdominio reservado o actualizar Callback URL cada reinicio.
- **Token Bitly inválido** → fallback a URL original + alerta en logs.
- **Gasto GPT** → `USE_OPENAI_FALLBACK=false` en caso de picos; `max_tokens` bajo.
- **CSV mal formado** → validación estricta + errores explicativos en `IngestLog`.

---

## 10) Siguientes pasos (post MVP)
- Rollback de catálogos por versión.
- `policy_service` mínimo (rate/quotas por plan).
- Dockerfile + docker-compose (web + db) y healthchecks.
- Piloto 3–5 clientes; métricas CTR/no-match básicas.
