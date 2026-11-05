# Facturación electrónica argentina UX

## Descripción General

Extiende la facturación electrónica argentina de Odoo Enterprise y la consulta
al padrón. Agrega un indicador de disponibilidad de ARCA a la barra superior.
La documentación previa del módulo se conserva en `README.rst`.

## Funcionalidades

- Indicador «Conexión ARCA» para compañías argentinas, con el ambiente de la
  compañía activa (producción u homologación).
- Consulta WSFE mediante `FEDummy` y disponibilidad del WSDL de WSAA. El control
  de WSAA no valida certificados, delegaciones ni credenciales de la compañía.
- «Verificar ahora» realiza consultas nuevas y actualiza el resultado visible.
- Consulta programada cada cinco minutos para los ambientes configurados.
- Última verificación en la zona horaria y formato del usuario. Antes de la
  primera consulta se informa que el servicio todavía no fue verificado.
- Fallas de red, respuestas incompletas y servicios no operativos se muestran
  como no disponibles, sin reutilizar estados exitosos como resultado nuevo.
- No se envían comprobantes ni se solicitan tokens desde el indicador.

## Instalación

- Para instalar este módulo seleccione `l10n_ar_edi_ux` en Ajustes → Aplicaciones
  e instálelo como cualquier otro módulo de Odoo. En bases existentes, actualice
  el módulo y recargue el navegador para cargar los nuevos recursos.
- Requiere las dependencias indicadas en el manifest, entre ellas `l10n_ar_edi`.
- Configure el ambiente ARCA de cada compañía en los ajustes contables y la zona
  horaria del usuario en sus preferencias.
- Usuarios internos pueden consultar y refrescar el indicador; los registros
  almacenados de estado no admiten edición directa por esos usuarios.
- Este indicador es informativo y no reemplaza el control preventivo de emisión
  de `aitic_l10n_ar_afip_status`. No automatiza la actualización de contactos.

## Colaboradores

- Desarrollo original: ADHOC SA; ver `README.rst` y el historial del repositorio.
- Adaptación del indicador de disponibilidad: AITIC S.A.S.

---

## AITIC

Adaptación desarrollada por **AITIC** — [aitic.com.ar](https://www.aitic.com.ar).

[![AITIC](https://www.aitic.com.ar/web/image/website/1/logo/AITIC?unique=0d6d95a)](https://www.aitic.com.ar)
