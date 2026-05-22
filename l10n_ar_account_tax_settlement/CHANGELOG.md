# Changelog


## [17.0.1.8.7] - 2026-05-22
### Corrección
 - **SIFERE - Generación de archivos TXT (iibb_sufrido_files_values):**
   - Corrección del número de certificado de retención en el TXT cuando un mismo comprobante de pago contiene dos o más retenciones del mismo impuesto.
   - Antes el archivo repetía el mismo número de certificado en todas las líneas de retención (se tomaba siempre el primero) porque se leía desde `line.withholding_id.name`, y el compute de `withholding_id` devuelve siempre el primer match cuando hay varias retenciones del mismo `tax_id` en el pago.
   - Ahora se usa `line.name`, que en cada apunte contable guarda el número de certificado correspondiente a su propia retención (el sync `_prepare_witholding_write_off_vals` lo setea por línea).

## [17.0.1.8.6] - 2026-04-16
### Corrección
 - **AGIP - Generación de archivos TXT (iibb_aplicado_agip_files_values) [TKT5947]:**
   - Consolidación de apuntes duplicados del mismo impuesto sobre un mismo comprobante. Odoo puede emitir más de un `account.move.line` con el mismo `tax_line_id` sobre una misma factura/NC (por ejemplo: líneas de producto con `price_unit` negativo, o recomputo parcial de impuestos). Sin esta consolidación, el TXT duplicaba el comprobante con montos parciales y e-ARCIBA lo rechazaba.
   - Se agrega un pre-procesamiento que suma `balance` y `tax_base_amount` por `(move_id, tax_line_id)`, y luego itera una sola línea por combinación usando los valores consolidados (`_c_balance`, `_c_tax_base`) en los campos: 4 (NC - Monto), 12 (NC - Ret/percep a deducir), 8 (Monto del comprobante - vía `perception_amount`), 20 (Retención/Percepción Practicada) y 21 (Monto Total Retenido/Percibido).

## [17.0.1.8.5] - 2026-03-01
### Corrección  
 - Se traslada todo lo desarrollado previamente de las version 17.0.1.7.[3-4-5], al módulo l10n_ar_withholding_arba debido a la necesidad de utilizar los campos lot_name y activity definidos en ese módulo

## [17.0.1.7.5] - 2026-03-01
### Mejora  
 - Desarrollo para archivos .txt según Resolución Normativa ARBA 22/2025 - Entrada en vigor 1/3 - Emisión de Comprobante de Retención: Comprobante A-122R


## [17.0.1.7.4] - 2026-03-01
### Mejora  
 - Desarrollo de nuevos archivos txt para la presentación de declaraciones juradas de impuestos provinciales de ARBA.
   1) 'TXT Perc/Ret IIBB aplicadas ARBA desde 01/03/2026: Percepciones ( excepto actividad 29, 7 quincenal, 7 y 17 de Bancos)'. (iibb_aplicado_arba_desde_01032026)
   2) 'TXT Perc/Ret IIBB aplicadas ARBA desde 01/03/2026: Percepciones Act. 7 método Percibido (quincenal)'. (iibb_aplicado_arba_act_7_desde_01032026)
  - La especificación de los 2 archivos txt se puede ver en readme o en el docstring de cada uno de los métodos que los generan.

## [17.0.1.7.3] - 2026-02-06

### Corregido
- **AGIP - Generación de archivos TXT (iibb_aplicado_agip_files_values):**
  - Corrección de valores negativos en archivos de AGIP que causaban rechazo en el aplicativo ARCIBA
  - Campo 16 (Importe otros conceptos): Ahora se reporta siempre como valor absoluto (≥0) según especificación AGIP v3.0
  - Campo 17 (Importe IVA): Se aplica valor absoluto para cumplir con requisito de mínimo 0
  - Campo 18 (Monto sujeto a retención/percepción): Se fuerza valor absoluto (>0) según especificación
  - Campo 20 (Retención/Percepción practicada): Valores absolutos para evitar rechazo
  - Campo 21 (Monto total retenido/percibido): Valores absolutos aplicados
  - **Notas de Crédito (NC):**
    - Campo 4 (Monto nota de crédito): Valor absoluto aplicado (>0)
    - Campo 12 (Ret/percep a deducir): Valor absoluto aplicado (>0)
  - Validación agregada: Ahora se verifica que todas las líneas tengan impuesto asociado (tax_line_id) antes de generar el archivo
  - Solución al problema reportado: "la columna 16 no es un decimal válido" y "el importe de otros conceptos no es válido"
  - Especialmente crítico para Órdenes de Pago (OP) asociadas a Notas de Crédito donde los cálculos resultaban negativos

### Notas
- Los cambios cumplen con la especificación oficial de AGIP versión 3.0
- Todos los campos numéricos ahora reportan valores absolutos según requerimiento de AGIP
- Los archivos generados ahora deben importarse correctamente en el aplicativo e-ARCIBA sin errores de formato

## [17.0.1.7.2] - Anterior
- Versión base del módulo

---

