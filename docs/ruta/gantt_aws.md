# Gantt — Liora (Mermaid)

```mermaid
gantt
    title Liora — Gantt (MVP & Visión Completa)
    dateFormat  YYYY-MM-DD
    axisFormat  %b %d
    section MVP
    Router + persistir slots_json :core, 2025-08-25, 2d
    Seeds demo (Cliente/Usuario/WABA) :core, 2025-08-26, 1d
    Policy_service (MVP) :core, 2025-08-27, 2d
    Tests mínimos (catalog/bitly/webhook) :qa, 2025-08-29, 5d
    Docker/compose + healthchecks :devops, 2025-09-03, 2d
    Piloto 3–5 clientes :producto, 2025-09-05, 7d
    section Visión Completa
    AWS Deploy (staging/producción) :devops, 2025-09-12, 7d
    Observabilidad (métricas/alertas/backups) :devops, 2025-09-12, 7d
    CI/CD + escaneo dependencias :devops, 2025-09-19, 5d
    RBAC/JWT + auditoría :core, 2025-09-19, 5d
    Rate limiting & cost control :core, 2025-09-24, 3d
    Scraper microservicio :integrations, 2025-09-24, 15d
    Agente digital (memoria/tools/auto-eval) :ai, 2025-10-09, 21d
    Export/Insights + dashboard CTR :producto, 2025-10-15, 7d
    Documentación + runbooks :opsdev, 2025-10-22, 4d
```
