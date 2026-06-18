# VIS-8 — Módulo Proveedor/Coordinador (web)

| Campo | Valor |
|---|---|
| Ticket | [VIS-8](https://linear.app/parrot-apps/issue/VIS-8/vis-8-modulo-proveedorcoordinador-web) |
| Estado | Backlog |
| Prioridad | Medium |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-8` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Diseño: `docs/web_screens` (Provider Main). Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Gestión de proveedores y coordinadores que participan en la prestación del servicio: datos personales, profesionales y contractuales. Insumo de agendamiento y reportes.

## 2. Alcance
- **Incluye:** CRUD de proveedores/coordinadores; datos personales/profesionales/contractuales; asociación con visitas o clientes cuando aplique; búsqueda y filtrado.
- **No incluye:** liquidación a proveedores (VIS-16) ni asignación de visitas (VIS-10); aquí se exponen los datos.

## 3. Análisis técnico
Backend: completar router `/providers` (base en VIS-3) con búsqueda. Web: página `src/pages/Providers`, formulario/tabla en `src/features/providers`, searchbox. Análogo a VIS-6 en estructura.

## 4. Plan de implementación
1. Backend: ampliar `/providers` con filtros de búsqueda.
2. Web: lista con searchbox; formulario de alta/edición.
3. Asociación opcional con clientes/visitas.
4. Desactivación lógica con auditoría.
5. Validaciones cliente/servidor.

## 5. Datos y migraciones
Usa la entidad Provider/Coordinator de VIS-3. Añadir columnas faltantes vía migración.

## 6. i18n
Claves de formulario y tabla (idioma base inglés).

## 7. Criterios de aceptación
- Usuarios autorizados crean, actualizan, ven y desactivan proveedores/coordinadores.
- Los registros se usan en agendamiento y reportes.

## 8. Pruebas y verificación
CRUD; búsqueda; permisos (Admin, Empresa, Proveedor/Coordinador, Soporte); desactivación y auditoría.

## 9. Riesgos y consideraciones
Campos exactos pendientes (PRD §14). Definir qué relación proveedor↔cliente/visita aplica al negocio.

## 10. Dependencias
Bloqueado por VIS-3. Relacionado con VIS-10 y VIS-17.
