# VIS-3 — Modelo de datos y APIs de datos maestros

| Campo | Valor |
|---|---|
| Ticket | [VIS-3](https://linear.app/parrot-apps/issue/VIS-3/vis-3-modelo-de-datos-y-apis-de-datos-maestros) |
| Estado | Backlog |
| Prioridad | Urgent |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-3` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Define el modelo de datos relacional central (PostgreSQL) y las APIs CRUD de datos maestros. Es la base de consistencia entre web y móvil y el insumo de agendamiento, financiero, reportes y mapa.

## 2. Alcance
- **Incluye:** esquema relacional con migraciones versionadas y APIs CRUD para cada entidad maestra con validación y permisos por rol.
- **No incluye:** la lógica de negocio de cada módulo (estados de visita en VIS-10, cálculos en VIS-16, etc.). Aquí solo el modelo y el CRUD base.

## 3. Análisis técnico
Modelos en `app/db/models` (uno por entidad o agrupados por dominio), esquemas Pydantic en `app/schemas`, routers en `app/api/routers/<entidad>.py`, y servicios CRUD genéricos en `app/services`. Reutiliza la dependencia de permisos de VIS-2. `User`/`Role`/`Permission` ya existen de VIS-2; aquí se añade el resto.

## 4. Plan de implementación
1. Definir entidades (PRD §8.3): Employee, Client/Patient, Provider/Coordinator, Service, Subservice, Tariff, Certificate/Document Requirement, Visit, Visit Assignment, Visit Status Event, Visit Incident/Novelty, Service Request, Evaluation, Notification, Message, Report Request, Financial Liquidation, Audit Log, Support Ticket.
2. Crear modelos SQLAlchemy con relaciones e índices; migración Alembic única o por dominio.
3. Esquemas Pydantic (create/update/read) por entidad, con validación de campos requeridos.
4. Routers CRUD por grupo de API (PRD §8.4): `/employees`, `/clients`, `/patients`, `/providers`, `/services`, `/tariffs`, `/certificates`, y stubs de `/visits`, `/service-requests`, `/evaluations`, `/notifications` para que los tickets de negocio los completen.
5. Aplicar permisos por rol en cada router.
6. Pruebas de validación y de permisos.

## 5. Datos y migraciones
Crea la mayoría de tablas del sistema. Definir claves foráneas (p. ej. Visit → Client, Visit Assignment → Employee/Provider), enums de estado de visita (alineados con VIS-10) y campos de geolocalización/timestamp en Visit y Visit Status Event.

## 6. i18n
No aplica directamente al backend. Los nombres de campos visibles se traducen en web/móvil.

## 7. Criterios de aceptación
- Existen APIs CRUD para cada entidad maestra.
- Las APIs validan campos requeridos y aplican permisos de rol.
- El esquema mantiene integridad referencial y soporta escalado futuro.

## 8. Pruebas y verificación
Tests CRUD por entidad (crear/leer/actualizar/eliminar), validación de campos, y verificación de permisos por rol. Probar migraciones up/down.

## 9. Riesgos y consideraciones
Los campos exactos de cada entidad son pregunta abierta del PRD §14: modelar lo conocido y dejar extensibilidad. La eventual migración de datos del sistema actual (PRD §14) debe considerarse en el diseño.

## 10. Dependencias
Bloqueado por VIS-1 (y coordina con VIS-2 para `User`/`Role`). **Bloquea** a casi todos los módulos funcionales.
