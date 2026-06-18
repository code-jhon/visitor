# VIS-9 — Módulo Configuración (servicios, subservicios, tarifas, certificados)

| Campo | Valor |
|---|---|
| Ticket | [VIS-9](https://linear.app/parrot-apps/issue/VIS-9/vis-9-modulo-configuracion-servicios-subservicios-tarifas-certificados) |
| Estado | Backlog |
| Prioridad | High |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-9` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Catálogos operativos que alimentan agendamiento, cálculos financieros y reportes: servicios, subservicios, tarifas (por servicio, proveedor, hora y kilómetro) y certificados/documentos requeridos. Define el modelo de tarifación del que dependen VIS-16 y VIS-17.

## 2. Alcance
- **Incluye:** CRUD de servicios y subservicios; CRUD de tarifas con sus cuatro modalidades; CRUD de certificados/documentos requeridos.
- **No incluye:** el cálculo financiero (VIS-16); aquí solo la configuración consumida.

## 3. Análisis técnico
Backend: routers `/services`, `/tariffs`, `/certificates` (base en VIS-3). Modelo de tarifa flexible que soporte modalidad (por servicio / proveedor / hora / km) y vigencia. Web: sección `src/pages/Configuration` con sub-vistas para cada catálogo en `src/features/configuration`.

## 4. Plan de implementación
1. Backend: definir/ajustar el modelo Tariff para las 4 modalidades y su relación con Service/Subservice/Provider.
2. CRUD de servicios y subservicios.
3. CRUD de tarifas por modalidad.
4. CRUD de certificados/documentos requeridos.
5. Web: pantallas de configuración con tablas y formularios por catálogo.
6. Asegurar que cambios se reflejan en agendamiento, financiero y reportes (sin caché obsoleta).

## 5. Datos y migraciones
Usa Service, Subservice, Tariff y Certificate/Document Requirement de VIS-3. Posible migración para campos de modalidad/vigencia de tarifa.

## 6. i18n
Claves de catálogos y formularios (idioma base inglés).

## 7. Criterios de aceptación
- Los cambios de configuración se reflejan en agendamiento, cálculos financieros y reportes.
- Solo usuarios autorizados (Admin, Empresa, Soporte) modifican la configuración.

## 8. Pruebas y verificación
CRUD de cada catálogo; verificar que una tarifa modificada impacta un cálculo de VIS-16; permisos por rol.

## 9. Riesgos y consideraciones
El modelo de tarifas es la base de la exactitud financiera: diseñarlo con vigencias para no romper liquidaciones históricas. Certificados próximos a vencer alimentan alertas (VIS-15).

## 10. Dependencias
Bloqueado por VIS-3. **Bloquea** VIS-10 (servicios/tarifas en solicitud), VIS-14, VIS-16, VIS-17.
