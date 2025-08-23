# 📑 Informe de Avance — Proyecto Liora

**Fecha:** 21 de agosto 2025  
**Última migración aplicada:** `f07744c1193c` (UUID/JSONB baseline)  
**Avance estimado:**  
- MVP: **80% completado**  
- Visión completa: **54%**

---

## 1. Resumen Ejecutivo
Liora es un **microservicio modular y multi-tenant** que enruta mensajes de WhatsApp (Meta Cloud API) hacia distintos **skills** (Ecommerce, Vida Sana, Reciclaje y Código).  
El MVP se centra en:  
- Publicación de **catálogo vía CSV**,  
- Generación de **links acortados con Bitly**,  
- Respuesta automática en WhatsApp Sandbox,  
- **Fallback con GPT-mini** en casos no reconocidos.

---

## 2. Estado Actual
### Estructura
- Reordenada según estándar `services/{core,skills,integrations}` y controladores desacoplados.  
- Modelo multi-tenant operativo (`cliente_id` en tablas compartidas).  

### Modelos (DB PostgreSQL)
- Tablas clave: `Cliente`, `Usuario`, `WabaAccount`, `ConvoState`, `ConversationLog`, `CatalogSnapshot`, `CatalogActive`, `IngestLog`, `UserContext`.  
- Migración inicial **aplicada** (UUID/JSONB, índices por `cliente_id`).  

### Servicios
- **Core**: `context_service` y `security` listos; `router_service` y `policy_service` en curso.  
- **Integraciones**:  
  - Meta Cloud API (verify + firma HMAC) → ✅  
  - Bitly (mock + UTM) → ✅ básico  
  - GPT-mini (OpenAI fallback) → pendiente integración.  
- **Dominios**: `catalog_service` con publish/activate/checksum funcional.  

### Skills
- Ecommerce → ✅ responde con catálogo + Bitly.  
- Vida Sana → ✅ respuestas mínimas.  
- Reciclaje → ✅ placeholder.  
- Código → 🚫 uso interno, fuera del MVP.  

### API
- Endpoints principales (`clientes`, `usuarios`, `waba`, `catalog/publish`, `webhook/meta`) definidos.  
- Envelope unificado de respuesta (`ok/data/error`).  

### QA & Deploy
- Pruebas unitarias → ⏳ pendientes.  
- Pruebas funcionales (E2E WhatsApp Sandbox con ngrok) → ⏳ pendientes.  
- Dockerfile/compose → ⏳ pendientes.  

---

## 3. Checklist MVP (resumen)
- [x] Estructura repo y migración inicial.  
- [x] Webhook Meta (GET/POST, firma verificada).  
- [x] CatalogService con CSV + checksum.  
- [x] Ecommerce Skill con Bitly.  
- [ ] Conectar router → webhook POST.  
- [ ] Integrar GPT-mini en fallback.  
- [ ] Seeds demo (Cliente, Usuario Owner, WABA sandbox).  
- [ ] Logs (`ConversationLog` + `IngestLog`).  
- [ ] QA E2E con WhatsApp sandbox.  

---

## 4. Riesgos y Limitaciones
- **ngrok URL volátil**: requiere actualizar callback en Meta cada reinicio.  
- **Tokens externos (Bitly, OpenAI)** aún mockeados → falta integrar productivo.  
- **Falta observabilidad** (logs centralizados, métricas y alertas).  
- **Despliegue productivo** aún sin plan (solo local).  

---

## 5. Próximos Pasos
1. Conectar `router_service` a `POST /webhook/meta`.  
2. Integrar `nlp_service` con GPT-mini como fallback.  
3. Sembrar Cliente Demo + Usuario Owner + WABA Sandbox.  
4. Implementar endpoints de logs (`/clientes/{id}/logs`).  
5. Pruebas unitarias y funcionales mínimas.  
6. Dockerfile + docker-compose (web + db).  
7. Demostración E2E con WhatsApp sandbox y catálogo CSV.  

---

📌 Con esto, Liora queda listo para un **piloto de 3–5 clientes**, midiendo CTR y tasa de *no-match*.
