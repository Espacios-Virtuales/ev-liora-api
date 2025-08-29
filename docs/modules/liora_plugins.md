# 🤖 Liora & Plugins (WhatsApp Bot Microservice)

Microservicio modular y **extensible por plugins** para gestionar múltiples clientes a través de un único número de WhatsApp (Meta API).  
Es la **base abstracta** del ecosistema, capaz de enrutar mensajes, aplicar políticas según plan/cliente y activar las extensiones (plugins) correspondientes.

Parte del ecosistema **Espacios Virtuales**.

---

## 🚀 Características

- Conexión a **Meta Cloud API** con soporte multi-tenant (un WABA único, múltiples clientes).
- **Core abstracto**:
  - Webhook Meta (GET/POST `/webhook/meta`)
  - Context Engine (Cliente, Plan, Identidad, Límites)
  - Capability Router (elige plugin)
  - Policies & Quotas (rate, tokens, features por plan)
  - Observabilidad (logs, métricas, alertas)
- **Plugins internos** activados por identidad/plan:
  - 📲 **Ecommerce** → catálogo activo, Bitly/UTM, slot-filling.
  - 🌱 **Vida Sana** → hábitos saludables, alimentación, bitácoras de mente–cuerpo–alma.
  - ♻️ **Reciclaje** → extensión de Vida Sana para Enraiza (rutas y prácticas sostenibles).
  - 💻 **Código** → asistente técnico, **uso interno y a futuro**.
- **Servicios externos desacoplados**:
  - **Scraping Service** → genera snapshots de catálogos y los publica en `/clientes/{id}/catalog/publish`.
  - **Agente Digital** (opcional) → vector DB para enriquecer consultas de Vida Sana.

---

## 🧱 Estructura

```
ev-liora-api/
├── app/
│   ├── config.py
│   ├── __init__.py
│   ├── extensions.py
│   ├── models/
│   ├── controllers/
│   ├── services/
│   │   ├── core/        # context_service, router_service, policy_service
│   │   ├── integrations/
│   │   │   ├── whatsapp_service.py
│   │   │   ├── bitly_service.py
│   │   │   └── catalog_service.py
│   └── views/
│       ├── api_view.py
│       └── whatsapp_view.py
├── plugins/
│   ├── ecommerce/
│   │   ├── plugin.py
│   │   └── manifest.json
│   ├── vida_sana/
│   │   ├── plugin.py
│   │   └── manifest.json
│   └── reciclaje/
│       ├── plugin.py
│       └── manifest.json
├── main.py
├── requirements.txt
└── README.md
```

---

## 📌 Plan de Desarrollo

1. **Core abstracto** (Webhook, Context, Router, Policies).  
2. **Plugin Ecommerce** (catálogo + Bitly).  
3. **Webhook publish** para snapshots.  
4. **Plugin Vida Sana** (hábitos, planes, bitácora).  
5. **Plugin Reciclaje** (integración Enraiza).  
6. **Plugin Código** (uso interno/futuro).  
7. QA, métricas, piloto multi-cliente.

---

## 🧙‍♂️ Autores

Equipo **Espacios Virtuales**  
Parte del ecosistema de microservicios conscientes y modulares.
