# Liora – Visión (alto nivel)

```mermaid
graph TD
  subgraph Meta["Meta Cloud API (WABA único)"]
    MWebhook[(Webhook /webhook/meta)]
  end

  MWebhook --> LCore["Liora Core (Flask API)"]

  subgraph Core["Core abstracto"]
    Router[[Router conversacional]]
    Context["Context Engine (Cliente, Plan, Identidad)"]
    Policy[[Policies & Quotas]]
    Obs["Observabilidad (logs, métricas, alertas)"]
  end

  LCore --> Context
  LCore --> Router
  LCore --> Policy
  LCore --> Obs

  Router -->|elige skill| SK_Ecomm["Skill: Ecommerce"]
  Router -->|elige skill| SK_Vida["Skill: Vida Sana"]
  Router -->|elige skill| SK_Rec["Skill: Reciclaje (Enraiza)"]
  Router -->|elige skill| SK_Code["Skill: Código (interno/futuro)"]

  subgraph Services["Servicios internos"]
    WSvc[[whatsapp_service]]
    Bitly[[bitly_service]]
    CatSvc[[catalog_service]]
  end

  LCore --> WSvc
  LCore --> Bitly
  LCore --> CatSvc

  SK_Ecomm --> CatSvc
  SK_Ecomm --> Bitly
  SK_Ecomm --> WSvc

  SK_Vida --> WSvc
  SK_Rec --> WSvc
  SK_Code -. uso interno .-> WSvc

  subgraph Ext["Servicios externos opcionales"]
    Scraper[(Scraping Service)]
    VidaAPI[(Agente Vida Sana API)]
  end

  %% ✅ Evitamos label en la arista: nodo intermedio con el endpoint
  Endpoint["/clientes/{id}/catalog/publish"]
  Scraper --> Endpoint --> LCore

  SK_Vida --> VidaAPI

  subgraph DB["DB Multi-tenant"]
    Cliente[(Cliente)]
    Usuario[(Usuario)]
    Convo[(ConvoState)]
    CActive[(CatalogActive)]
    CSnap[(CatalogSnapshot)]
    Ingest[(IngestLog)]
    CLog[(ConversationLog)]
  end

  Context --> Cliente
  Context --> Usuario
  Router --> Convo
  CatSvc --> CActive
  CatSvc --> CSnap
  CatSvc --> Ingest
  WSvc --> CLog
