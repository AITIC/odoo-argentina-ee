# Changelog

Todas las modificaciones relevantes de este módulo se documentarán aquí.

## [15.0.1.10.2] - 2026-02-27
- Actualización de la versión en __manifest__.py a 15.0.1.10.2.
- Traslado de código al módulo 'l10n_ar_withholding_arba' para poder utilizar los campos 'activity' y 'lot_name' del modelo account.journal definidos en ese módulo

## [15.0.1.9.2] - 2026-02-27
- Actualización de la versión en __manifest__.py a 15.0.1.9.2.
- Modificación de archivo .txt a .csv para retenciones_iva_files_values

## [15.0.1.9.1] - 2026-02-27
- Actualización de la versión en __manifest__.py a 15.0.1.9.1.
- Implementación de Normativa ARCA A112R


## [15.0.1.8.1] - 2026-02-27
- Actualización de la versión en __manifest__.py a 15.0.1.8.1.
- Se agregan nuevas opciones y métodos para exportar TXT de percepciones y retenciones ARBA según la nueva especificación vigente desde el 01/03/2026:
	- Opción 'iibb_aplicado_arba_desde_01032026' y 'iibb_aplicado_arba_act_7_desde_01032026' en el campo settlement_tax.
	- Métodos asociados para la generación de archivos TXT conforme a la normativa ARBA (incluyendo percepciones Act. 7 método Percibido y retenciones).
	- Implementación basada en la especificación oficial publicada por ARBA.

## [15.0.0] - 2026-02-27
- Creación del archivo de changelog para registrar cambios futuros en el módulo `l10n_ar_account_tax_settlement`.


