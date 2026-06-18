# VIS-17 — Reportes y exportaciones

| Campo | Valor |
|---|---|
| Ticket | [VIS-17](https://linear.app/parrot-apps/issue/VIS-17/vis-17-reportes-y-exportaciones) |
| Estado | Backlog |
| Prioridad | High |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-17` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Generación de reportes operativos, financieros y de cumplimiento, con exportación a PDF, XLS, DOC y envío por email. Los datos deben coincidir exactamente con los registros operativos de origen.

## 2. Alcance
- **Incluye:** los 14 reportes del PRD §7.2.9; filtros por rango de fechas, empleado, proveedor, cliente, servicio, estado; exportación a PDF/XLS/DOC y email.
- **No incluye:** los cálculos financieros en sí (VIS-16); aquí se consumen y presentan.

## 3. Análisis técnico
Backend: motor de reportes en `app/services/reports.py` y router `/reports` + `/exports`. Cada reporte es una consulta parametrizada sobre datos de visitas (VIS-10), financiero (VIS-16), evaluaciones (VIS-13), empleados/clientes/proveedores. Exportadores a PDF/XLS/DOC y entrega por email. Web: `src/features/reports` con selección de reporte, filtros y descarga.

## 4. Plan de implementación
1. Backend: definir cada reporte como consulta parametrizada con filtros.
2. Reportes: horas pagadas por empleado; horas facturadas por proveedor; pensión por porcentaje; impuestos por empleado; horas por cliente; vacaciones; días de enfermedad; incidentes por cliente; facturación; ausentismo; lista de impuestos del gobierno; servicio periódico por cliente; servicios por cliente a cargo del proveedor; servicio periódico de clientes por proveedor.
3. Exportadores PDF/XLS/DOC y envío por email.
4. `GET /reports/{tipo}` y `POST /exports` (formato + filtros).
5. Web: pantalla de reportes con filtros y descarga/envío.
6. Validar que cada reporte cuadra con los registros de origen.

## 5. Datos y migraciones
Usa Report Request de VIS-3 para registrar generaciones. Sin nuevas tablas de negocio; principalmente lectura. Índices de apoyo según las consultas.

## 6. i18n
Claves de nombres de reportes, filtros y encabezados de exportación (idioma base inglés).

## 7. Criterios de aceptación
- Usuarios autorizados generan cada reporte por filtros/rango.
- Los reportes se exportan a PDF, XLS y DOC, y se envían por email.
- Los datos del reporte coinciden con los registros de origen.

## 8. Pruebas y verificación
Verificar cada reporte contra datos sembrados; exactitud de filtros; integridad de archivos exportados; envío por email; permisos.

## 9. Riesgos y consideraciones
Depende de VIS-16 para reportes financieros y de la calidad de los datos de visitas. El rendimiento de reportes grandes: considerar generación asíncrona. La lista de impuestos del gobierno puede requerir datos externos (pregunta abierta PRD §14).

## 10. Dependencias
Bloqueado por VIS-10 y VIS-16. Consume datos de VIS-6, VIS-7, VIS-8, VIS-13.
