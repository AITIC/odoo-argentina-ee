## [17.0.1.11.0] - 2026-11-05

### Added

- Indicador «Conexión ARCA» en la barra superior, con disponibilidad de WSFE y
  WSAA por ambiente de la compañía activa y actualización programada cada cinco
  minutos. Reutiliza el transporte TLS de `l10n_ar_edi`, sin generar tokens.

### Fixed

- `ArcaStatusSystray.onRefreshClick` consulta y guarda un estado nuevo mediante
  `refresh_status`, en lugar de releer el resultado anterior. Informa fallas de
  consulta sin mostrar una confirmación exitosa.
- `ArcaStatusSystray.lastCheckLabel` convierte la fecha UTC al huso horario y
  formato del usuario, incluyendo cambios de día.
- Adaptación de la interfaz de v19 para Odoo 17.
  Ticket [#6680](https://www.aitic.com.ar/odoo/helpdesk.ticket/7182).
