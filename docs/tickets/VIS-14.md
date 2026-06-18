# VIS-14 — Solicitud de servicio (web + móvil)

| Campo | Valor |
|---|---|
| Ticket | [VIS-14](https://linear.app/parrot-apps/issue/VIS-14/vis-14-solicitud-de-servicio-web-movil) |
| Estado | Backlog |
| Prioridad | High |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-14` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Flujo guiado paso a paso para solicitar un servicio, con principios de usabilidad. Disponible en web y móvil, incluso para clientes sin cita o potencialmente no registrados (sujeto a reglas de negocio). Las solicitudes entran a la cola de agendamiento.

## 2. Alcance
- **Incluye:** formulario paso a paso; solicitud por clientes registrados; solicitud por no agendados/no registrados según reglas; mostrar servicios y tarifas configurados (VIS-9); notificación a empresa/admin; confirmación al usuario.
- **No incluye:** la asignación/agenda de la solicitud (VIS-10), solo su creación e ingreso a la cola.

## 3. Análisis técnico
Backend: router `/service-requests` (base en VIS-3) que crea una Service Request, dispara notificación (VIS-15) y la pone en la cola de agendamiento (VIS-10). Web: `src/features/service-request` (wizard multistep). Móvil: `src/screens/ServiceRequest`. Consume catálogos de VIS-9.

## 4. Plan de implementación
1. Backend: `POST /service-requests` con validación; reglas para clientes no registrados; creación de notificación a empresa/admin.
2. Vincular la solicitud a la cola de agendamiento (estado Requested en VIS-10).
3. Web: wizard paso a paso (selección de servicio/subservicio, datos de contacto/paciente, confirmación) mostrando tarifas.
4. Móvil: flujo equivalente.
5. Pantalla/estado de confirmación.

## 5. Datos y migraciones
Usa Service Request de VIS-3. Confirmar campos para clientes no registrados (contacto, datos mínimos).

## 6. i18n
Claves del wizard, pasos y confirmación (idioma base inglés).

## 7. Criterios de aceptación
- Los usuarios envían una solicitud mediante el flujo guiado.
- Las solicitudes aparecen en agendamiento/cola de trabajo.
- El usuario recibe confirmación tras enviar.

## 8. Pruebas y verificación
Enviar solicitud como cliente registrado y no registrado; verificar notificación y aparición en cola; mostrar tarifas correctas; confirmación; permisos.

## 9. Riesgos y consideraciones
Las reglas para clientes no registrados son sensibles (anti-spam, validación). Las tarifas mostradas dependen de VIS-9. Definir el límite entre "solicitud" y "creación de cliente".

## 10. Dependencias
Bloqueado por VIS-9 y VIS-10. Genera notificaciones (VIS-15); consumido por VIS-18 (móvil).
