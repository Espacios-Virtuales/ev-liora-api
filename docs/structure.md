
# 📂 Estructura del Proyecto — Liora (Core + Plugins)

Esta estructura refleja la migración a **plugins** independientes por capacidad, con contrato y registro centralizados.

```
ev-liora-api/
├─ app/
│  ├─ config.py
│  ├─ extensions.py
│  ├─ models/
│  │  ├─ cliente.py
│  │  ├─ usuario.py
│  │  ├─ user_context.py
│  │  ├─ client_context.py
│  │  ├─ waba_account.py
│  │  ├─ convo_state.py
│  │  ├─ conversation_log.py
│  │  ├─ catalog_active.py
│  │  ├─ catalog_snapshot.py
│  │  └─ ingest_log.py
│  ├─ services/
│  │  ├─ core/
│  │  │  ├─ context_service.py
│  │  │  ├─ router_service.py
│  │  │  ├─ policy_service.py
│  │  │  ├─ plugin_contracts.py      # NUEVO
│  │  │  ├─ plugin_registry.py       # NUEVO
│  │  │  └─ security.py
│  │  ├─ integrations/
│  │  │  ├─ whatsapp_service.py
│  │  │  ├─ bitly_service.py
│  │  │  └─ nlp_service.py
│  │  └─ catalog_service.py
│  ├─ plugins/                        # NUEVO: plugins internos (antes skills)
│  │  ├─ ecommerce/
│  │  │  ├─ plugin.py
│  │  │  └─ manifest.json
│  │  ├─ vida_sana/
│  │  │  ├─ plugin.py
│  │  │  └─ manifest.json
│  │  └─ reciclaje/
│  │     ├─ plugin.py
│  │     └─ manifest.json
│  ├─ controllers/
│  │  ├─ auth_controller.py
│  │  ├─ clientes_controller.py
│  │  ├─ usuarios_controller.py
│  │  ├─ waba_controller.py
│  │  ├─ meta_webhook_controller.py
│  │  └─ catalog_controller.py
│  └─ views/
│     ├─ api_view.py
│     └─ whatsapp_view.py
│
├─ apps_external/                     # plugins externos (microservicios)
│  ├─ scraper/
│  │  ├─ README.md
│  │  └─ src/...
│  └─ vida_sana_agent/
│     ├─ README.md
│     └─ src/...
│
├─ migrations/                        # Alembic
│  ├─ env.py
│  ├─ script.py.mako
│  └─ versions/
│     ├─ f07744c1193c_init_uuid_jsonb.py
│     └─ <yyyyMMddhhmm>_add_user_client_ctx.py
│
├─ scripts/
│  ├─ seed_demo.py
│  ├─ export_logs.py
│  └─ check_health.py
│
├─ tests/
│  ├─ unit/
│  ├─ functional/
│  └─ integration/
│
├─ docs/
│  ├─ structure.md                    # ← este documento
│  ├─ modules/
│  │  └─ plugins.md                   # guía completa de plugins
│  ├─ diagrams/
│  │  ├─ flow.md
│  │  ├─ models.md
│  │  └─ vision.md
│  └─ debug/
│     ├─ DEBUG_GENERAL.md
│     └─ checklist.md
│
├─ .env.example
├─ docker-compose.yml
├─ Dockerfile
├─ requirements.txt
├─ main.py
└─ README.md
```

## Principios
- **Plugins** no acceden directo a la DB → usan servicios del Core con *scope* por `cliente_id`.
- **Contrato + Registry**: `plugin_contracts.py` define la interfaz y `plugin_registry.py` registra/carga.
- **Políticas/Flags**: `policy_service` + `ClientContext.features` habilitan o limitan plugins por plan.
- **Observabilidad**: logs/CTR por plugin + versión (desde manifest).
