-- Script para crear la tabla de cierres_caja (si no está creada por SQLAlchemy)
-- Esta tabla se crea automáticamente desde el modelo CierreCaja al iniciar la aplicación

CREATE TABLE IF NOT EXISTS cierres_caja (
    id INT PRIMARY KEY AUTO_INCREMENT,
    caja VARCHAR(50) NOT NULL,
    local_id INT NOT NULL,
    usuario_id INT NOT NULL,
    efectivo DECIMAL(12,2) DEFAULT 0,
    cheque DECIMAL(12,2) DEFAULT 0,
    tarjeta DECIMAL(12,2) DEFAULT 0,
    debito DECIMAL(12,2) DEFAULT 0,
    deposito DECIMAL(12,2) DEFAULT 0,
    credito DECIMAL(12,2) DEFAULT 0,
    vale DECIMAL(12,2) DEFAULT 0,
    lealtad DECIMAL(12,2) DEFAULT 0,
    retiros DECIMAL(12,2) DEFAULT 0,
    total_ingresos DECIMAL(12,2) DEFAULT 0,
    total_cierre DECIMAL(12,2) DEFAULT 0,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (local_id) REFERENCES locales(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_caja (caja),
    INDEX idx_local_id (local_id),
    INDEX idx_usuario_id (usuario_id),
    INDEX idx_fecha_creacion (fecha_creacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
