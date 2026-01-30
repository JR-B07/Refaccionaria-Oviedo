-- Script SQL para crear la tabla de Arqueos de Caja
-- Este archivo es de referencia; las tablas se crean automáticamente vía SQLAlchemy

CREATE TABLE arqueos_caja (
    id INT PRIMARY KEY AUTO_INCREMENT,
    caja VARCHAR(50) NOT NULL,
    local_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha_arqueo DATETIME DEFAULT CURRENT_TIMESTAMP,
    turno VARCHAR(50),
    
    -- Montos declarados
    efectivo_declarado DECIMAL(12, 2) DEFAULT 0,
    cheque_declarado DECIMAL(12, 2) DEFAULT 0,
    tarjeta_declarado DECIMAL(12, 2) DEFAULT 0,
    debito_declarado DECIMAL(12, 2) DEFAULT 0,
    deposito_declarado DECIMAL(12, 2) DEFAULT 0,
    credito_declarado DECIMAL(12, 2) DEFAULT 0,
    vale_declarado DECIMAL(12, 2) DEFAULT 0,
    lealtad_declarado DECIMAL(12, 2) DEFAULT 0,
    
    -- Montos contados
    efectivo_contado DECIMAL(12, 2) DEFAULT 0,
    cheque_contado DECIMAL(12, 2) DEFAULT 0,
    tarjeta_contado DECIMAL(12, 2) DEFAULT 0,
    debito_contado DECIMAL(12, 2) DEFAULT 0,
    deposito_contado DECIMAL(12, 2) DEFAULT 0,
    credito_contado DECIMAL(12, 2) DEFAULT 0,
    vale_contado DECIMAL(12, 2) DEFAULT 0,
    lealtad_contado DECIMAL(12, 2) DEFAULT 0,
    
    -- Diferencias
    diferencia_efectivo DECIMAL(12, 2) DEFAULT 0,
    diferencia_cheque DECIMAL(12, 2) DEFAULT 0,
    diferencia_tarjeta DECIMAL(12, 2) DEFAULT 0,
    diferencia_debito DECIMAL(12, 2) DEFAULT 0,
    diferencia_deposito DECIMAL(12, 2) DEFAULT 0,
    diferencia_credito DECIMAL(12, 2) DEFAULT 0,
    diferencia_vale DECIMAL(12, 2) DEFAULT 0,
    diferencia_lealtad DECIMAL(12, 2) DEFAULT 0,
    
    -- Totales
    total_declarado DECIMAL(12, 2) DEFAULT 0,
    total_contado DECIMAL(12, 2) DEFAULT 0,
    diferencia_total DECIMAL(12, 2) DEFAULT 0,
    
    -- Detalles
    observaciones TEXT,
    reconciliado BOOLEAN DEFAULT FALSE,
    responsable_reconciliacion VARCHAR(255),
    
    -- Auditoría
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Claves foráneas
    FOREIGN KEY (local_id) REFERENCES locales(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    
    -- Índices
    INDEX idx_caja (caja),
    INDEX idx_local (local_id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_fecha (fecha_arqueo),
    INDEX idx_estado (reconciliado)
);

-- Comentarios para documentación
ALTER TABLE arqueos_caja COMMENT = 'Registro de arqueos (conciliación) de cajas';
ALTER TABLE arqueos_caja MODIFY COLUMN caja COMMENT 'Identificador/nombre de la caja (ej: Caja 1)';
ALTER TABLE arqueos_caja MODIFY COLUMN turno COMMENT 'Turno: Mañana, Tarde, Noche';
ALTER TABLE arqueos_caja MODIFY COLUMN efectivo_declarado COMMENT 'Monto de efectivo según sistema';
ALTER TABLE arqueos_caja MODIFY COLUMN efectivo_contado COMMENT 'Monto de efectivo contado físicamente';
ALTER TABLE arqueos_caja MODIFY COLUMN diferencia_efectivo COMMENT 'Diferencia = Contado - Declarado (positivo: sobrante, negativo: faltante)';
ALTER TABLE arqueos_caja MODIFY COLUMN reconciliado COMMENT 'TRUE si el arqueo fue reconciliado/validado';
ALTER TABLE arqueos_caja MODIFY COLUMN responsable_reconciliacion COMMENT 'Nombre/ID del gerente que reconcilió';
