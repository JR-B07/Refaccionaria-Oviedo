-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 10-02-2026 a las 04:25:34
-- Versión del servidor: 8.0.30
-- Versión de PHP: 8.2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `refaccionaria_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `arqueos_caja`
--

CREATE TABLE `arqueos_caja` (
  `caja` varchar(50) NOT NULL,
  `local_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `fecha_arqueo` datetime DEFAULT CURRENT_TIMESTAMP,
  `turno` varchar(50) DEFAULT NULL,
  `efectivo_declarado` decimal(12,2) DEFAULT NULL,
  `retiros_declarado` decimal(12,2) DEFAULT NULL,
  `cheque_declarado` decimal(12,2) DEFAULT NULL,
  `tarjeta_declarado` decimal(12,2) DEFAULT NULL,
  `debito_declarado` decimal(12,2) DEFAULT NULL,
  `deposito_declarado` decimal(12,2) DEFAULT NULL,
  `credito_declarado` decimal(12,2) DEFAULT NULL,
  `vale_declarado` decimal(12,2) DEFAULT NULL,
  `lealtad_declarado` decimal(12,2) DEFAULT NULL,
  `efectivo_contado` decimal(12,2) DEFAULT NULL,
  `retiros_contado` decimal(12,2) DEFAULT NULL,
  `cheque_contado` decimal(12,2) DEFAULT NULL,
  `tarjeta_contado` decimal(12,2) DEFAULT NULL,
  `debito_contado` decimal(12,2) DEFAULT NULL,
  `deposito_contado` decimal(12,2) DEFAULT NULL,
  `credito_contado` decimal(12,2) DEFAULT NULL,
  `vale_contado` decimal(12,2) DEFAULT NULL,
  `lealtad_contado` decimal(12,2) DEFAULT NULL,
  `diferencia_efectivo` decimal(12,2) DEFAULT NULL,
  `diferencia_retiros` decimal(12,2) DEFAULT NULL,
  `diferencia_cheque` decimal(12,2) DEFAULT NULL,
  `diferencia_tarjeta` decimal(12,2) DEFAULT NULL,
  `diferencia_debito` decimal(12,2) DEFAULT NULL,
  `diferencia_deposito` decimal(12,2) DEFAULT NULL,
  `diferencia_credito` decimal(12,2) DEFAULT NULL,
  `diferencia_vale` decimal(12,2) DEFAULT NULL,
  `diferencia_lealtad` decimal(12,2) DEFAULT NULL,
  `total_declarado` decimal(12,2) DEFAULT NULL,
  `total_contado` decimal(12,2) DEFAULT NULL,
  `diferencia_total` decimal(12,2) DEFAULT NULL,
  `observaciones` text,
  `reconciliado` tinyint(1) DEFAULT NULL,
  `responsable_reconciliacion` varchar(255) DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Registro de arqueos (conciliación) de cajas';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencia_empleados`
--

