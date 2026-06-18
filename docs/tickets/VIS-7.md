# VIS-7 — Módulo Clientes/Pacientes (web)

| Campo | Valor |
|---|---|
| Ticket | [VIS-7](https://linear.app/parrot-apps/issue/VIS-7/vis-7-modulo-clientespacientes-web) |
| Estado | Backlog |
| Prioridad | High |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-7` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Diseño: `docs/web_screens` (Patient Main). Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Gestión de registros de clientes/pacientes y visibilidad de su agendamiento. Maneja datos sensibles de salud, sujetos a visibilidad por rol (VIS-4).

## 2. Alcance
- **Incluye:** CRUD de clientes/pacientes; perfil del paciente; calendario de visitas e historial de estados; búsqueda; vinculación con visitas.
- **No incluye:** el detalle clínico completo (VIS-12) ni el motor de agendamiento (VIS-10); aquí se muestra la visibilidad del calendario.

## 3. Análisis técnico
Backend: completar router `/clients` y `/patients` (base en VIS-3) con búsqueda y endpoint de calendario del paciente. Web: página `src/pages/Patients`, formulario/tabla en `src/features/patients`, vista de calendario por paciente que consume estado de visitas (VIS-10). Aplicar serialización por rol de campos sensibles (VIS-4).

## 4. Plan de implementación
1. Backend: ampliar `/clients`/`/patients` con filtros de búsqueda y `GET /patients/{id}/calendar`.
2. Web: lista con searchbox; formulario de alta/edición de perfil.
3. Vista de calendario del paciente con estados de visita.
4. Desactivación lógica y registro en auditoría.
5. Aplicar visibilidad por rol a campos sensibles.

## 5. Datos y migraciones
Usa la entidad Client/Patient de VIS-3. Añadir columnas de perfil que falten vía migración.

## 6. i18n
Claves para formulario, calendario y estados (idioma base inglés).

## 7. Criterios de aceptación
- Usuarios autorizados gestionan información de pacientes.
- Los registros se vinculan a visitas.
- El calendario muestra el estado correcto de cada visita.
- Los campos sensibles solo son visibles a roles con permiso.

## 8. Pruebas y verificación
CRUD; búsqueda; calendario refleja estados reales; permisos (Admin, Empresa, Empleado, Cliente, Soporte); visibilidad de campos sensibles.

## 9. Riesgos y consideraciones
Datos sensibles de salud: cumplir VIS-4 y el marco legal aplicable (PRD §14). Los campos exactos del paciente son pregunta abierta.

## 10. Dependencias
Bloqueado por VIS-3. Relacionado con VIS-10 (calendario), VIS-12 (detalle).
