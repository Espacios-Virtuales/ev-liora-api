# Liora – Modelo de datos (ER simplificado)

```mermaid
classDiagram
  class WabaAccount {
    +id: UUID
    +name: str
    +phone_number_id: str
    +access_token: str
    +created_at: datetime
    +updated_at: datetime
  }

  class Cliente {
    +id: UUID
    +slug: str
    +name: str
    +plan: str
    +waba_account_id: UUID
    +created_at: datetime
    +updated_at: datetime
  }

  class Usuario {
    +id: UUID
    +cliente_id: UUID
    +msisdn: str
    +name: str
    +created_at: datetime
  }

  class ConvoState {
    +id: UUID
    +cliente_id: UUID
    +waba_account_id: UUID
    +user_msisdn: str
    +last_intent: str
    +slots_json: json
    +context_json: json
    +updated_at: datetime
  }

  class CatalogActive {
    +id: UUID
    +cliente_id: UUID
    +version: str
    +rows_count: int
    +stock_pct: float
    +created_at: datetime
  }

  class CatalogSnapshot {
    +id: UUID
    +cliente_id: UUID
    +version: str
    +checksum: str
    +rows_count: int
    +source: str
    +created_at: datetime
  }

  class IngestLog {
    +id: UUID
    +cliente_id: UUID
    +snapshot_id: UUID
    +errors_json: json
    +divergences_json: json
    +metrics_json: json
    +created_at: datetime
  }

  class ConversationLog {
    +id: UUID
    +cliente_id: UUID
    +waba_account_id: UUID
    +user_msisdn: str
    +direction: str
    +intent: str
    +slots_json: json
    +message_type: str
    +message_body: text
    +link_ctrs_json: json
    +handoff: bool
    +created_at: datetime
  }

  %% Relaciones
  WabaAccount "1" --> "many" Cliente : sirve a
  Cliente "1" --> "many" Usuario : tiene
  Cliente "1" --> "1" CatalogActive : publica
  Cliente "1" --> "many" CatalogSnapshot : versiona
  CatalogSnapshot "1" --> "many" IngestLog : genera
  Cliente "1" --> "many" ConversationLog : registra
  Cliente "1" --> "many" ConvoState : guarda_estado
  WabaAccount "1" --> "many" ConvoState : por_waba

  %% Notas (en lugar de <<unique(...)>> o // comentarios)
  note for ConvoState "unique(user_msisdn, cliente_id)"
  note for CatalogActive "unique(cliente_id)"
  note for CatalogSnapshot "source: bitcommerce | scraper | manual"
  note for ConversationLog "direction: in | out"
