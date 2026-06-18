# VIS-15 — Mensajes, alertas y notificaciones

| Campo | Valor |
|---|---|
| Ticket | [VIS-15](https://linear.app/parrot-apps/issue/VIS-15/vis-15-mensajes-alertas-y-notificaciones) |
| Estado | Backlog |
| Prioridad | High |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-15` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Diseño: `docs/web_screens` (Sidebar). Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Canal de notificación y comunicación de eventos operativos (web + móvil). Genera alertas a partir de reglas, persiste mensajes y los entrega por bandeja web, notificación móvil y email donde esté configurado.

## 2. Alcance
- **Incluye:** alertas (servicios no asignados próximos a incumplimiento, impuestos próximos a pagar, citas canceladas, novedades, licencias/certificados por vencer); mensajes (solicitud, inicio, finalización de servicio); bandeja, estado leído/no leído, persistencia y auditabilidad; entrega web/móvil/email.
- **No incluye:** push nativo móvil completo (parte se aborda en VIS-18); aquí el backend de notificaciones y la bandeja web.

## 3. Análisis técnico
Backend: servicio `app/services/notifications.py` que genera notificaciones desde eventos (transiciones de visita en VIS-10, vencimientos de certificados en VIS-9, plazos de impuestos en VIS-16). Router `/notifications` con listar, marcar leído. Worker para reglas temporales (próximos a incumplir/vencer). Web: centro de notificaciones en el layout (sidebar). Integración de email donde esté configurado.

## 4. Plan de implementación
1. Backend: modelo/uso de Notification y Message (VIS-3); servicio generador de notificaciones.
2. Reglas de alerta: evaluadas por eventos y por worker programado (SLA, vencimientos, impuestos).
3. Router `/notifications`: listar por usuario/rol, marcar leído/no leído.
4. Integrar emisión desde VIS-10 (ciclo de visita), VIS-9 (certificados), VIS-14 (solicitudes), VIS-16 (impuestos).
5. Web: centro/bandeja de notificaciones con estado leído.
6. Canal email donde esté configurado; preparar contrato para push móvil (VIS-18).

## 5. Datos y migraciones
Usa Notification y Message de VIS-3. Índices por usuario/estado/fecha.

## 6. i18n
Plantillas de alertas y mensajes (idioma base inglés).

## 7. Criterios de aceptación
- Los usuarios reciben alertas relevantes según rol y permisos.
- Las alertas se almacenan y pueden marcarse como leídas.
- Las alertas operativas críticas son visibles en dashboard/centro de notificaciones.
- Los registros de notificación son consultables y auditables.

## 8. Pruebas y verificación
Disparar cada tipo de alerta/mensaje; verificar entrega por rol; marcar leído; reglas temporales del worker; entrega por email.

## 9. Riesgos y consideraciones
Las integraciones SMS/WhatsApp/email y la necesidad de push en MVP son preguntas abiertas (PRD §14). Evitar ruido de notificaciones (deduplicación, agrupación). Las reglas de plazos (impuestos, licencias) requieren datos de VIS-9/VIS-16.

## 10. Dependencias
Bloqueado por VIS-3 y VIS-10. Integra con VIS-9, VIS-14, VIS-16; consumido por VIS-18 (push).
