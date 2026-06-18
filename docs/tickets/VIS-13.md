# VIS-13 — Evaluación de servicio (web + móvil)

| Campo | Valor |
|---|---|
| Ticket | [VIS-13](https://linear.app/parrot-apps/issue/VIS-13/vis-13-evaluacion-de-servicio-web-movil) |
| Estado | Backlog |
| Prioridad | Medium |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-13` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Evaluación del cliente sobre el servicio completado, disponible en web y móvil. Se solicita tras finalizar la visita y sus datos alimentan la reportería (VIS-17).

## 2. Alcance
- **Incluye:** formulario de evaluación post-servicio con preguntas configurables; calificación de calidad; vínculo a visita, empleado/proveedor y cliente; datos disponibles para reportes.
- **No incluye:** el modelo exacto de preguntas/puntuación (pregunta abierta PRD §14); se implementa configurable.

## 3. Análisis técnico
Backend: router `/evaluations` (base en VIS-3) con creación vinculada a una visita completada; modelo de preguntas configurable. Web: `src/features/evaluation`. Móvil: `src/screens/Evaluation`, disparada al completar visita (VIS-18). El disparo se origina en la transición a Completed (VIS-10).

## 4. Plan de implementación
1. Backend: modelo de evaluación con preguntas configurables y `POST /evaluations` vinculado a visita/empleado/cliente.
2. Endpoint de lectura para reportes (VIS-17).
3. Web: formulario de evaluación.
4. Móvil: pantalla de evaluación, invocada tras completar la visita.
5. Integrar el disparo desde el cierre de visita (VIS-10/VIS-18).

## 5. Datos y migraciones
Usa Evaluation de VIS-3. Posible tabla de preguntas/configuración de evaluación si el modelo es dinámico.

## 6. i18n
Claves del formulario y preguntas por defecto (idioma base inglés).

## 7. Criterios de aceptación
- Los clientes evalúan servicios completados.
- Las evaluaciones se almacenan y son visibles para roles autorizados.
- La evaluación aparece en los datos de reportería.

## 8. Pruebas y verificación
Crear evaluación tras visita completada; impedir evaluación sin visita válida; verificar vínculos; aparición en reportes; permisos.

## 9. Riesgos y consideraciones
Las preguntas y el modelo de puntuación son pregunta abierta (PRD §14): implementar configurable para no rehacer. Definir si la evaluación es obligatoria u opcional.

## 10. Dependencias
Bloqueado por VIS-10. Alimenta VIS-17; consumido por VIS-18 (móvil).
