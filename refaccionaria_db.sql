-- ================================================================
-- BASE DE DATOS REFACCIONARIA OVIEDO
-- Sistema completo de gestión de refacciones automotrices
-- Última actualización: Febrero 2026
-- ================================================================

CREATE DATABASE IF NOT EXISTS refaccionaria_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE refaccionaria_db;

-- ================================================================
-- CONFIGURACIÓN DEL SISTEMA
-- ================================================================

CREATE TABLE IF NOT EXISTS configuracion_sistema (
    id INT PRIMARY KEY AUTO_INCREMENT,
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor TEXT,
    tipo VARCHAR(50),
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_clave (clave)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar configuraciones iniciales
INSERT INTO configuracion_sistema (clave, valor, tipo, descripcion) VALUES
('empresa_nombre', 'Refaccionaria Automotriz', 'string', 'Nombre de la empresa'),
('empresa_rfc', 'XAXX010101000', 'string', 'RFC de la empresa'),
('empresa_direccion', 'Calle Principal #123', 'string', 'Dirección fiscal'),
('iva_porcentaje', '16', 'decimal', 'Porcentaje de IVA'),
('ticket_mensaje', 'Gracias por su compra', 'string', 'Mensaje en ticket'),
('stock_minimo_global', '5', 'integer', 'Stock mínimo global para alertas'),
('ventas_folio_inicial', '1000', 'integer', 'Número inicial para folios')
ON DUPLICATE KEY UPDATE valor=VALUES(valor);

-- ================================================================
-- LOCALES / SUCURSALES
-- ================================================================

CREATE TABLE IF NOT EXISTS locales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- USUARIOS Y AUTENTICACIÓN
-- ================================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100),
    apellido_materno VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    clave_hash VARCHAR(255) NOT NULL,
    rol ENUM('administrador', 'gerente', 'vendedor', 'almacenista', 'cajero') DEFAULT 'vendedor',
    estado ENUM('activo', 'inactivo', 'suspendido') DEFAULT 'activo',
    local_id INT,
    ultimo_login DATETIME,
    intentos_fallidos INT DEFAULT 0,
    bloqueado_hasta DATETIME,
    debe_cambiar_clave BOOLEAN DEFAULT TRUE,
    tema_interfaz VARCHAR(20) DEFAULT 'claro',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (local_id) REFERENCES locales(id) ON DELETE SET NULL,
    INDEX idx_nombre_usuario (nombre_usuario),
    INDEX idx_email (email),
    INDEX idx_local (local_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- CATÁLOGO DE MARCAS
-- ================================================================

CREATE TABLE IF NOT EXISTS marcas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    pais_origen VARCHAR(100),
    activo INT DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- PRODUCTOS
-- ================================================================

CREATE TABLE IF NOT EXISTS productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    codigo_barras VARCHAR(100) UNIQUE,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    categoria VARCHAR(100),
    precio_compra DECIMAL(10, 2) NOT NULL,
    precio_venta DECIMAL(10, 2) NOT NULL,
    precio_venta_credito DECIMAL(10, 2),
    stock_total INT DEFAULT 0,
    stock_minimo INT DEFAULT 5,
    ubicacion_estante VARCHAR(50),
    ubicacion_fila VARCHAR(10),
    ubicacion_columna VARCHAR(10),
    compatibilidad JSON,
    año_inicio INT,
    año_fin INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_codigo (codigo),
    INDEX idx_codigo_barras (codigo_barras),
    INDEX idx_nombre (nombre),
    INDEX idx_marca (marca),
    INDEX idx_categoria (categoria)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- INVENTARIO POR LOCAL
-- ================================================================

CREATE TABLE IF NOT EXISTS inventario_local (
    id INT PRIMARY KEY AUTO_INCREMENT,
    producto_id INT NOT NULL,
    local_id INT NOT NULL,
    stock INT DEFAULT 0,
    stock_reservado INT DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    FOREIGN KEY (local_id) REFERENCES locales(id) ON DELETE CASCADE,
    UNIQUE KEY uq_producto_local (producto_id, local_id),
    INDEX idx_producto (producto_id),
    INDEX idx_local (local_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- CLIENTES
-- ================================================================

CREATE TABLE IF NOT EXISTS clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    alias VARCHAR(100),
    nombre VARCHAR(200) NOT NULL,
    apellido_paterno VARCHAR(100),
    apellido_materno VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(20),
    rfc VARCHAR(13) UNIQUE,
    tipo_figura VARCHAR(50) DEFAULT 'Persona Física',
    razon_social VARCHAR(200),
    calle VARCHAR(200),
    numero VARCHAR(20),
    colonia VARCHAR(100),
    ciudad VARCHAR(100),
    estado VARCHAR(100),
    codigo_postal VARCHAR(10),
    activo BOOLEAN DEFAULT TRUE,
    local_id INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (local_id) REFERENCES locales(id) ON DELETE SET NULL,
    INDEX idx_nombre (nombre),
    INDEX idx_email (email),
    INDEX idx_rfc (rfc),
    INDEX idx_alias (alias)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- PROVEEDORES
-- ================================================================

CREATE TABLE IF NOT EXISTS proveedores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    clave VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    rfc VARCHAR(20),
    web VARCHAR(200),
    calle VARCHAR(200),
    numero_exterior VARCHAR(20),
    numero_interior VARCHAR(20),
    colonia VARCHAR(100),
    codigo_postal VARCHAR(10),
    municipio VARCHAR(100),
    estado VARCHAR(100),
    ciudad VARCHAR(100),
    pais VARCHAR(100) DEFAULT 'MEXICO',
    contacto_compras_nombre VARCHAR(100),
    contacto_compras_email VARCHAR(100),
    contacto_compras_telefono VARCHAR(20),
    lista_precios_compra VARCHAR(100),
    dias_entrega INT DEFAULT 0,
    tipo_moneda ENUM('pesos', 'dolares') DEFAULT 'pesos',
    descuento_factura DECIMAL(5, 2) DEFAULT 0,
    descuento_listas_precio DECIMAL(5, 2) DEFAULT 0,
    descuento_producto_factura DECIMAL(5, 2) DEFAULT 0,
    notas_compras TEXT,
    contacto_finanzas_nombre VARCHAR(100),
    contacto_finanzas_email VARCHAR(100),
    contacto_finanzas_telefono VARCHAR(20),
    forma_pago ENUM('contado', 'credito') DEFAULT 'contado',
    dias_credito INT DEFAULT 0,
    saldo DECIMAL(10, 2) DEFAULT 0,
    activo VARCHAR(10) DEFAULT 'ACTIVO',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_clave (clave),
    INDEX idx_nombre (nombre),
    INDEX idx_rfc (rfc)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- VENTAS
-- ================================================================

CREATE TABLE IF NOT EXISTS ventas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    folio VARCHAR(50) UNIQUE NOT NULL,
    local_id INT NOT NULL,
    usuario_id INT NOT NULL,
    cliente_id INT,
    tipo_venta ENUM('contado', 'credito', 'apartado') DEFAULT 'contado',
    estado ENUM('pendiente', 'completada', 'cancelada', 'devuelta') DEFAULT 'completada',
    subtotal DECIMAL(10, 2) DEFAULT 0,
    descuento DECIMAL(10, 2) DEFAULT 0,
    iva DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) DEFAULT 0,
    pago_recibido DECIMAL(10, 2) DEFAULT 0,
    cambio DECIMAL(10, 2) DEFAULT 0,
    fecha_limite_pago DATETIME,
    saldo_pendiente DECIMAL(10, 2) DEFAULT 0,
    metodo_pago VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (local_id) REFERENCES locales(id) ON DELETE RESTRICT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL,
    INDEX idx_folio (folio),
    INDEX idx_local (local_id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_cliente (cliente_id),
    INDEX idx_fecha (fecha_creacion),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS detalle_ventas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    local_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    descuento DECIMAL(10, 2) DEFAULT 0,
    importe DECIMAL(10, 2) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE RESTRICT,
    FOREIGN KEY (local_id) REFERENCES locales(id) ON DELETE RESTRICT,
    INDEX idx_venta (venta_id),
    INDEX idx_producto (producto_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- COMPRAS
-- ================================================================

CREATE TABLE IF NOT EXISTS compras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    folio VARCHAR(50) UNIQUE NOT NULL,
    factura VARCHAR(100),
    estado ENUM('pendiente', 'completo', 'cancelado', 'parcial') DEFAULT 'pendiente',
    fecha DATETIME NOT NULL,
    proveedor_id INT NOT NULL,
    local_id INT NOT NULL,
    usuario_id INT,
    subtotal DECIMAL(10, 2) DEFAULT 0,
    descuento DECIMAL(10, 2) DEFAULT 0,
    iva DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL,
    notas TEXT,
    tipo_moneda VARCHAR(20) DEFAULT 'pesos',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE RESTRICT,
    FOREIGN KEY (local_id) REFERENCES locales(id) ON DELETE RESTRICT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_folio (folio),
    INDEX idx_factura (factura),
    INDEX idx_proveedor (proveedor_id),
    INDEX idx_fecha (fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS detalle_compras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    compra_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    descuento DECIMAL(10, 2) DEFAULT 0,
    importe DECIMAL(10, 2) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (compra_id) REFERENCES compras(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE RESTRICT,
    INDEX idx_compra (compra_id),
    INDEX idx_producto (producto_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- TRASPASOS ENTRE LOCALES
-- ================================================================

CREATE TABLE IF NOT EXISTS traspasos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    folio VARCHAR(50) UNIQUE NOT NULL,
    estado ENUM('pendiente', 'transito', 'completado', 'cancelado') DEFAULT 'pendiente',
    fecha DATETIME NOT NULL,
    origen_id INT NOT NULL,
    destino_id INT NOT NULL,
    notas TEXT,
    usuario_id INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (origen_id) REFERENCES locales(id) ON DELETE RESTRICT,
    FOREIGN KEY (destino_id) REFERENCES locales(id) ON DELETE RESTRICT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_folio (folio),
    INDEX idx_origen (origen_id),
    INDEX idx_destino (destino_id),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS detalle_traspasos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    traspaso_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    cantidad_enviada INT DEFAULT 0,
    cantidad_recibida INT DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (traspaso_id) REFERENCES traspasos(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE RESTRICT,
    INDEX idx_traspaso (traspaso_id),
    INDEX idx_producto (producto_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- GASTOS
-- ================================================================

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar ejemplos de gastos
INSERT INTO gastos (folio, estado, fecha, total, categoria, factura, usuario, sucursal_origen, departamento, proveedor, sucursal_destino, descripcion) VALUES
('G-1023', 'Pendiente', '2024-12-18', 1850.00, 'Refacciones', 'F-8812', 'Laura Martínez', 'Matriz', 'Ventas', 'Autopartes MX', 'Sucursal Norte', 'Pastillas y balatas para revisión técnica'),
('G-1024', 'Pagado', '2024-12-22', 920.00, 'Insumos', 'F-8820', 'Carlos Pérez', 'Matriz', 'Compras', 'Suministros del Norte', 'Matriz', 'Papelería y etiquetas para inventario'),
('G-1025', 'Pendiente', '2025-01-05', 3120.00, 'Servicios', 'F-8890', 'Laura Martínez', 'Sucursal Norte', 'Ventas', 'Servicio Rápido', 'Sucursal Norte', 'Mantenimiento de racks y estantes'),
('G-1026', 'Cancelado', '2025-01-08', 450.00, 'Viáticos', 'F-8899', 'Diego Rodríguez', 'Matriz', 'Operaciones', 'Hotel Central', 'Matriz', 'Viaje a visita de proveedor'),
('G-1027', 'Pagado', '2025-01-12', 1750.00, 'Refacciones', 'F-8905', 'Ana Karen', 'Sucursal Centro', 'Taller', 'Autopartes MX', 'Sucursal Centro', 'Filtros y correas de motor')
ON DUPLICATE KEY UPDATE folio=VALUES(folio);

-- ================================================================
-- MÓDULO DE CAJA
-- ================================================================

-- Arqueos de Caja - Registro de arqueos (conciliación) de cajas
CREATE TABLE IF NOT EXISTS arqueos_caja (
    id INT PRIMARY KEY AUTO_INCREMENT,
    caja VARCHAR(50) NOT NULL COMMENT 'Identificador/nombre de la caja (ej: Caja 1)',
    local_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha_arqueo DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora del arqueo',
    turno VARCHAR(50) COMMENT 'Turno: Mañana, Tarde, Noche',
    -- Montos declarados
    efectivo_declarado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de efectivo según sistema',
    retiros_declarado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de retiros según sistema',
    cheque_declarado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de cheques según sistema',
    tarjeta_declarado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de tarjeta según sistema',
    debito_declarado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de débito según sistema',
    deposito_declarado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de depósito según sistema',
    credito_declarado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de crédito según sistema',
    vale_declarado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de vales según sistema',
    lealtad_declarado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de programa lealtad según sistema',
    -- Montos contados
    efectivo_contado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de efectivo contado físicamente',
    retiros_contado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de retiros contado físicamente',
    cheque_contado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de cheques contado físicamente',
    tarjeta_contado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de tarjeta contado físicamente',
    debito_contado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de débito contado físicamente',
    deposito_contado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de depósito contado físicamente',
    credito_contado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de crédito contado físicamente',
    vale_contado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de vales contado físicamente',
    lealtad_contado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Monto de programa lealtad contado físicamente',
    -- Diferencias
    diferencia_efectivo DECIMAL(12, 2) DEFAULT 0 COMMENT 'Diferencia = Contado - Declarado',
    diferencia_retiros DECIMAL(12, 2) DEFAULT 0 COMMENT 'Diferencia retiros = Contado - Declarado',
    diferencia_cheque DECIMAL(12, 2) DEFAULT 0 COMMENT 'Diferencia cheques = Contado - Declarado',
    diferencia_tarjeta DECIMAL(12, 2) DEFAULT 0 COMMENT 'Diferencia tarjeta = Contado - Declarado',
    diferencia_debito DECIMAL(12, 2) DEFAULT 0 COMMENT 'Diferencia débito = Contado - Declarado',
    diferencia_deposito DECIMAL(12, 2) DEFAULT 0 COMMENT 'Diferencia depósito = Contado - Declarado',
    diferencia_credito DECIMAL(12, 2) DEFAULT 0 COMMENT 'Diferencia crédito = Contado - Declarado',
    diferencia_vale DECIMAL(12, 2) DEFAULT 0 COMMENT 'Diferencia vales = Contado - Declarado',
    diferencia_lealtad DECIMAL(12, 2) DEFAULT 0 COMMENT 'Diferencia lealtad = Contado - Declarado',
    -- Totales
    total_declarado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Total declarado (suma de todos)',
    total_contado DECIMAL(12, 2) DEFAULT 0 COMMENT 'Total contado (suma de todos)',
    diferencia_total DECIMAL(12, 2) DEFAULT 0 COMMENT 'Diferencia total = Contado - Declarado',
    -- Observaciones
    observaciones TEXT COMMENT 'Notas y observaciones del arqueo',
    reconciliado BOOLEAN DEFAULT FALSE COMMENT 'TRUE si el arqueo fue reconciliado/validado',
    responsable_reconciliacion VARCHAR(255) COMMENT 'Nombre/ID del gerente que reconcilió',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora de creación del registro',
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha y hora de última actualización',
    FOREIGN KEY (local_id) REFERENCES locales(id) ON DELETE RESTRICT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    INDEX idx_caja (caja),
    INDEX idx_local (local_id),
    INDEX idx_fecha (fecha_arqueo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Cierres de Caja
CREATE TABLE IF NOT EXISTS cierres_caja (
    id INT PRIMARY KEY AUTO_INCREMENT,
    caja VARCHAR(50) NOT NULL,
    local_id INT NOT NULL,
    usuario_id INT NOT NULL,
    efectivo DECIMAL(12, 2) DEFAULT 0,
    cheque DECIMAL(12, 2) DEFAULT 0,
    tarjeta DECIMAL(12, 2) DEFAULT 0,
    debito DECIMAL(12, 2) DEFAULT 0,
    deposito DECIMAL(12, 2) DEFAULT 0,
    credito DECIMAL(12, 2) DEFAULT 0,
    vale DECIMAL(12, 2) DEFAULT 0,
    lealtad DECIMAL(12, 2) DEFAULT 0,
    retiros DECIMAL(12, 2) DEFAULT 0,
    total_ingresos DECIMAL(12, 2) DEFAULT 0,
    total_cierre DECIMAL(12, 2) DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (local_id) REFERENCES locales(id) ON DELETE RESTRICT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    INDEX idx_caja (caja),
    INDEX idx_local (local_id),
    INDEX idx_fecha (fecha_creacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Retiros de Caja
CREATE TABLE IF NOT EXISTS retiros_caja (
    id INT PRIMARY KEY AUTO_INCREMENT,
    folio VARCHAR(50) UNIQUE NOT NULL,
    local_id INT NOT NULL,
    usuario_id INT NOT NULL,
    monto DECIMAL(12, 2) NOT NULL,
    fecha_retiro DATETIME DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (local_id) REFERENCES locales(id) ON DELETE RESTRICT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    INDEX idx_folio (folio),
    INDEX idx_local (local_id),
    INDEX idx_fecha (fecha_retiro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- VALES DE VENTA
-- ================================================================

CREATE TABLE IF NOT EXISTS vales_venta (
    id INT PRIMARY KEY AUTO_INCREMENT,
    folio VARCHAR(50) UNIQUE NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    concepto VARCHAR(200),
    fecha DATETIME NOT NULL,
    vendedor_id INT NOT NULL,
    local_id INT NOT NULL,
    usado BOOLEAN DEFAULT FALSE,
    fecha_uso DATETIME,
    destino VARCHAR(50),
    tipo ENUM('venta', 'devolucion') DEFAULT 'venta',
    disponible BOOLEAN DEFAULT TRUE,
    descripcion VARCHAR(500),
    venta_origen_id INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (vendedor_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    FOREIGN KEY (local_id) REFERENCES locales(id) ON DELETE RESTRICT,
    FOREIGN KEY (venta_origen_id) REFERENCES ventas(id) ON DELETE SET NULL,
    INDEX idx_folio (folio),
    INDEX idx_vendedor (vendedor_id),
    INDEX idx_usado (usado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- PAQUETES Y GRUPOS DE PRODUCTOS
-- ================================================================

-- Paquetes
CREATE TABLE IF NOT EXISTS paquetes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    clase VARCHAR(100),
    codigo_barras VARCHAR(100) UNIQUE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_clase (clase),
    INDEX idx_codigo_barras (codigo_barras)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS paquete_productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paquete_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT DEFAULT 1,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (paquete_id) REFERENCES paquetes(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE RESTRICT,
    INDEX idx_paquete (paquete_id),
    INDEX idx_producto (producto_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Grupos
CREATE TABLE IF NOT EXISTS grupos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(200) NOT NULL,
    tipo VARCHAR(100),
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_tipo (tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS grupo_productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    grupo_id INT NOT NULL,
    producto_id INT NOT NULL,
    linea VARCHAR(100),
    caracteristica1 VARCHAR(200),
    caracteristica2 VARCHAR(200),
    clave VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (grupo_id) REFERENCES grupos(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    INDEX idx_grupo (grupo_id),
    INDEX idx_producto (producto_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS grupo_aplicaciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    grupo_id INT NOT NULL,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    motor VARCHAR(100),
    desde INT,
    hasta INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (grupo_id) REFERENCES grupos(id) ON DELETE CASCADE,
    INDEX idx_grupo (grupo_id),
    INDEX idx_marca (marca),
    INDEX idx_modelo (modelo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- PROMOCIONES
-- ================================================================

CREATE TABLE IF NOT EXISTS promociones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(120) NOT NULL,
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar promoción de ejemplo
INSERT INTO promociones (descripcion, activa) VALUES 
('10% de descuento en filtros de aceite', TRUE)
ON DUPLICATE KEY UPDATE descripcion=VALUES(descripcion);

-- ================================================================
-- ASISTENCIA DE EMPLEADOS
-- ================================================================

CREATE TABLE IF NOT EXISTS asistencia_empleados (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    sucursal VARCHAR(100),
    fecha DATE NOT NULL,
    entrada TIME,
    comida TIME,
    regreso TIME,
    salida TIME,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_asistencia_nombre_fecha (nombre, fecha),
    INDEX idx_nombre (nombre),
    INDEX idx_fecha (fecha),
    INDEX idx_sucursal (sucursal)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- DATOS DE EJEMPLO
-- ================================================================

-- Insertar retiros de caja de ejemplo (comentado por defecto)
-- Descomenta para insertar datos de prueba
/*
INSERT INTO retiros_caja (folio, local_id, usuario_id, monto, descripcion, fecha_retiro) VALUES
('R-20260120-001', 1, 3, 4800.00, 'RETIRO GENERADO AUTOMATICO', '2026-01-20 12:32:24'),
('R-20260119-002', 1, 3, 5100.00, 'RETIRO GENERADO AUTOMATICO', '2026-01-19 14:19:23'),
('R-20260119-003', 1, 3, 5100.00, 'RETIRO GENERADO AUTOMATICO', '2026-01-19 11:56:55'),
('R-20260117-004', 1, 3, 4800.00, 'RETIRO GENERADO AUTOMATICO', '2026-01-17 09:34:12'),
('R-20260116-005', 1, 3, 4800.00, 'RETIRO GENERADO AUTOMATICO', '2026-01-16 14:37:33'),
('R-20260115-006', 1, 6, 4800.00, 'RETIRO GENERADO AUTOMATICO', '2026-01-15 12:04:42'),
('R-20260114-007', 1, 3, 4800.00, 'RETIRO GENERADO AUTOMATICO', '2026-01-14 16:06:14'),
('R-20260113-008', 1, 3, 5100.00, 'RETIRO GENERADO AUTOMATICO', '2026-01-13 15:34:31'),
('R-20260112-009', 1, 3, 5080.00, 'ANILLOS BASTIDORES AUTO', '2026-01-12 11:18:07'),
('R-20260112-010', 1, 3, 5080.00, 'PROD CASTROL', '2026-01-12 11:18:31')
ON DUPLICATE KEY UPDATE folio=VALUES(folio);
*/

-- ================================================================
-- COMENTARIOS Y DOCUMENTACIÓN
-- ================================================================

-- Comentarios sobre tablas de arqueos
ALTER TABLE arqueos_caja COMMENT = 'Registro de arqueos (conciliación) de cajas';

-- Información sobre el esquema
SELECT 
    'Base de datos refaccionaria_db creada exitosamente' AS mensaje,
    '25 tablas principales creadas' AS detalle,
    'Febrero 2026' AS ultima_actualizacion;

-- ================================================================
-- FIN DEL SCRIPT
-- ================================================================
