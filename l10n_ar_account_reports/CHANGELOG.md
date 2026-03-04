# Changelog — l10n_ar_account_reports

Todas las versiones siguen [Semantic Versioning](https://semver.org/) con el prefijo de versión de Odoo (`14.0.x.y.z`).

---

## [14.0.1.1.0] — 2026-03-04

### Cambiado
- Bump de versión para registrar el estado actual del módulo y habilitar la creación del changelog.

---

## [14.0.1.0.0] — (inicial)

### Agregado

#### Reporte de impuestos genérico (Tax Report)
- Extensión de `account.generic.tax.report` para soportar los tipos de impuesto propios de Argentina (`customer` / `supplier`) además de los estándar de Odoo (`sale` / `purchase`).
- Filtrado de impuestos tipo `none` (no se incluyen en el reporte).
- Soporte de impuestos agrupados con hijos indentados (3 espacios).
- Aplicación de signo correcto: −1 para ventas, +1 para compras.
- Soporte de comparación de períodos (2 columnas por período: base neta e impuesto).

#### Dashboard de diarios — Balance en Libro Mayor
- Extensión de `account.journal` con método `action_general_ledger()`.
- Reemplazo del vínculo "Balance in GL" en la vista kanban de diarios tipo Banco/Efectivo.
- Filtrado automático del Libro Mayor por la cuenta de pago cuando el diario tiene la misma cuenta de débito y crédito configurada.

#### Formato de nombres en reportes contables
- Extensión de `account.report` con `_format_aml_name()`.
- Evita duplicar información cuando el nombre de la línea coincide con el nombre o referencia del asiento.
- Trunca a 32 caracteres + "…" cuando la cadena supera 35 caracteres (respeta flag `no_format`).

#### Reporte "Cheques a Fecha"
- Wizard `account.check.to_date.report.wizard` con campos:
  - `to_date` (Hasta Fecha, requerido, por defecto hoy).
  - `journal_id` (Diario, opcional — filtra cheques propios o de terceros).
- Distingue dos categorías de cheques pendientes:
  - **Cheques propios** (estado `handed`): emitidos y entregados, aún no cobrados.
  - **Cheques de terceros** (estado `holding`): recibidos, aún no depositados.
- Reporte QWeb-PDF con dos secciones:
  - *Cheques propios*: número, fecha contable, fecha de pago, empresa, chequera, importe.
  - *Cheques de terceros*: número, fecha contable, fecha de pago, CUIT emisor, importe.
  - Totales por sección y título dinámico con la fecha de corte.
- Menú: **Contabilidad → Reportes → Estados Legales → Cheques a Fecha** (secuencia 20).
- Template ODT asociado (Aeroo) para generación alternativa.
