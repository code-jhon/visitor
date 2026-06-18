# VIS-18 — Aplicación móvil (login, ejecución de visita, mapa, notificaciones)

| Campo | Valor |
|---|---|
| Ticket | [VIS-18](https://linear.app/parrot-apps/issue/VIS-18/vis-18-aplicacion-movil-login-ejecucion-de-visita-mapa-notificaciones) |
| Estado | Backlog |
| Prioridad | Urgent |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-18` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Diseño: `docs/app_screens` (Mobile App Screens). Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
App móvil React Native (Android + iOS) para operación de campo y clientes. Hace simple la ejecución de visitas para empleados (inicio/fin con geolocalización) y habilita a clientes a solicitar y evaluar servicios. Reutiliza VIS-12 (detalle), VIS-13 (evaluación) y VIS-14 (solicitud) en su entorno móvil y el API de mapa de VIS-11.

## 2. Alcance
- **Incluye:** login y home por rol; almacenamiento seguro de token; mapa de visitas con filtros; gestión de visita (detalle, iniciar/finalizar con timestamp+geo, novedades, disparo de evaluación); notificaciones (bandeja, leído, push donde aplique); manejo de errores GPS/red.
- **No incluye:** modo offline-first (fuera de alcance PRD §5); módulos administrativos web.

## 3. Análisis técnico
Móvil (`apps/mobile`): navegación por rol en `src/navigation`, pantallas en `src/screens` (Login, Home, Map, VisitDetail, PatientDetail, Evaluation, ServiceRequest, Notifications), estado en `src/store`, cliente HTTP en `src/api`. Consume `/auth` (VIS-2), `/visits/*` y `/schedule` (VIS-10), `/map/visits` (VIS-11), `/patients/{id}/detail` (VIS-12), `/evaluations` (VIS-13), `/service-requests` (VIS-14), `/notifications` (VIS-15). Geolocalización con permisos del dispositivo; almacenamiento seguro de token (SecureStore/Keychain). Push con FCM/APNs donde se defina.

## 4. Plan de implementación
1. Login seguro, persistencia de sesión y home por rol.
2. Mapa de visitas asignadas/visibles (reutiliza API de VIS-11) con filtros por estado y fecha.
3. Gestión de visita: detalle, iniciar/finalizar con un botón capturando timestamp + geolocalización, registrar novedades.
4. Disparo del flujo de evaluación (VIS-13) al completar la visita.
5. Pantallas de detalle de paciente (VIS-12) y solicitud de servicio (VIS-14) en móvil.
6. Bandeja de notificaciones (VIS-15) con marcar leído y push donde la plataforma lo permita.
7. Manejo de errores cuando GPS/red no estén disponibles; almacenamiento seguro de tokens.

## 5. Datos y migraciones
Sin cambios de esquema propios; consume las APIs existentes. Confirmar que `start`/`finish` aceptan coordenadas y timestamp del dispositivo (VIS-10).

## 6. i18n
Reutiliza el scaffolding i18n móvil (idioma base inglés) para todas las pantallas.

## 7. Criterios de aceptación
- El usuario ve solo módulos apropiados a su rol.
- El empleado inicia y finaliza una visita desde móvil; el estado se refleja en la web.
- Los eventos de inicio/fin incluyen timestamp y geolocalización cuando hay permisos.
- Las notificaciones se reciben y su estado sincroniza con el backend.

## 8. Pruebas y verificación
Probar en Android e iOS: login/persistencia; inicio/fin con y sin permiso de GPS; consistencia de estado con web; recepción de notificaciones/push; manejo de pérdida de red.

## 9. Riesgos y consideraciones
Permisos de GPS e inestabilidad de red afectan la trazabilidad (PRD §14). El push en MVP y las integraciones de mensajería son preguntas abiertas. Sin modo offline (excluido): definir el comportamiento ante red intermitente. Ticket grande: puede subdividirse en sub-tareas de implementación si se requiere.

## 10. Dependencias
Bloqueado por VIS-2, VIS-10, VIS-15. Reutiliza VIS-11, VIS-12, VIS-13, VIS-14.
