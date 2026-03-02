# Changelog

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

