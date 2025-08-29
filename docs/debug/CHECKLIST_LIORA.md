
# ✅ CHECKLIST — Liora (MVP vs Visión Completa)
**Actualizado:** 2025-08-20 21:36 UTC

> Este checklist consolida el estado operativo del **MVP (sin scraper ni agente)** y de la **Visión Completa**.  
> Las cifras son estimadas para planificación; se ajustan al cerrar cada hito.

---

## Resumen numérico
- **Avance MVP:** **80%**
```
[█████████████████████████████████████-------------------] 80%
```
- **Avance Visión Completa:** **54%**
```
[█████████████████████████-------------------------------] 54%
```

**Leyenda de estado**: ✅ Hecho · 🟡 En curso · ⏳ Pendiente · 🚫 Fuera del alcance (en esta visión)

---

## Matriz de estado por área
| Área | MVP | Visión Completa |
|---|---:|---:|
| Modelos + DB (UUID/JSONB, índices) | ✅ 100% | ✅ 100% |
| API/Controllers/Views/Init | ✅ 100% | ✅ 100% |
| Core (context, router, policy) | 🟡 70% | 🟡 60% |
| Integraciones (Meta verify/HMAC, Bitly) | 🟡 80% | 🟡 70% |
| Dominio Catálogo (publish/activate/checksum) | 🟡 85% | 🟡 85% |
| Skills base (ecommerce/vida/reciclaje) | 🟡 90% | 🟡 75% |
| Tests (unit/functional) | ⏳ 5% | ⏳ 5% |
| Despliegue & Operación (Docker/compose/AWS) | ⏳ 0% | ⏳ 0% |
| Observabilidad (métricas/alertas/backups) | ⏳ 0% | ⏳ 0% |
| Scraper microservicio | 🚫 N/A | ⏳ 0% |
| Agente digital | 🚫 N/A | ⏳ 0% |

---

## Checklist — MVP (sin scraper ni agente)
### Base
- [x] Estructura del repo (core/skills/integrations).
- [x] `.env` base y conexión a Postgres.
- [x] Migración inicial Alembic (UUID/JSONB) — rev `f07744c1193c`.
- [ ] Seeds demo: Cliente + Usuario owner + WABA (sandbox/mock).

### Integración Meta & Routing
- [x] `GET /webhook/meta` (verify).
- [x] `POST /webhook/meta` (firma HMAC verificada).
- [ ] Conectar `router_service` al POST webhook y persistir `slots_json` tras skill.
- [ ] `policy_service` (flags/quotas por plan) y guardas en endpoints/skills.

### Catálogo + Ecommerce
- [x] `catalog_service` publish/activate/get/list.
- [x] Validadores (talla/color) y `checksum`.
- [x] Bitly/UTM en enlaces.
- [ ] Rollback de versiones (opcional para MVP).

### Skills
- [x] `ecommerce` (resumen catálogo + links).
- [x] `vida_sana` (tips/bitácora mínima).
- [x] `reciclaje` (placeholder).

### QA y Piloto
- [ ] Tests unitarios mínimos: `catalog`, `bitly`, `webhook verify`.
- [ ] Tests funcionales mínimos: flujo `/catalogo`, `/vida`, `?` con mock WhatsApp.
- [ ] Ingesta snapshot real (CSV Bitcommerce).
- [ ] Piloto 3–5 clientes.

### Despliegue/Operación (MVP)
- [ ] Dockerfile + docker-compose (web + db).
- [ ] Healthchecks y runtime config.
- [ ] Logs básicos y rotación.

---

## Checklist — Visión Completa
Incluye todo el **MVP** más:
### Integración avanzada
- [ ] `policy_service` completo (planes, cuotas, límites de token).
- [ ] RBAC/JWT (roles) y auditoría de acciones.
- [ ] Rate limiting y control de costos por tenant.

### Scraper microservicio
- [ ] Diseño de colas de trabajo y permisos por cliente.
- [ ] Extracción de catálogo (WP/Bitcommerce/API), normalización y diffs.
- [ ] Publicación de snapshot y reconciliación con `CatalogActive`.
- [ ] Retries/backoff, timeouts y alertas.

### Agente digital
- [ ] Orquestación de skills externas (MCP/Tools si aplica).
- [ ] Memoria conversacional extendida y políticas de privacidad.
- [ ] Evaluación automática de respuestas (auto‑eval) y fallback.

### Observabilidad & Fiabilidad
- [ ] Métricas (requests, errores, latencia, CTR/no‑match) por tenant.
- [ ] Alertas (ingestas fallidas, picos de no‑match, 5xx).
- [ ] Backups/retención de datos y restauración.
- [ ] Trazabilidad (request id, correlación de eventos).

### Despliegue & Operación
- [ ] Infra de staging y producción en AWS (EC2/ECS/RDS).
- [ ] CI/CD (build, test, deploy) y escaneo de dependencias.
- [ ] Gestión de secretos (SSM/KMS) y rotación.
- [ ] Plan de escalado y SLOs.

### Experiencia & Producto
- [ ] Export/Insights (`/clientes/<built-in function id>/export` y dashboard CTR).
- [ ] Documentación pública y runbooks (operación/incidentes).
- [ ] Internacionalización (i18n) y performance (caching, N+1).

---

## Próximos pasos sugeridos (orden ejecutable)
1) Conectar `router_service` + persistir `slots_json`.  
2) Implementar `policy_service` mínimo viable.  
3) Sembrado demo y **tests mínimos**.  
4) Docker/compose + healthchecks.  
5) Piloto con 3–5 clientes y medición de CTR/no‑match.

> Este checklist sustituye versiones previas; mantenerlo como **fuente única** junto con `DEBUG_GENERAL.md`.
