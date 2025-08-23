# 📂 Estructura del Proyecto

```
ev-liora-api/
├─ app/                                   # Flask app (núcleo Liora)
│  ├─ __init__.py
│  ├─ config.py
│  ├─ extensions.py                       # db + naming conventions, init
│  ├─ views/
│  │  ├─ api_view.py
│  │  └─ whatsapp_view.py
│  ├─ controllers/                        # HTTP surface (sin lógica de negocio)
│  │  ├─ auth_controller.py
│  │  ├─ clientes_controller.py
│  │  ├─ usuarios_controller.py
│  │  ├─ waba_controller.py
│  │  ├─ meta_webhook_controller.py
│  │  └─ catalog_controller.py
│  ├─ services/
│  │  ├─ core/                            # núcleo
│  │  │  ├─ context_service.py
│  │  │  ├─ router_service.py
│  │  │  ├─ policy_service.py
│  │  │  └─ security.py
│  │  ├─ skills/                          # capacidades (activadas por router)
│  │  │  ├─ ecommerce_skill.py
│  │  │  ├─ vida_sana_skill.py
│  │  │  └─ reciclaje_skill.py
│  │  ├─ integrations/                    # providers externos
│  │  │  ├─ whatsapp_service.py           # Meta Cloud API
│  │  │  ├─ bitly_service.py
│  │  │  └─ nlp_service.py                # opcional (fallback GPT-mini)
│  │  └─ catalog_service.py               # dominio catálogo (publish/activate)
│  └─ models/                             # SQLAlchemy (UUID/JSONB, índices)
│     ├─ cliente.py
│     ├─ usuario.py
│     ├─ user_context.py                  # 1:1 con Usuario (scope por cliente_id)
│     ├─ client_context.py                # 1:1 con Cliente (políticas/branding)
│     ├─ waba_account.py
│     ├─ convo_state.py
│     ├─ conversation_log.py
│     ├─ catalog_active.py
│     ├─ catalog_snapshot.py
│     ├─ ingest_log.py
│     ├─ membresia.py
│     └─ documento.py
│
├─ apps_external/                         # Apps/microservicios fuera del core API
│  ├─ scraper/                            # (futuro) extracción catálogos
│  │  ├─ README.md
│  │  ├─ requirements.txt
│  │  └─ src/...
│  └─ vida_sana_agent/                    # (futuro) agente Vida Sana (vector/IA)
│     ├─ README.md
│     └─ src/...
│
├─ scripts/                               # utilidades locales/ci (no librería)
│  ├─ seed_demo.py                        # crea cliente demo + usuario + waba (mock)
│  ├─ gen_mermaid_from_db.py              # ER/diagramas a docs (si aplica)
│  ├─ export_logs.py                      # export convers./ingesta a CSV/JSON
│  └─ check_health.py                     # verificación simple /health
│
├─ migrations/                            # Alembic (DB schema & seeds)
│  ├─ env.py
│  ├─ script.py.mako
│  └─ versions/
│     ├─ f07744c1193c_init_uuid_jsonb.py  # baseline UUID/JSONB ✅
│     └─ <yyyyMMddhhmm>_add_user_client_ctx.py
│
├─ tests/                                 # Pytest (unit + functional + integração)
│  ├─ conftest.py
│  ├─ unit/
│  │  ├─ test_catalog_service.py
│  │  ├─ test_bitly_service.py
│  │  ├─ test_context_service.py
│  │  └─ test_meta_verify.py
│  ├─ functional/
│  │  ├─ test_webhook_flow.py             # /webhook/meta (GET/POST + router)
│  │  └─ test_catalog_publish_flow.py     # CSV → Snapshot → Active
│  └─ integration/
│     └─ test_whatsapp_send_mock.py
│
├─ docs/                                  # documentación pública del repo
│  ├─ structure.md                        # ← ESTE DOCUMENTO
│  ├─ diagrams/
│  │  ├─ vision.md                        # arquitectura alta【56】
│  │  ├─ flow.md                          # secuencia conversación/ingesta【57】
│  │  └─ models.md                        # ER simplificado【58】
│  ├─ debug/
│  │  ├─ checklist.md                     # estado y métricas de avance【63】
│  │  └─ DEBUG_GENERAL.md                 # bitácora unificada【62】
│  └─ modules/
│     └─ skills.md                        # descripción de skills【55】
│
├─ .env.example                           # variables base (dev/staging/prod)
├─ docker-compose.yml                     # dev stack (web + db)
├─ Dockerfile                             # imagen de la API
├─ requirements.txt
├─ main.py
└─ README.md                              # índice de docs y cómo correr【59】

```