CREATE TABLE `asistencia_empleados` (
  `nombre` varchar(150) NOT NULL,
  `sucursal` varchar(100) DEFAULT NULL,
  `fecha` date NOT NULL,
  `entrada` time DEFAULT NULL,
  `comida` time DEFAULT NULL,
  `regreso` time DEFAULT NULL,
  `salida` time DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cierres_caja`
--

CREATE TABLE `cierres_caja` (
  `caja` varchar(50) NOT NULL,
  `local_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `efectivo` decimal(12,2) DEFAULT NULL,
  `cheque` decimal(12,2) DEFAULT NULL,
  `tarjeta` decimal(12,2) DEFAULT NULL,
  `debito` decimal(12,2) DEFAULT NULL,
  `deposito` decimal(12,2) DEFAULT NULL,
  `credito` decimal(12,2) DEFAULT NULL,
  `vale` decimal(12,2) DEFAULT NULL,
  `lealtad` decimal(12,2) DEFAULT NULL,
  `retiros` decimal(12,2) DEFAULT NULL,
  `total_ingresos` decimal(12,2) DEFAULT NULL,
  `total_cierre` decimal(12,2) DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `alias` varchar(100) DEFAULT NULL,
  `nombre` varchar(200) NOT NULL,
  `apellido_paterno` varchar(100) DEFAULT NULL,
  `apellido_materno` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `rfc` varchar(13) DEFAULT NULL,
  `tipo_figura` varchar(50) DEFAULT NULL,
  `razon_social` varchar(200) DEFAULT NULL,
  `calle` varchar(200) DEFAULT NULL,
  `numero` varchar(20) DEFAULT NULL,
  `colonia` varchar(100) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `estado` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT NULL,
  `local_id` int DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compras`
--

CREATE TABLE `compras` (
  `folio` varchar(50) NOT NULL,
  `factura` varchar(100) DEFAULT NULL,
  `estado` enum('PENDIENTE','COMPLETO','CANCELADO','PARCIAL') DEFAULT NULL,
  `fecha` datetime NOT NULL,
  `proveedor_id` int NOT NULL,
  `local_id` int NOT NULL,
  `usuario_id` int DEFAULT NULL,
  `subtotal` decimal(10,2) DEFAULT NULL,
  `descuento` decimal(10,2) DEFAULT NULL,
  `iva` decimal(10,2) DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  `notas` text,
  `tipo_moneda` varchar(20) DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion_sistema`
--

CREATE TABLE `configuracion_sistema` (
  `id` int NOT NULL,
  `clave` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `valor` text COLLATE utf8mb4_unicode_ci,
  `tipo` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `configuracion_sistema`
--

INSERT INTO `configuracion_sistema` (`id`, `clave`, `valor`, `tipo`, `descripcion`, `fecha_creacion`, `fecha_actualizacion`) VALUES
(1, 'empresa_nombre', 'Refaccionaria Automotriz', 'string', 'Nombre de la empresa', '2026-02-10 04:24:04', '2026-02-10 04:24:04'),
(2, 'empresa_rfc', 'XAXX010101000', 'string', 'RFC de la empresa', '2026-02-10 04:24:04', '2026-02-10 04:24:04'),
(3, 'empresa_direccion', 'Calle Principal #123', 'string', 'Dirección fiscal', '2026-02-10 04:24:04', '2026-02-10 04:24:04'),
(4, 'iva_porcentaje', '16', 'decimal', 'Porcentaje de IVA', '2026-02-10 04:24:04', '2026-02-10 04:24:04'),
(5, 'ticket_mensaje', 'Gracias por su compra', 'string', 'Mensaje en ticket', '2026-02-10 04:24:04', '2026-02-10 04:24:04'),
(6, 'stock_minimo_global', '5', 'integer', 'Stock mínimo global para alertas', '2026-02-10 04:24:04', '2026-02-10 04:24:04'),
(7, 'ventas_folio_inicial', '1000', 'integer', 'Número inicial para folios', '2026-02-10 04:24:04', '2026-02-10 04:24:04');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_compras`
--

CREATE TABLE `detalle_compras` (
  `compra_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `descuento` decimal(10,2) DEFAULT NULL,
  `importe` decimal(10,2) NOT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_traspasos`
--

CREATE TABLE `detalle_traspasos` (
  `traspaso_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `cantidad_enviada` int DEFAULT NULL,
  `cantidad_recibida` int DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_ventas`
--

CREATE TABLE `detalle_ventas` (
  `venta_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `local_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `descuento` decimal(10,2) DEFAULT NULL,
  `importe` decimal(10,2) NOT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gastos`
--

CREATE TABLE `gastos` (
  `id` int NOT NULL,
  `folio` varchar(50) NOT NULL,
  `estado` enum('PENDIENTE','PAGADO','CANCELADO') NOT NULL,
  `fecha` datetime NOT NULL,
  `total` float NOT NULL,
  `categoria` varchar(100) NOT NULL,
  `factura` varchar(50) DEFAULT NULL,
  `usuario` varchar(150) NOT NULL,
  `sucursal_origen` varchar(100) NOT NULL,
  `departamento` varchar(100) NOT NULL,
  `proveedor` varchar(150) DEFAULT NULL,
  `sucursal_destino` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `fecha_creacion` datetime NOT NULL,
  `fecha_actualizacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `gastos`
--

INSERT INTO `gastos` (`id`, `folio`, `estado`, `fecha`, `total`, `categoria`, `factura`, `usuario`, `sucursal_origen`, `departamento`, `proveedor`, `sucursal_destino`, `descripcion`, `fecha_creacion`, `fecha_actualizacion`) VALUES
(1, 'G-1023', 'PENDIENTE', '2024-12-18 00:00:00', 1850, 'Refacciones', 'F-8812', 'Laura Martínez', 'Matriz', 'Ventas', 'Autopartes MX', 'Sucursal Norte', 'Pastillas y balatas para revisión técnica', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(2, 'G-1024', 'PAGADO', '2024-12-22 00:00:00', 920, 'Insumos', 'F-8820', 'Carlos Pérez', 'Matriz', 'Compras', 'Suministros del Norte', 'Matriz', 'Papelería y etiquetas para inventario', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(3, 'G-1025', 'PENDIENTE', '2025-01-05 00:00:00', 3120, 'Servicios', 'F-8890', 'Laura Martínez', 'Sucursal Norte', 'Ventas', 'Servicio Rápido', 'Sucursal Norte', 'Mantenimiento de racks y estantes', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(4, 'G-1026', 'CANCELADO', '2025-01-08 00:00:00', 450, 'Viáticos', 'F-8899', 'Diego Rodríguez', 'Matriz', 'Operaciones', 'Hotel Central', 'Matriz', 'Viaje a visita de proveedor', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(5, 'G-1027', 'PAGADO', '2025-01-12 00:00:00', 1750, 'Refacciones', 'F-8905', 'Ana Karen', 'Sucursal Centro', 'Taller', 'Autopartes MX', 'Sucursal Centro', 'Filtros y correas de motor', '0000-00-00 00:00:00', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupos`
--

CREATE TABLE `grupos` (
  `nombre` varchar(200) NOT NULL,
  `tipo` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `activo` tinyint(1) DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupo_aplicaciones`
--

CREATE TABLE `grupo_aplicaciones` (
  `grupo_id` int NOT NULL,
  `marca` varchar(100) DEFAULT NULL,
  `modelo` varchar(100) DEFAULT NULL,
  `motor` varchar(100) DEFAULT NULL,
  `desde` int DEFAULT NULL,
  `hasta` int DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupo_productos`
--

CREATE TABLE `grupo_productos` (
  `grupo_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `linea` varchar(100) DEFAULT NULL,
  `caracteristica1` varchar(200) DEFAULT NULL,
  `caracteristica2` varchar(200) DEFAULT NULL,
  `clave` varchar(100) DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_local`
--

CREATE TABLE `inventario_local` (
  `producto_id` int NOT NULL,
  `local_id` int NOT NULL,
  `stock` int DEFAULT NULL,
  `stock_reservado` int DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `locales`
--

CREATE TABLE `locales` (
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marcas`
--

CREATE TABLE `marcas` (
  `nombre` varchar(100) NOT NULL,
  `pais_origen` varchar(100) DEFAULT NULL,
  `activo` int DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paquetes`
--

CREATE TABLE `paquetes` (
  `nombre` varchar(200) NOT NULL,
  `descripcion` text,
  `clase` varchar(100) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paquete_productos`
--

CREATE TABLE `paquete_productos` (
  `paquete_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int DEFAULT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `codigo` varchar(50) NOT NULL,
  `codigo_barras` varchar(100) DEFAULT NULL,
  `nombre` varchar(200) NOT NULL,
  `descripcion` text,
  `marca` varchar(100) DEFAULT NULL,
  `modelo` varchar(100) DEFAULT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `precio_compra` decimal(10,2) NOT NULL,
  `precio_venta` decimal(10,2) NOT NULL,
  `precio_venta_credito` decimal(10,2) DEFAULT NULL,
  `stock_total` int DEFAULT NULL,
  `stock_minimo` int DEFAULT NULL,
  `ubicacion_estante` varchar(50) DEFAULT NULL,
  `ubicacion_fila` varchar(10) DEFAULT NULL,
  `ubicacion_columna` varchar(10) DEFAULT NULL,
  `compatibilidad` json DEFAULT NULL,
  `año_inicio` int DEFAULT NULL,
  `año_fin` int DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `promociones`
--

CREATE TABLE `promociones` (
  `id` int NOT NULL,
  `descripcion` varchar(120) NOT NULL,
  `activa` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `promociones`
--

INSERT INTO `promociones` (`id`, `descripcion`, `activa`) VALUES
(1, '10% de descuento en filtros de aceite', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `clave` varchar(50) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `rfc` varchar(20) DEFAULT NULL,
  `web` varchar(200) DEFAULT NULL,
  `calle` varchar(200) DEFAULT NULL,
  `numero_exterior` varchar(20) DEFAULT NULL,
  `numero_interior` varchar(20) DEFAULT NULL,
  `colonia` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `municipio` varchar(100) DEFAULT NULL,
  `estado` varchar(100) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `pais` varchar(100) DEFAULT NULL,
  `contacto_compras_nombre` varchar(100) DEFAULT NULL,
  `contacto_compras_email` varchar(100) DEFAULT NULL,
  `contacto_compras_telefono` varchar(20) DEFAULT NULL,
  `lista_precios_compra` varchar(100) DEFAULT NULL,
  `dias_entrega` int DEFAULT NULL,
  `tipo_moneda` enum('PESOS','DOLARES') DEFAULT NULL,
  `descuento_factura` decimal(5,2) DEFAULT NULL,
  `descuento_listas_precio` decimal(5,2) DEFAULT NULL,
  `descuento_producto_factura` decimal(5,2) DEFAULT NULL,
  `notas_compras` text,
  `contacto_finanzas_nombre` varchar(100) DEFAULT NULL,
  `contacto_finanzas_email` varchar(100) DEFAULT NULL,
  `contacto_finanzas_telefono` varchar(20) DEFAULT NULL,
  `forma_pago` enum('CONTADO','CREDITO') DEFAULT NULL,
  `dias_credito` int DEFAULT NULL,
  `saldo` decimal(10,2) DEFAULT NULL,
  `activo` varchar(10) DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `retiros_caja`
--

CREATE TABLE `retiros_caja` (
  `folio` varchar(50) NOT NULL,
  `local_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `monto` decimal(12,2) NOT NULL,
  `fecha_retiro` datetime DEFAULT CURRENT_TIMESTAMP,
  `descripcion` text NOT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `traspasos`
--

CREATE TABLE `traspasos` (
  `folio` varchar(50) NOT NULL,
  `estado` enum('PENDIENTE','EN_TRANSITO','COMPLETADO','CANCELADO') DEFAULT NULL,
  `fecha` datetime NOT NULL,
  `origen_id` int NOT NULL,
  `destino_id` int NOT NULL,
  `notas` text,
  `usuario_id` int DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `nombre` varchar(100) NOT NULL,
  `apellido_paterno` varchar(100) DEFAULT NULL,
  `apellido_materno` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `nombre_usuario` varchar(50) NOT NULL,
  `clave_hash` varchar(255) NOT NULL,
  `rol` enum('ADMINISTRADOR','GERENTE','VENDEDOR','ALMACENISTA','CAJERO') DEFAULT NULL,
  `estado` enum('ACTIVO','INACTIVO','SUSPENDIDO') DEFAULT NULL,
  `local_id` int DEFAULT NULL,
  `ultimo_login` datetime DEFAULT NULL,
  `intentos_fallidos` int DEFAULT NULL,
  `bloqueado_hasta` datetime DEFAULT NULL,
  `debe_cambiar_clave` tinyint(1) DEFAULT NULL,
  `tema_interfaz` varchar(20) DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vales_venta`
--

CREATE TABLE `vales_venta` (
  `folio` varchar(50) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `concepto` varchar(200) DEFAULT NULL,
  `fecha` datetime NOT NULL,
  `vendedor_id` int NOT NULL,
  `local_id` int NOT NULL,
  `usado` tinyint(1) DEFAULT NULL,
  `fecha_uso` datetime DEFAULT NULL,
  `destino` varchar(50) DEFAULT NULL,
  `tipo` enum('VENTA','DEVOLUCION') DEFAULT NULL,
  `disponible` tinyint(1) DEFAULT NULL,
  `descripcion` varchar(500) DEFAULT NULL,
  `venta_origen_id` int DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `folio` varchar(50) NOT NULL,
  `local_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `cliente_id` int DEFAULT NULL,
  `tipo_venta` enum('CONTADO','CREDITO','APARTADO') DEFAULT NULL,
  `estado` enum('PENDIENTE','COMPLETADA','CANCELADA','DEVUELTA') DEFAULT NULL,
  `subtotal` decimal(10,2) DEFAULT NULL,
  `descuento` decimal(10,2) DEFAULT NULL,
  `iva` decimal(10,2) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `pago_recibido` decimal(10,2) DEFAULT NULL,
  `cambio` decimal(10,2) DEFAULT NULL,
  `fecha_limite_pago` datetime DEFAULT NULL,
  `saldo_pendiente` decimal(10,2) DEFAULT NULL,
  `metodo_pago` varchar(50) DEFAULT NULL,
  `id` int NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `arqueos_caja`
--
ALTER TABLE `arqueos_caja`
  ADD PRIMARY KEY (`id`),
  ADD KEY `local_id` (`local_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `ix_arqueos_caja_id` (`id`);

--
-- Indices de la tabla `asistencia_empleados`
--
ALTER TABLE `asistencia_empleados`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_asistencia_nombre_fecha` (`nombre`,`fecha`),
  ADD KEY `ix_asistencia_empleados_fecha` (`fecha`),
  ADD KEY `ix_asistencia_empleados_id` (`id`),
  ADD KEY `ix_asistencia_empleados_nombre` (`nombre`);

--
-- Indices de la tabla `cierres_caja`
--
ALTER TABLE `cierres_caja`
  ADD PRIMARY KEY (`id`),
  ADD KEY `local_id` (`local_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `ix_cierres_caja_id` (`id`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_clientes_email` (`email`),
  ADD UNIQUE KEY `ix_clientes_rfc` (`rfc`),
  ADD KEY `local_id` (`local_id`),
  ADD KEY `ix_clientes_alias` (`alias`),
  ADD KEY `ix_clientes_nombre` (`nombre`),
  ADD KEY `ix_clientes_id` (`id`);

--
-- Indices de la tabla `compras`
--
ALTER TABLE `compras`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_compras_folio` (`folio`),
  ADD KEY `proveedor_id` (`proveedor_id`),
  ADD KEY `local_id` (`local_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `ix_compras_id` (`id`),
  ADD KEY `ix_compras_factura` (`factura`);

--
-- Indices de la tabla `configuracion_sistema`
--
ALTER TABLE `configuracion_sistema`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `clave` (`clave`),
  ADD KEY `idx_clave` (`clave`);

--
-- Indices de la tabla `detalle_compras`
--
ALTER TABLE `detalle_compras`
  ADD PRIMARY KEY (`id`),
  ADD KEY `compra_id` (`compra_id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `ix_detalle_compras_id` (`id`);

--
-- Indices de la tabla `detalle_traspasos`
--
ALTER TABLE `detalle_traspasos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `traspaso_id` (`traspaso_id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `ix_detalle_traspasos_id` (`id`);

--
-- Indices de la tabla `detalle_ventas`
--
ALTER TABLE `detalle_ventas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `venta_id` (`venta_id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `local_id` (`local_id`),
  ADD KEY `ix_detalle_ventas_id` (`id`);

--
-- Indices de la tabla `gastos`
--
ALTER TABLE `gastos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_gastos_folio` (`folio`),
  ADD KEY `ix_gastos_id` (`id`);

--
-- Indices de la tabla `grupos`
--
ALTER TABLE `grupos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_grupos_tipo` (`tipo`),
  ADD KEY `ix_grupos_nombre` (`nombre`),
  ADD KEY `ix_grupos_id` (`id`);

--
-- Indices de la tabla `grupo_aplicaciones`
--
ALTER TABLE `grupo_aplicaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `grupo_id` (`grupo_id`),
  ADD KEY `ix_grupo_aplicaciones_id` (`id`);

--
-- Indices de la tabla `grupo_productos`
--
ALTER TABLE `grupo_productos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `grupo_id` (`grupo_id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `ix_grupo_productos_id` (`id`);

--
-- Indices de la tabla `inventario_local`
--
ALTER TABLE `inventario_local`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `local_id` (`local_id`),
  ADD KEY `ix_inventario_local_id` (`id`);

--
-- Indices de la tabla `locales`
--
ALTER TABLE `locales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_locales_id` (`id`);

--
-- Indices de la tabla `marcas`
--
ALTER TABLE `marcas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_marcas_nombre` (`nombre`),
  ADD KEY `ix_marcas_id` (`id`);

--
-- Indices de la tabla `paquetes`
--
ALTER TABLE `paquetes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_paquetes_clase` (`clase`),
  ADD KEY `ix_paquetes_id` (`id`),
  ADD KEY `ix_paquetes_nombre` (`nombre`);

--
-- Indices de la tabla `paquete_productos`
--
ALTER TABLE `paquete_productos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `paquete_id` (`paquete_id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `ix_paquete_productos_id` (`id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_productos_codigo` (`codigo`),
  ADD UNIQUE KEY `ix_productos_codigo_barras` (`codigo_barras`),
  ADD KEY `ix_productos_id` (`id`);

--
-- Indices de la tabla `promociones`
--
ALTER TABLE `promociones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_promociones_id` (`id`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_proveedores_clave` (`clave`),
  ADD KEY `ix_proveedores_id` (`id`),
  ADD KEY `ix_proveedores_rfc` (`rfc`);

--
-- Indices de la tabla `retiros_caja`
--
ALTER TABLE `retiros_caja`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_retiros_caja_folio` (`folio`),
  ADD KEY `local_id` (`local_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `ix_retiros_caja_id` (`id`);

--
-- Indices de la tabla `traspasos`
--
ALTER TABLE `traspasos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_traspasos_folio` (`folio`),
  ADD KEY `origen_id` (`origen_id`),
  ADD KEY `destino_id` (`destino_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `ix_traspasos_id` (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_usuarios_email` (`email`),
  ADD UNIQUE KEY `ix_usuarios_nombre_usuario` (`nombre_usuario`),
  ADD KEY `local_id` (`local_id`),
  ADD KEY `ix_usuarios_id` (`id`);

--
-- Indices de la tabla `vales_venta`
--
ALTER TABLE `vales_venta`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_vales_venta_folio` (`folio`),
  ADD KEY `vendedor_id` (`vendedor_id`),
  ADD KEY `local_id` (`local_id`),
  ADD KEY `venta_origen_id` (`venta_origen_id`),
  ADD KEY `ix_vales_venta_id` (`id`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_ventas_folio` (`folio`),
  ADD KEY `local_id` (`local_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `ix_ventas_id` (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `arqueos_caja`
--
ALTER TABLE `arqueos_caja`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `asistencia_empleados`
--
ALTER TABLE `asistencia_empleados`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cierres_caja`
--
ALTER TABLE `cierres_caja`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `compras`
--
ALTER TABLE `compras`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `configuracion_sistema`
--
ALTER TABLE `configuracion_sistema`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `detalle_compras`
--
ALTER TABLE `detalle_compras`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_traspasos`
--
ALTER TABLE `detalle_traspasos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_ventas`
--
ALTER TABLE `detalle_ventas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `gastos`
--
ALTER TABLE `gastos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `grupos`
--
ALTER TABLE `grupos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `grupo_aplicaciones`
--
ALTER TABLE `grupo_aplicaciones`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `grupo_productos`
--
ALTER TABLE `grupo_productos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_local`
--
ALTER TABLE `inventario_local`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `locales`
--
ALTER TABLE `locales`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `marcas`
--
ALTER TABLE `marcas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `paquetes`
--
ALTER TABLE `paquetes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `paquete_productos`
--
ALTER TABLE `paquete_productos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `promociones`
--
ALTER TABLE `promociones`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `retiros_caja`
--
ALTER TABLE `retiros_caja`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `traspasos`
--
ALTER TABLE `traspasos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `vales_venta`
--
ALTER TABLE `vales_venta`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `arqueos_caja`
--
ALTER TABLE `arqueos_caja`
  ADD CONSTRAINT `arqueos_caja_ibfk_1` FOREIGN KEY (`local_id`) REFERENCES `locales` (`id`),
  ADD CONSTRAINT `arqueos_caja_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `cierres_caja`
--
ALTER TABLE `cierres_caja`
  ADD CONSTRAINT `cierres_caja_ibfk_1` FOREIGN KEY (`local_id`) REFERENCES `locales` (`id`),
  ADD CONSTRAINT `cierres_caja_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`local_id`) REFERENCES `locales` (`id`);

--
-- Filtros para la tabla `compras`
--
ALTER TABLE `compras`
  ADD CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`),
  ADD CONSTRAINT `compras_ibfk_2` FOREIGN KEY (`local_id`) REFERENCES `locales` (`id`),
  ADD CONSTRAINT `compras_ibfk_3` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `detalle_compras`
--
ALTER TABLE `detalle_compras`
  ADD CONSTRAINT `detalle_compras_ibfk_1` FOREIGN KEY (`compra_id`) REFERENCES `compras` (`id`),
  ADD CONSTRAINT `detalle_compras_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `detalle_traspasos`
--
ALTER TABLE `detalle_traspasos`
  ADD CONSTRAINT `detalle_traspasos_ibfk_1` FOREIGN KEY (`traspaso_id`) REFERENCES `traspasos` (`id`),
  ADD CONSTRAINT `detalle_traspasos_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `detalle_ventas`
--
ALTER TABLE `detalle_ventas`
  ADD CONSTRAINT `detalle_ventas_ibfk_1` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`),
  ADD CONSTRAINT `detalle_ventas_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`),
  ADD CONSTRAINT `detalle_ventas_ibfk_3` FOREIGN KEY (`local_id`) REFERENCES `locales` (`id`);

--
-- Filtros para la tabla `grupo_aplicaciones`
--
ALTER TABLE `grupo_aplicaciones`
  ADD CONSTRAINT `grupo_aplicaciones_ibfk_1` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`);

--
-- Filtros para la tabla `grupo_productos`
--
ALTER TABLE `grupo_productos`
  ADD CONSTRAINT `grupo_productos_ibfk_1` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`),
  ADD CONSTRAINT `grupo_productos_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `inventario_local`
--
ALTER TABLE `inventario_local`
  ADD CONSTRAINT `inventario_local_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`),
  ADD CONSTRAINT `inventario_local_ibfk_2` FOREIGN KEY (`local_id`) REFERENCES `locales` (`id`);

--
-- Filtros para la tabla `paquete_productos`
--
ALTER TABLE `paquete_productos`
  ADD CONSTRAINT `paquete_productos_ibfk_1` FOREIGN KEY (`paquete_id`) REFERENCES `paquetes` (`id`),
  ADD CONSTRAINT `paquete_productos_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `retiros_caja`
--
ALTER TABLE `retiros_caja`
  ADD CONSTRAINT `retiros_caja_ibfk_1` FOREIGN KEY (`local_id`) REFERENCES `locales` (`id`),
  ADD CONSTRAINT `retiros_caja_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `traspasos`
--
ALTER TABLE `traspasos`
  ADD CONSTRAINT `traspasos_ibfk_1` FOREIGN KEY (`origen_id`) REFERENCES `locales` (`id`),
  ADD CONSTRAINT `traspasos_ibfk_2` FOREIGN KEY (`destino_id`) REFERENCES `locales` (`id`),
  ADD CONSTRAINT `traspasos_ibfk_3` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`local_id`) REFERENCES `locales` (`id`);

--
-- Filtros para la tabla `vales_venta`
--
ALTER TABLE `vales_venta`
  ADD CONSTRAINT `vales_venta_ibfk_1` FOREIGN KEY (`vendedor_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `vales_venta_ibfk_2` FOREIGN KEY (`local_id`) REFERENCES `locales` (`id`),
  ADD CONSTRAINT `vales_venta_ibfk_3` FOREIGN KEY (`venta_origen_id`) REFERENCES `ventas` (`id`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`local_id`) REFERENCES `locales` (`id`),
  ADD CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `ventas_ibfk_3` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
