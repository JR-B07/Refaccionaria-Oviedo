-- Insertar 2 paquetes de ejemplo
DELETE FROM paquetes WHERE nombre LIKE 'Kit%';

INSERT INTO paquetes (nombre, clase, descripcion, local_id, activo, fecha_creacion, fecha_actualizacion) 
VALUES 
  ('Kit Suspensión Delantera', 'Suspensión', 'Kit completo de suspensión delantera con amortiguadores y resortes', 1, 1, NOW(), NOW()),
  ('Kit Frenos Completo', 'Frenos', 'Sistema de frenos completo con pastillas, discos y mangueras', 1, 1, NOW(), NOW());

SELECT id, nombre, clase, descripcion FROM paquetes;
