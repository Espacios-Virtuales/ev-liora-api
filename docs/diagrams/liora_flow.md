# Liora – Flujos principales (Conversación e Ingesta)

```mermaid
sequenceDiagram
  autonumber

  participant U as Usuario WhatsApp
  participant Meta as Meta Webhook
  participant Core as Liora Core
  participant Ctx as Context Engine
  participant St as ConvoState
  participant Rt as Router
  participant E as Ecommerce Skill
  participant V as Vida Sana Skill
  participant R as Reciclaje Skill
  participant W as whatsapp_service
  participant Cat as catalog_service
  participant DB as DB

  %% Conversación: texto entrante
  U->>Meta: Mensaje (texto)
  Meta->>Core: POST /webhook/meta
  Core->>Ctx: Resolver cliente/plan/identidad
  Ctx-->>Core: Contexto
  Core->>St: get_or_create(user_msisdn, cliente)
  St-->>Core: estado actual
  Core->>Rt: handle_incoming(evento, estado)

  alt intención catálogo
    Rt->>E: intent=catalogo.*
    E->>Cat: consultar CatalogActive
    Cat-->>E: productos/summary
    E->>W: send_text + links Bitly
  else intención vida sana
    Rt->>V: intent=vida_sana.*
    V->>W: recomendaciones/bitácora
  else intención reciclaje
    Rt->>R: intent=reciclaje.*
    R->>W: rutas/prácticas sostenibles
  else no-match
    Rt->>W: menú + ayuda
  end

  W-->>U: Respuesta WhatsApp
  Core->>DB: ConversationLog (in/out, intent, slots)

  %% Ingesta de Catálogo (push externo)
  participant Ext as Scraping/Bitcommerce
  Ext->>Core: POST /clientes/{id}/catalog/publish
  Core->>Cat: validar + snapshot + activar
  Cat->>DB: CatalogSnapshot + IngestLog + CatalogActive
  Cat-->>Core: OK
  Core-->>Ext: 200
