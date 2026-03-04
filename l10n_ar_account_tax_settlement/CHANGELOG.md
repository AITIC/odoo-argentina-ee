# Changelog — l10n_ar_account_tax_settlement

Todas las versiones siguen [Semantic Versioning](https://semver.org/) con el prefijo de versión de Odoo (`14.0.x.y.z`).

---

## [14.0.1.2.0] — (actual)

### Agregado
- Nuevo tipo de liquidación `iibb_aplicado_arba_desde_01032026`: formato ARBA actualizado obligatorio a partir del 1° de marzo de 2026.
- Nuevo tipo `iibb_aplicado_arba_act_7_desde_01032026`: variante para Actividad 7 con el mismo formato actualizado.
- Métodos `iibb_aplicado_arba_desde_01032026_files_values()` para generación de TXT en el nuevo esquema ARBA.

---

## [14.0.1.1.0]

### Agregado
- Soporte para **DGR Mendoza** (`iibb_aplicado_dgr_mendoza`): generación de TXT de percepciones/retenciones para la provincia de Mendoza.
- Método `iibb_aplicado_dgr_mendoza_files_values()`.

---

## [14.0.1.0.0]

### Agregado
- Versión inicial para Odoo 14.
- Exportación TXT para **SICORE** (`sicore_aplicado`).
- Exportación TXT para **SIFERE** (`iibb_sufrido`).
- Exportación TXT para **ARBA** percepciones/retenciones (`iibb_aplicado`).
- Exportación TXT para ARBA **Actividad 7** quincenal (`iibb_aplicado_act_7`).
- Exportación TXT para **AGIP** CABA (`iibb_aplicado_agip`).
- Exportación TXT para **API** Santa Fe (`iibb_aplicado_api`).
- Exportación TXT para **SIRCAR** Córdoba (`iibb_aplicado_sircar`).
- Wizard de **Ajuste por Inflación** (`inflation.adjustment`) con cálculo de REI mensual.
- Modelo `inflation.adjustment.index` para gestión de índices de precios mensuales.
- Índices precargados desde enero 2013 hasta febrero 2021 (base diciembre 2016 = 100).
- Creación automática de diarios de liquidación al instalar el plan de cuentas argentino.
- Validación de módulo `account_withholding_automatic` para tipos que requieren retenciones automáticas.
- Funciones auxiliares: `format_amount()`, `round_half_up()`, `get_line_tax_base()`, `get_pos_and_number()`.
