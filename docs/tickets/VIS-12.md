# VIS-12 — Detalle de paciente (web + móvil)

| Campo | Valor |
|---|---|
| Ticket | [VIS-12](https://linear.app/parrot-apps/issue/VIS-12/vis-12-detalle-de-paciente-web-movil) |
| Estado | Backlog |
| Prioridad | Medium |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-12` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Diseño: `docs/web_screens` (Detail Main) y `docs/app_screens`. Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Vista de información relevante del paciente, accesible desde web y móvil. El empleado la usa para recordar información vital antes y durante la visita. Respeta la visibilidad por rol de campos sensibles (VIS-4).

## 2. Alcance
- **Incluye:** resumen del paciente; información relevante de la visita; notas/instrucciones; visibilidad de campos sensibles por rol; versiones web y móvil.
- **No incluye:** edición del perfil (eso es VIS-7); aquí es principalmente lectura contextual.

## 3. Análisis técnico
Backend: endpoint `GET /patients/{id}/detail` con serialización por rol (VIS-4). Web: `src/features/patients/PatientDetail`. Móvil: `src/screens/PatientDetail` (consumido también desde VIS-18). Reutiliza datos de VIS-7 y se enlaza desde mapa (VIS-11) y agendamiento (VIS-10).

## 4. Plan de implementación
1. Backend: `GET /patients/{id}/detail` que devuelve resumen + datos de visita, filtrando campos sensibles según rol.
2. Web: componente de detalle con secciones de resumen, visita e instrucciones.
3. Móvil: pantalla equivalente, optimizada para consulta rápida antes de la visita.
4. Enlaces desde mapa y calendario al detalle.

## 5. Datos y migraciones
Sin cambios de esquema. Lectura sobre Client/Patient y Visit (VIS-3).

## 6. i18n
Claves de etiquetas del detalle (idioma base inglés), en web y móvil.

## 7. Criterios de aceptación
- Usuarios autorizados acceden al detalle del paciente.
- Los datos sensibles solo son visibles para roles con permiso.
- El empleado revisa rápidamente la información antes del servicio (móvil).

## 8. Pruebas y verificación
Verificar visibilidad por rol; consistencia de datos con VIS-7; navegación desde mapa/calendario; rendimiento en móvil.

## 9. Riesgos y consideraciones
Datos sensibles de salud: estricta aplicación de VIS-4 y marco legal (PRD §14). Definir qué campos son "relevantes antes de la visita".

## 10. Dependencias
Bloqueado por VIS-7. Reutilizado por VIS-18 (móvil), enlazado desde VIS-10 y VIS-11.
