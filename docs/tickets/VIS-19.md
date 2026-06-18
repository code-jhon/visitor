# VIS-19 — Soporte, ayuda contextual y sistema de tickets

| Campo | Valor |
|---|---|
| Ticket | [VIS-19](https://linear.app/parrot-apps/issue/VIS-19/vis-19-soporte-ayuda-contextual-y-sistema-de-tickets) |
| Estado | Backlog |
| Prioridad | Medium |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-19` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Capacidades transversales de soporte y ayuda: botón de ayuda por componente, búsqueda por criterios, soporte por email y un sistema de tickets entregado con la documentación del proyecto. También deja preparada la base de internacionalización.

## 2. Alcance
- **Incluye:** botón de ayuda por componente web (con imágenes/video); patrón de searchbox por criterios en los módulos principales; soporte por email; sistema de tickets de soporte (entidad Support Ticket, API `/support/tickets`); scaffolding i18n con idioma base inglés.
- **No incluye:** traducción a idiomas adicionales (futuro); la búsqueda se implementa como patrón reutilizable, no se rehace por módulo.

## 3. Análisis técnico
Backend: router `/support/tickets` (base en VIS-3) con CRUD y estados de ticket; envío por email. Web: componente reutilizable `HelpButton` y patrón `SearchBox` en `src/components`, consumidos por los módulos (VIS-6, VIS-7, VIS-8, VIS-10, VIS-16, VIS-17). i18n: consolidar el scaffolding de VIS-1 con claves base. Este ticket puede entregarse de forma incremental junto a cada módulo.

## 4. Plan de implementación
1. Backend: `/support/tickets` con creación, listado, cambio de estado; notificación/email a soporte.
2. Web: componente `HelpButton` reutilizable con soporte de imágenes/video.
3. Web: componente `SearchBox` parametrizable por criterios, adoptado por los módulos principales.
4. Canal de soporte por email.
5. i18n: estructura de claves base y guía para que cada módulo registre las suyas (idioma base inglés).
6. Documentar el sistema de tickets para entregarlo con la documentación del proyecto.

## 5. Datos y migraciones
Usa Support Ticket de VIS-3. Definir estados del ticket (abierto, en progreso, resuelto, cerrado) si no existen.

## 6. i18n
Este ticket establece el patrón i18n base (idioma inglés) reutilizado por todos los módulos.

## 7. Criterios de aceptación
- Cada componente web principal tiene botón de ayuda funcional.
- Los usuarios crean tickets de soporte y les dan seguimiento.
- La búsqueda devuelve resultados según criterios definidos por la empresa.

## 8. Pruebas y verificación
Verificar el botón de ayuda en varios módulos; crear y seguir un ticket de soporte; envío de email; búsqueda por criterios en módulos clave; cambio de idioma base.

## 9. Riesgos y consideraciones
Es transversal: coordinar su entrega incremental con cada módulo para evitar retrabajo. El contenido de ayuda (imágenes/video) requiere material del negocio. Los idiomas futuros son pregunta abierta (PRD §14).

## 10. Dependencias
Bloqueado por VIS-3. Transversal a todos los módulos web (provee `HelpButton` y `SearchBox`).
