# VIS-6 — Módulo Empleados (web)

| Campo | Valor |
|---|---|
| Ticket | [VIS-6](https://linear.app/parrot-apps/issue/VIS-6/vis-6-modulo-empleados-web) |
| Estado | Backlog |
| Prioridad | High |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-6` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Diseño: `docs/web_screens` (Employee Main). Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Gestión de la información de empleados/cuidadores: datos personales, profesionales y de condiciones de contratación. Es insumo de agendamiento (disponibilidad) y del módulo financiero (liquidaciones).

## 2. Alcance
- **Incluye:** CRUD de empleados; datos personales/profesionales/contractuales; búsqueda y filtrado; asociación con agendas/visitas y disponibilidad.
- **No incluye:** la lógica de liquidación (VIS-16) ni de agendamiento (VIS-10); aquí se exponen los datos que aquellas consumen.

## 3. Análisis técnico
Backend: completar el router `/employees` (CRUD ya base en VIS-3) con búsqueda por criterios y endpoint de disponibilidad. Web: página `src/pages/Employees`, formulario y tabla en `src/features/employees`, searchbox (patrón de VIS-19), consumo vía `src/api`.

## 4. Plan de implementación
1. Backend: ampliar `/employees` con filtros de búsqueda (nombre, documento, estado, etc.) y `GET /employees/{id}/availability`.
2. Web: lista paginada con searchbox y filtros.
3. Formulario de alta/edición con secciones personal, profesional y contractual.
4. Acción de desactivar (no borrado físico) coherente con auditoría (VIS-4).
5. Validaciones de campos requeridos en cliente y servidor.

## 5. Datos y migraciones
Usa la entidad Employee de VIS-3. Si faltan campos profesionales/contractuales, añadir columnas vía migración.

## 6. i18n
Claves para etiquetas de formulario, columnas de tabla y mensajes (idioma base inglés).

## 7. Criterios de aceptación
- Usuarios con permiso crean, editan, ven y desactivan empleados.
- Los registros se buscan y filtran.
- La disponibilidad del empleado se usa durante el agendamiento.

## 8. Pruebas y verificación
CRUD completo; búsqueda/filtros; permisos por rol (Admin, Empresa, Empleado, Soporte); desactivación y su registro en auditoría.

## 9. Riesgos y consideraciones
Los campos exactos del empleado son pregunta abierta del PRD §14. La disponibilidad debe modelarse de forma consumible por VIS-10.

## 10. Dependencias
Bloqueado por VIS-3. **Bloquea** parcialmente VIS-10 (asignación/disponibilidad).
