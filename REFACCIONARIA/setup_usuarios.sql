-- =============================================================================
-- SCRIPT DE CREACIÓN DE USUARIOS Y PERFILES
-- =============================================================================
-- Este script crea los usuarios principales del sistema directamente en MySQL
-- Ejecutar: mysql -u root -p < setup_usuarios.sql
-- O desde MySQL: source setup_usuarios.sql;
-- =============================================================================

USE refaccionaria_db;

-- =============================================================================
-- 1. LIMPIAR USUARIOS EXISTENTES (opcional, descomentar si es necesario)
-- =============================================================================
-- DELETE FROM usuarios WHERE nombre_usuario IN ('sucursal1', 'sucursal2', 'admin', 'almacenero');

-- =============================================================================
-- 2. CREAR USUARIO ADMINISTRADOR
-- =============================================================================
INSERT INTO usuarios (
    nombre_usuario,
    contrasena,
    email,
    nombre_empleado,
    rol,
    sucursal_id,
    estado,
    es_administrador,
    fecha_creacion
) VALUES (
    'admin',
    '$2b$12$eImiTXuWVxfaHNAVZ3/hu.pHTwbDlHjGp5ZWPvW/Lo4u/syJlS9LK', -- bcrypt hash de: admin123
    'admin@refaccionaria.com',
    'Administrador',
    'ADMIN',
    1,
    1,
    1,
    NOW()
)
ON DUPLICATE KEY UPDATE nombre_usuario=nombre_usuario; -- No duplicar si existe

-- =============================================================================
-- 3. CREAR USUARIO SUCURSAL 1
-- =============================================================================
INSERT INTO usuarios (
    nombre_usuario,
    contrasena,
    email,
    nombre_empleado,
    rol,
    sucursal_id,
    estado,
    es_administrador,
    fecha_creacion
) VALUES (
    'sucursal1',
    '$2b$12$9bwyCCGS6RXMSzPwbGKE.uPCZzQKzY4xqNqNxPx7H.LxD5h.kEgvm', -- bcrypt hash de: sucursal123
    'sucursal1@refaccionaria.com',
    'Usuario Sucursal 1',
    'VENDEDOR',
    1,
    1,
    0,
    NOW()
)
ON DUPLICATE KEY UPDATE nombre_usuario=nombre_usuario;

-- =============================================================================
-- 4. CREAR USUARIO SUCURSAL 2
-- =============================================================================
INSERT INTO usuarios (
    nombre_usuario,
    contrasena,
    email,
    nombre_empleado,
    rol,
    sucursal_id,
    estado,
    es_administrador,
    fecha_creacion
) VALUES (
    'sucursal2',
    '$2b$12$9bwyCCGS6RXMSzPwbGKE.uPCZzQKzY4xqNqNxPx7H.LxD5h.kEgvm', -- bcrypt hash de: sucursal123
    'sucursal2@refaccionaria.com',
    'Usuario Sucursal 2',
    'VENDEDOR',
    2,
    1,
    0,
    NOW()
)
ON DUPLICATE KEY UPDATE nombre_usuario=nombre_usuario;

-- =============================================================================
-- 5. CREAR USUARIO ALMACENERO
-- =============================================================================
INSERT INTO usuarios (
    nombre_usuario,
    contrasena,
    email,
    nombre_empleado,
    rol,
    sucursal_id,
    estado,
    es_administrador,
    fecha_creacion
) VALUES (
    'almacenero',
    '$2b$12$9bwyCCGS6RXMSzPwbGKE.uPCZzQKzY4xqNqNxPx7H.LxD5h.kEgvm', -- bcrypt hash de: sucursal123
    'almacenero@refaccionaria.com',
    'Usuario Almacenero',
    'ALMACENERO',
    1,
    1,
    0,
    NOW()
)
ON DUPLICATE KEY UPDATE nombre_usuario=nombre_usuario;

-- =============================================================================
-- 6. VERIFICAR USUARIOS CREADOS
-- =============================================================================
SELECT 
    usuario_id,
    nombre_usuario,
    email,
    nombre_empleado,
    rol,
    sucursal_id,
    estado,
    es_administrador,
    fecha_creacion
FROM usuarios
WHERE nombre_usuario IN ('admin', 'sucursal1', 'sucursal2', 'almacenero')
ORDER BY usuario_id;

-- =============================================================================
-- NOTAS IMPORTANTES:
-- =============================================================================
-- Contraseñas usadas (bcrypt hashed):
-- - admin: admin123
-- - sucursal1: sucursal123
-- - sucursal2: sucursal123
-- - almacenero: sucursal123
--
-- Para generar nuevos hashes bcrypt, usar Python:
-- python -c "import bcrypt; print(bcrypt.hashpw(b'tu_password', bcrypt.gensalt()).decode())"
-- =============================================================================
