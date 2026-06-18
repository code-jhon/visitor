# VIS-4 — Auditoría, seguridad y protección de datos

| Campo | Valor |
|---|---|
| Ticket | [VIS-4](https://linear.app/parrot-apps/issue/VIS-4/vis-4-auditoria-seguridad-y-proteccion-de-datos) |
| Estado | Backlog |
| Prioridad | High |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-4` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Capacidades transversales de auditoría y protección de datos sensibles de salud. Crítico por el manejo de información de pacientes y por el requisito de trazabilidad del PRD.

## 2. Alcance
- **Incluye:** registro de auditoría de cambios de datos y eventos de ciclo de vida de visita; cifrado en tránsito y en reposo de datos sensibles; mínimo privilegio; validación/saneamiento de entradas; visibilidad de campos sensibles por rol; backups restaurables.
- **No incluye:** definición del modelo Audit Log (lo crea VIS-3) ni el RBAC base (VIS-2); aquí se implementa el mecanismo que los usa.

## 3. Análisis técnico
Middleware/servicio de auditoría en `app/services/audit.py` que intercepta operaciones de escritura y eventos de visita, escribiendo en la tabla `audit_log` (actor, timestamp, acción, entidad, antes/después, geolocalización). Capa de serialización por rol en los esquemas Pydantic para ocultar campos sensibles. Configuración de TLS y cifrado en reposo a nivel de infraestructura (RDS/S3, coordinar con VIS-1).

## 4. Plan de implementación
1. `app/services/audit.py`: helper para emitir registros de auditoría desde servicios y routers; integrarlo en operaciones de escritura críticas y en transiciones de visita (VIS-10).
2. Garantizar inmutabilidad de `audit_log` (sin update/delete por usuarios normales; solo lectura para Admin/Soporte) vía permisos.
3. Serialización por rol: utilidades de esquema que filtran campos sensibles de paciente según el rol del solicitante.
4. Validación/saneamiento centralizado de entradas (Pydantic + sanitización adicional donde haya texto libre/HTML).
5. Configurar cifrado en reposo (RDS, S3) y forzar TLS extremo a extremo (con VIS-1).
6. Endpoint de consulta de auditoría para Admin/Soporte con filtros (entidad, actor, rango de fechas).
7. Verificar política de backups restaurables.

## 5. Datos y migraciones
Usa la tabla `audit_log` de VIS-3. Posibles índices por entidad, actor y fecha para consulta eficiente.

## 6. i18n
Etiquetas de la vista de auditoría (idioma base inglés).

## 7. Criterios de aceptación
- Admin/Soporte pueden trazar eventos operativos y de datos.
- Los endpoints sensibles requieren autenticación.
- Los campos sensibles no se exponen a roles sin permiso.
- Los registros de auditoría no pueden ser modificados por usuarios normales.

## 8. Pruebas y verificación
Verificar que una escritura genera registro de auditoría con antes/después; que un rol sin permiso no ve campos sensibles; que `audit_log` rechaza modificación; restaurar un backup en entorno aislado.

## 9. Riesgos y consideraciones
El marco legal (HIPAA u otro, PRD §14) puede exigir controles adicionales de retención, consentimiento y notificación de brechas. La auditoría no debe degradar el rendimiento: considerar escritura asíncrona. Parte del hardening pertenece a la Entrega 3.

## 10. Dependencias
Bloqueado por VIS-2 y VIS-3. Se integra con VIS-10 (eventos de visita) y con la infraestructura de VIS-1.
