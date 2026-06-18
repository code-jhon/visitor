# VIS-16 — Módulo financiero / liquidaciones

| Campo | Valor |
|---|---|
| Ticket | [VIS-16](https://linear.app/parrot-apps/issue/VIS-16/vis-16-modulo-financiero-liquidaciones) |
| Estado | Backlog |
| Prioridad | High |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-16` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Motor de liquidaciones y cálculos financieros. Usa la configuración de tarifas (VIS-9) y los registros de visitas (VIS-10) como insumos. Las salidas alimentan reportes (VIS-17). Requiere reglas legales/de negocio precisas.

## 2. Alcance
- **Incluye:** horas laboradas por rango de fechas y tipo de contrato; pensión por porcentaje legal (ref. 9.5%); vacaciones; incapacidades; auxilio de rodamiento/transporte (por km); empleados persona natural; horas facturables.
- **No incluye:** integraciones de pago/gobierno (fuera de alcance PRD §5); aquí solo cálculo y trazabilidad.

## 3. Análisis técnico
Backend: motor en `app/services/financial.py` con cálculos reproducibles y trazables; router `/financial/liquidations`. Inputs: Visit Status Event (horas reales), Tariff (VIS-9), tipo de contrato del empleado (VIS-6). Persistir Financial Liquidation con sus inputs/outputs para reproducibilidad. Web: `src/features/financial` para generar y consultar liquidaciones por rango.

## 4. Plan de implementación
1. Definir, con el negocio, las fórmulas exactas (pregunta abierta PRD §14): horas, pensión, vacaciones, incapacidades, rodamiento.
2. Backend: implementar cada cálculo como función pura y testeable.
3. `POST /financial/liquidations` por rango de fechas y empleado/tipo de contrato; persistir inputs y outputs.
4. Trazabilidad: enlazar cada resultado a visitas/horas/configuración de origen.
5. Web: pantalla de generación de liquidaciones y consulta.
6. Exponer salidas a reportes (VIS-17) y plazos de impuestos a alertas (VIS-15).

## 5. Datos y migraciones
Usa Financial Liquidation de VIS-3. Añadir tablas/campos para guardar parámetros de cálculo (porcentajes, vigencias) y el detalle de inputs.

## 6. i18n
Claves de conceptos financieros y pantallas (idioma base inglés).

## 7. Criterios de aceptación
- Usuarios autorizados generan liquidaciones por rango de fechas.
- Los cálculos son reproducibles y trazables a su origen.
- Las entradas y salidas se almacenan o registran.
- Las salidas alimentan reportes y exportaciones.

## 8. Pruebas y verificación
Tests unitarios de cada fórmula con casos conocidos; reproducibilidad (mismo input → mismo output); trazabilidad a visitas; verificación contra ejemplos del negocio.

## 9. Riesgos y consideraciones
Las fórmulas exactas de impuestos, pensiones, vacaciones, incapacidades y rodamiento son pregunta abierta crítica (PRD §14): no implementar sin confirmarlas. Cambios de tarifa con vigencia no deben alterar liquidaciones pasadas. Precisión monetaria (usar decimales, no float).

## 10. Dependencias
Bloqueado por VIS-9 y VIS-10. Alimenta VIS-17 y VIS-15.
