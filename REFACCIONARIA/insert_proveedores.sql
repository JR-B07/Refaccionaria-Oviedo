-- Agregar proveedores de ejemplo
INSERT INTO proveedores (nombre, razon_social, rfc, telefono, email, direccion, ciudad, estado, codigo_postal, dias_credito, limite_credito, descuento, tipo_proveedor, activo) 
VALUES 
('AUTOPARTES DEL NORTE', 'Autopartes del Norte S.A. de C.V.', 'ADN850623G45', '8181234567', 'ventas@autopartesnorte.com.mx', 'Av. Industria #123', 'Monterrey', 'Nuevo León', '64000', 30, 150000.00, 5.0, 'NACIONAL', 1),
('REFACCIONES GARCIA', 'Refacciones García y Asociados S.C.', 'RGA920415H78', '3338765432', 'pedidos@refaccionesgarcia.com', 'Blvd. Tlaquepaque #456', 'Guadalajara', 'Jalisco', '44100', 15, 80000.00, 3.0, 'NACIONAL', 1),
('LUBRICANTES SUPREMOS', 'Lubricantes Supremos de México S.A.', 'LSM880307K21', '5555123456', 'contacto@lubricantesupremos.mx', 'Calz. de Tlalpan #789', 'Ciudad de México', 'CDMX', '03100', 45, 250000.00, 8.0, 'NACIONAL', 1),
('FILTROS PREMIUM', 'Distribuidora de Filtros Premium S.A.', 'DFP900512M34', '4424567890', 'info@filtrospremium.com.mx', 'Av. Constitución #321', 'Querétaro', 'Querétaro', '76000', 20, 100000.00, 4.5, 'NACIONAL', 1),
('FRENOS INDUSTRIALES', 'Frenos Industriales de Occidente S.A.', 'FIO931128N56', '3337654321', 'ventas@frenosindustriales.com', 'Carr. a Zapopan #654', 'Guadalajara', 'Jalisco', '44500', 30, 120000.00, 6.0, 'NACIONAL', 1);
