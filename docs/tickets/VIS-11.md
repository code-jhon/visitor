# VIS-11 — Mapa de visitas (web)

| Campo | Valor |
|---|---|
| Ticket | [VIS-11](https://linear.app/parrot-apps/issue/VIS-11/vis-11-mapa-de-visitas-web) |
| Estado | Backlog |
| Prioridad | High |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-11` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Diseño: `docs/web_screens` (Map Main). Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Mapa en tiempo real con datos georeferenciados de visitas/pacientes. Módulo multiperfil y de alta complejidad técnica (la cuantificación lo marca como aumento de tiempo y costo). Se reutiliza como widget en el dashboard (VIS-5) y como base del mapa móvil (VIS-18).

## 2. Alcance
- **Incluye:** marcadores georeferenciados; tooltip/resumen por marcador; filtros por estado (agendadas, sin agendar, canceladas, novedades) y fecha (hoy/semana/mes); actualización en tiempo real donde sea viable.
- **No incluye:** heatmaps (mejora futura) ni el mapa móvil (VIS-18, que reutiliza la API).

## 3. Análisis técnico
Backend: endpoint `/map/visits` que devuelve solo datos autorizados para el usuario, con filtros de estado y rango de fecha, incluyendo timestamp y actor de cada registro de ubicación. Web: `src/features/map` con un proveedor de mapas (a definir: Google Maps / Mapbox / Leaflet — pregunta abierta PRD §14), capa de marcadores y panel de filtros. Refresco en tiempo/casi-real-time (polling o websockets).

## 4. Plan de implementación
1. Backend: `GET /map/visits` con filtros (estado, fecha) y control de acceso por rol.
2. Elegir proveedor de mapas e integrarlo en web.
3. Renderizar marcadores de pacientes/visitas con clustering si el volumen lo exige.
4. Tooltip/resumen al hacer clic en un marcador.
5. Panel de filtros por estado y fecha.
6. Mecanismo de actualización en tiempo real donde sea viable.
7. Exponer un modo "widget" para el dashboard (VIS-5).

## 5. Datos y migraciones
Usa coordenadas de Visit/Patient y registros de ubicación de Visit Status Event (VIS-3/VIS-10). Sin nuevas tablas, salvo índices geoespaciales si se requieren.

## 6. i18n
Claves de filtros y resumen de marcador (idioma base inglés).

## 7. Criterios de aceptación
- Los usuarios ven visitas/pacientes en el mapa según permisos.
- Los filtros actualizan correctamente los marcadores.
- Al hacer clic en un marcador se abre un resumen útil.
- El mapa solo devuelve datos autorizados para el solicitante.

## 8. Pruebas y verificación
Verificar filtrado por estado/fecha; control de acceso por rol; rendimiento con volumen esperado; refresco en tiempo real; clustering.

## 9. Riesgos y consideraciones
Mayor complejidad y costo (marcado en la cuantificación). El proveedor de mapas es pregunta abierta (PRD §14) y afecta costos/licencias. El rendimiento con muchos marcadores requiere clustering. La geolocalización depende de permisos.

## 10. Dependencias
Bloqueado por VIS-10. Reutilizado por VIS-5 y VIS-18.
