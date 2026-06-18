# VIS-5 — Dashboard operativo (web)

| Campo | Valor |
|---|---|
| Ticket | [VIS-5](https://linear.app/parrot-apps/issue/VIS-5/vis-5-dashboard-operativo-web) |
| Estado | Backlog |
| Prioridad | High |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-5` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Diseño: `docs/web_screens` (Main Content). Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Dashboard operativo principal de la web con visibilidad en tiempo real: indicadores, resumen de agenda, widget de mapa y accesos directos a visitas por estado. Es la pantalla de aterrizaje administrativa (Vista 1 de la propuesta).

## 2. Alcance
- **Incluye:** indicadores operativos clave; resumen de agenda; widget de mapa; accesos a visitas agendadas/activas/pendientes/canceladas/finalizadas; navegación a vistas detalladas.
- **No incluye:** el mapa completo (VIS-11) ni el detalle de cada módulo; aquí se consumen sus resúmenes.

## 3. Análisis técnico
Web (`apps/web`): página `src/pages/Dashboard.tsx`, widgets en `src/features/dashboard`, layout con sidebar (ver `docs/web_screens/Sidebar*.jpg`). Consume endpoints de resumen agregados desde el backend (`/dashboard/summary` a crear) y reutiliza el componente de mapa de VIS-11 en modo widget. Data-fetching con React Query y refresco periódico.

## 4. Plan de implementación
1. Backend: endpoint `GET /dashboard/summary` que agrega conteos por estado de visita, agenda del día y métricas clave, respetando permisos por rol.
2. Web: layout base con sidebar y navegación (compartido con el resto de módulos web).
3. Componentes de indicadores (tarjetas con conteos) y resumen de agenda.
4. Integrar el widget de mapa (VIS-11) en modo embebido.
5. Accesos directos que naveguen a Agendamiento (VIS-10) filtrado por estado.
6. Refresco en tiempo/casi-real-time (polling o websockets si se define).

## 5. Datos y migraciones
Sin cambios de esquema. Solo lectura agregada sobre visitas y agenda.

## 6. i18n
Claves para títulos de indicadores, estados y etiquetas del dashboard (idioma base inglés).

## 7. Criterios de aceptación
- Usuarios autorizados ven métricas resumen tras login.
- El dashboard refleja el estado actual de las visitas.
- Se navega desde los widgets a las vistas detalladas de cada módulo.

## 8. Pruebas y verificación
Verificar que los conteos coinciden con los datos de visitas; que los accesos directos filtran correctamente; comportamiento por rol; refresco de datos.

## 9. Riesgos y consideraciones
Depende del estado de visitas (VIS-10) y del mapa (VIS-11): pueden entregarse versiones progresivas (primero indicadores, luego mapa). El refresco en tiempo real añade complejidad; empezar con polling.

## 10. Dependencias
Bloqueado por VIS-2 y VIS-3. Se enriquece con VIS-10 y VIS-11.
