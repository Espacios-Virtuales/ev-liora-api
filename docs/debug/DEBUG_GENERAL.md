# 🐞 DEBUG_GENERAL.md — Liora API (Unificado)

> Propósito: consolidar en **un solo documento** el estado, decisiones, checklist de avance, bitácora de migración y pasos de prueba/despliegue del proyecto **Liora** (Core + Plugins + Integraciones + Ingesta Catálogo).  
> **Última actualización:** 2025-08-28

---

## 0) Resumen ejecutivo (semáforo)
- **Estructura** (`services/core|plugins|integrations`, controllers, views): 🟡 en progreso
- **Modelos** (Cliente, Usuario, WabaAccount, ConvoState, ConversationLog, Catalog* , IngestLog, UserContext, ClientContext): 🟡 definidos (UUID/JSONB), migración aplicada
- **Servicios** (dominio + core + integraciones): 🟡 listos en su mayoría; `router_service` y `policy_service` por conectar
- **Controladores** (clientes, usuarios, waba, webhook, documentos, membresías): 🟢 homologados al envelope
- **Vistas** (API v1 + manejador de errores): 🟢 listo
- **Init** (create_app + /health): 🟢 operativo
- **Migraciones Alembic**: 🟢 **aplicadas** (baseline UUID/JSONB)
- **Tests mínimos**: 🔴 pendiente (unit + functional + integración)
- **Scraper/Agente**: fuera de MVP (documentado el patrón para replicar)

---

## 1) Objetivo y alcance del MVP
- **Multi‑tenant simple** por `cliente_id` en tablas compartidas.
- **Webhook Meta** (GET verify / POST events) conectado a un **router** de intents con plugins: *ecommerce*, *vida sana*, *reciclaje (placeholder)*.
- **Catálogo**: recepción de snapshot (CSV/API), validación, versionado y **activación atómica** en `CatalogActive`, con **Bitly/UTM** en enlaces hacia el sitio.
- **Observabilidad**: logs de conversación e ingesta, métricas mínimas.
- **Sin scraper ni agente** en esta primera iteración (se deja patrón replicable).
