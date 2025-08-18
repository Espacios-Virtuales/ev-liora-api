# ✅ Checklist Proceso de Desarrollo – Liora (Core + Skills)

## 1. Preparación y Base
- [ ] Revisar **estructura actual** de Liora Core (models, services, controllers, views).
- [ ] Configurar entorno `.env` con:
  - [ ] Base de datos
  - [ ] Token Meta API (WABA único)
  - [ ] Token Bitly
  - [ ] Secretos HMAC para snapshots
- [ ] Verificar migraciones y crear tablas base: `Cliente`, `Usuario`, `ConvoState`, `CatalogActive`, `CatalogSnapshot`, `IngestLog`, `ConversationLog`.

## 2. Integración Meta Cloud API
- [ ] Endpoint `GET /webhook/meta` (verificación token).
- [ ] Endpoint `POST /webhook/meta` (eventos de mensajes).
- [ ] Encolar evento fast/slow según plan.
- [ ] Integrar con `router_service`.

## 3. Skill Ecommerce
- [ ] Rutas informativas (FAQ, contacto).
- [ ] Catálogo con slot-filling (color, talla).
- [ ] Bitly + UTM en todos los enlaces.
- [ ] Derivación a humano con deep-link.

## 4. Gestión de Catálogo (Snapshots)
- [ ] Endpoint `POST /clientes/{id}/catalog/publish`.
- [ ] Validación HMAC, esquema de columnas.
- [ ] Versionado y checksum.
- [ ] Reemplazo atómico en `CatalogActive`.
- [ ] Validadores/normalizadores (colores, tallas).
- [ ] Rollback de versiones.

## 5. Skill Vida Sana
- [ ] Crear modelo base de planes/bitácoras (mente–cuerpo–alma).
- [ ] Implementar flujo de consultas simples (alimentación, hábitos).
- [ ] Registrar logs de intención y respuestas.
- [ ] Export de planes y recomendaciones por cliente.

## 6. Skill Reciclaje (Enraiza)
- [ ] Implementar módulo de rutas de reciclaje y prácticas sostenibles.
- [ ] Asociar datos de ciudad/cliente para recomendaciones.
- [ ] Export de métricas (ej: materiales recuperados, interacciones).

## 7. Skill Código (interno/futuro)
- [ ] Crear módulo de asistente técnico limitado.
- [ ] Restringir uso solo a administradores/equipo interno.
- [ ] Controlar consumo de tokens y latencia.

## 8. Métricas y Bitácoras
- [ ] Registrar conversaciones (intención, slots, CTR, derivaciones).
- [ ] Registrar snapshots (origen, versión, % stock, errores).
- [ ] Export `GET /clientes/{id}/export/excel`.

## 9. QA y Piloto
- [ ] Pruebas unitarias de servicios.
- [ ] Pruebas funcionales de Ecommerce y Vida Sana.
- [ ] Ingestión de snapshot real (CSV Bitcommerce).
- [ ] Test de derivación a humano.
- [ ] Piloto con 3–5 clientes.

## 10. Despliegue y Operación
- [ ] Hosting (container Flask + DB gestionada).
- [ ] Backups de DB y retención de logs.
- [ ] Monitoreo de latencia y uptime.
- [ ] Alertas: errores de ingestión, alta tasa de no-match.
- [ ] Plan de escalado y soporte.
