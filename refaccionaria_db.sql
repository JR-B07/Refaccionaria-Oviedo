CREATE DATABASE IF NOT EXISTS refaccionaria_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE refaccionaria_db;

-- Tabla de configuración del sistema
CREATE TABLE IF NOT EXISTS configuracion_sistema (
    id INT PRIMARY KEY AUTO_INCREMENT,
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor TEXT,
    tipo VARCHAR(50),
    descripcion TEXT,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insertar configuraciones iniciales
INSERT INTO configuracion_sistema (clave, valor, tipo, descripcion) VALUES
('empresa_nombre', 'Refaccionaria Automotriz', 'string', 'Nombre de la empresa'),
('empresa_rfc', 'XAXX010101000', 'string', 'RFC de la empresa'),
('empresa_direccion', 'Calle Principal #123', 'string', 'Dirección fiscal'),
('iva_porcentaje', '16', 'decimal', 'Porcentaje de IVA'),
('ticket_mensaje', 'Gracias por su compra', 'string', 'Mensaje en ticket'),
('stock_minimo_global', '5', 'integer', 'Stock mínimo global para alertas'),
('ventas_folio_inicial', '1000', 'integer', 'Número inicial para folios');

-- Tabla de Gastos
CREATE TABLE IF NOT EXISTS gastos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    folio VARCHAR(50) UNIQUE NOT NULL,
    estado ENUM('Pendiente', 'Pagado', 'Cancelado') DEFAULT 'Pendiente' NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    total DECIMAL(12, 2) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    factura VARCHAR(50),
    usuario VARCHAR(150) NOT NULL,
    sucursal_origen VARCHAR(100) NOT NULL,
    departamento VARCHAR(100) NOT NULL,
    proveedor VARCHAR(150),
    sucursal_destino VARCHAR(100),
    descripcion TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    INDEX idx_folio (folio),
    INDEX idx_estado (estado),
    INDEX idx_usuario (usuario),
    INDEX idx_departamento (departamento),
    INDEX idx_fecha (fecha)
);

INSERT INTO gastos (folio, estado, fecha, total, categoria, factura, usuario, sucursal_origen, departamento, proveedor, sucursal_destino, descripcion) VALUES
('G-1023', 'Pendiente', '2024-12-18', 1850.00, 'Refacciones', 'F-8812', 'Laura Martínez', 'Matriz', 'Ventas', 'Autopartes MX', 'Sucursal Norte', 'Pastillas y balatas para revisión técnica'),
('G-1024', 'Pagado', '2024-12-22', 920.00, 'Insumos', 'F-8820', 'Carlos Pérez', 'Matriz', 'Compras', 'Suministros del Norte', 'Matriz', 'Papelería y etiquetas para inventario'),
('G-1025', 'Pendiente', '2025-01-05', 3120.00, 'Servicios', 'F-8890', 'Laura Martínez', 'Sucursal Norte', 'Ventas', 'Servicio Rápido', 'Sucursal Norte', 'Mantenimiento de racks y estantes'),
('G-1026', 'Cancelado', '2025-01-08', 450.00, 'Viáticos', 'F-8899', 'Diego Rodríguez', 'Matriz', 'Operaciones', 'Hotel Central', 'Matriz', 'Viaje a visita de proveedor'),
('G-1027', 'Pagado', '2025-01-12', 1750.00, 'Refacciones', 'F-8905', 'Ana Karen', 'Sucursal Centro', 'Taller', 'Autopartes MX', 'Sucursal Centro', 'Filtros y correas de motor');

-- Tabla de Promociones
CREATE TABLE IF NOT EXISTS promociones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(120) NOT NULL,
    activa BOOLEAN DEFAULT TRUE
);

-- Insertar promoción de ejemplo
INSERT INTO promociones (descripcion, activa) VALUES ('10% de descuento en filtros de aceite', TRUE);

-- Índices para optimización
CREATE INDEX idx_productos_codigo ON productos(codigo);
CREATE INDEX idx_productos_codigo_barras ON productos(codigo_barras);
CREATE INDEX idx_ventas_folio ON ventas(folio);
CREATE INDEX idx_ventas_fecha ON ventas(fecha_creacion);
CREATE INDEX idx_inventario_local ON inventario_local(local_id, producto_id);