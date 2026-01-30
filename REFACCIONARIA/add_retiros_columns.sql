-- Agregar columnas de retiros a la tabla arqueos_caja
USE refaccionaria;

-- Agregar retiros_declarado después de efectivo_declarado
ALTER TABLE arqueos_caja 
ADD COLUMN retiros_declarado DECIMAL(12,2) DEFAULT 0.00 AFTER efectivo_declarado;

-- Agregar retiros_contado después de efectivo_contado
ALTER TABLE arqueos_caja 
ADD COLUMN retiros_contado DECIMAL(12,2) DEFAULT 0.00 AFTER efectivo_contado;

-- Agregar diferencia_retiros después de diferencia_efectivo
ALTER TABLE arqueos_caja 
ADD COLUMN diferencia_retiros DECIMAL(12,2) DEFAULT 0.00 AFTER diferencia_efectivo;

-- Verificar las columnas agregadas
SELECT COLUMN_NAME, DATA_TYPE, COLUMN_DEFAULT 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'refaccionaria' 
  AND TABLE_NAME = 'arqueos_caja' 
  AND COLUMN_NAME LIKE '%retiros%';
