# VIS-10 — Agendamiento y ciclo de vida de visitas

| Campo | Valor |
|---|---|
| Ticket | [VIS-10](https://linear.app/parrot-apps/issue/VIS-10/vis-10-agendamiento-y-ciclo-de-vida-de-visitas) |
| Estado | Backlog |
| Prioridad | Urgent |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-10` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Diseño: `docs/web_screens` (Schedule Main). Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Módulo central del producto: creación, asignación y gestión del ciclo de vida de visitas, con su motor de estados en el backend. Toda transacción se almacena con marca de tiempo y geolocalización. Alimenta dashboard, mapa, financiero, reportes y la app móvil.

## 2. Alcance
- **Incluye:** crear/solicitar, asignar, iniciar, finalizar, cancelar visitas; registrar novedades; reglas automáticas de finalización olvidada; validación de transiciones; calendario (día/semana/mes/rango); filtros; APIs de calendario y disponibilidad.
- **No incluye:** UI de mapa (VIS-11), cálculos (VIS-16) ni la app móvil (VIS-18); aquí se exponen las APIs que esos consumen.

## 3. Análisis técnico
Backend: motor de estados en `app/services/scheduling.py` con máquina de estados (Requested → Pending assignment → Scheduled → In progress → Completed / Cancelled / Incident reported) que valida transiciones e impide saltos inválidos. Routers `/visits`, `/visits/{id}/start|finish|cancel|incidents`, `/schedule`, `/availability`. Cada transición escribe Visit Status Event con timestamp/geo y emite auditoría (VIS-4) y notificación (VIS-15). Worker en `app/workers` para auto-gestión de finalización olvidada. Web: `src/pages/Schedule` con calendario, panel de asignación y filtros.

## 4. Plan de implementación
1. Definir la máquina de estados y las transiciones válidas en `app/services/scheduling.py`.
2. Endpoints de ciclo de vida: crear, asignar, `start`, `finish`, `cancel`, `incidents`.
3. Persistir Visit Status Event (timestamp + geolocalización) en cada transición; emitir auditoría y notificación.
4. APIs de calendario (`/schedule`) con vistas día/semana/mes/rango y de disponibilidad (`/availability`) de empleados/proveedores.
5. Worker programado para reglas de finalización olvidada.
6. Web: vista de calendario con filtros (agendadas, sin agendar, todas, canceladas, en curso, finalizadas, disponibilidad de empleados/proveedores) y acciones de gestión.
7. Identificar visitas sin asignar y próximas a incumplimiento de SLA.

## 5. Datos y migraciones
Usa Visit, Visit Assignment, Visit Status Event, Visit Incident/Novelty de VIS-3. Confirmar enum de estados, campos de geolocalización/timestamp e índices por fecha/estado/empleado.

## 6. i18n
Claves de estados, acciones del calendario y filtros (idioma base inglés).

## 7. Criterios de aceptación
- Las visitas recorren los estados definidos; cada cambio es auditable.
- Las transiciones inválidas se rechazan.
- Los filtros del calendario devuelven resultados precisos.
- Web y móvil reciben estado de visita consistente.
- Se identifican visitas sin asignar y próximas a SLA.

## 8. Pruebas y verificación
Probar cada transición válida e inválida; persistencia de timestamp/geo; worker de auto-finalización; exactitud de filtros y disponibilidad; consistencia con móvil (VIS-18).

## 9. Riesgos y consideraciones
Módulo más complejo y central: priorizarlo. La geolocalización depende de permisos del dispositivo (PRD §14). Las reglas automáticas de finalización deben definirse con el negocio. Concurrencia en cambios de estado: usar transacciones.

## 10. Dependencias
Bloqueado por VIS-3, VIS-6, VIS-7, VIS-9. **Bloquea** VIS-5, VIS-11, VIS-13, VIS-14, VIS-15, VIS-16, VIS-17, VIS-18.
