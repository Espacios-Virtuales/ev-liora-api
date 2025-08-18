# 📂 Estructura del Proyecto

```
ev-liora-api/
├── app/
│   ├── models/
│   │   ├── waba_account.py      # NUEVO (sustituye numero_whatsapp.py)
│   │   ├── cliente.py           # NUEVO
│   │   ├── catalog_active.py    # NUEVO
│   │   ├── catalog_snapshot.py  # NUEVO
│   │   ├── convo_state.py       # NUEVO
│   │   ├── ingest_log.py        # NUEVO
│   │   ├── usuario.py
│   │   ├── membresia.py
│   │   ├── documento.py
│   │   ├── chat_model.py
│   ├── controllers/
│   │   ├── meta_webhook_controller.py  # RENOMBRAR desde wsp_controller.py
│   │   ├── chat_controller.py
│   │   ├── documento_controller.py
│   │   ├── membresia_controller.py
│   │   ├── user_controller.py
│   ├── services/
│   │   ├── core/        # context_service, router_service, policy_service
│   │   ├── skills/
│   │   │   ├── ecommerce_skill.py
│   │   │   ├── vida_sana_skill.py
│   │   │   ├── reciclaje_skill.py
│   │   │   └── codigo_skill.py (uso interno/futuro)
│   │   ├── whatsapp_service.py
│   │   ├── catalog_service.py    # NUEVO: snapshots + validadores + activo
│   │   ├── bitly_service.py      # NUEVO: UTM + short links
│   │   ├── nlp_service.py        # NUEVO: fallback GPT-4o mini (opcional)
│   │   ├── chat_service.py
│   │   ├── documento_service.py
│   │   ├── membresia_service.py
│   └── views/
│       ├── whatsapp_view.py
│       └── api_view.py
```
