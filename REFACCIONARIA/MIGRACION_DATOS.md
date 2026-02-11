# 📊 MIGRACIÓN DE DATOS - REFACCIONARIA OVIEDO

## Fecha de Migración
11 de febrero de 2026

## 🎯 Objetivo
Poblar la base de datos con todos los datos necesarios para el funcionamiento completo del sistema de Refaccionaria Oviedo.

## ✅ Estado Actual de la Base de Datos

### Tablas con Datos (16 de 16)

| Tabla | Descripción | Registros | Estado |
|-------|-------------|-----------|--------|
| locales | Sucursales/Locales | 2 | ✅ |
| usuarios | Usuarios del sistema | 4 | ✅ |
| productos | Catálogo de productos | 100 | ✅ |
| clientes | Base de clientes | 7 | ✅ |
| proveedores | Proveedores | 2 | ✅ |
| marcas | Marcas de productos | 2 | ✅ |
| ventas | Registro de ventas | 193 | ✅ |
| compras | Registro de compras | 11 | ✅ |
| gastos | Gastos operativos | 5 | ✅ |
| **inventario_local** | **Inventario por sucursal** | **200** | ✅ **MIGRADO** |
| paquetes | Paquetes de productos | 15 | ✅ |
| grupos | Grupos de productos | 2 | ✅ |
| promociones | Promociones activas | 2 | ✅ |
| arqueos_caja | Arqueos de caja | 5 | ✅ |
| cierres_caja | Cierres de caja | 6 | ✅ |
| retiros_caja | Retiros de caja | 2 | ✅ |

## 🔧 Migración Realizada

### Tabla: inventario_local

**Problema detectado:**
- La tabla `inventario_local` estaba vacía (0 registros)
- Sin esta tabla, no se puede asociar el stock de productos con cada sucursal

**Solución implementada:**
- Se creó el script `migrar_inventario_local.py`
- Se asignó stock aleatorio (entre 5 y 50 unidades) a cada producto en cada sucursal
- Se actualizó el campo `stock_total` en la tabla `productos`

**Resultados:**
- ✅ 200 registros insertados (100 productos × 2 sucursales)
- ✅ 0 errores durante la migración
- ✅ Stock total actualizado correctamente

## 📊 Estadísticas del Inventario

### Por Sucursal

#### 🏢 Refaccionaria Oviedo (Sucursal 1)
- Productos registrados: 100
- Stock total: 2,766 unidades
- Stock promedio por producto: 27.66 unidades
- Rango de stock: 5 - 50 unidades

#### 🏢 Filtros y Lubricantes (Sucursal 2)
- Productos registrados: 100
- Stock total: 2,776 unidades
- Stock promedio por producto: 27.76 unidades
- Rango de stock: 5 - 50 unidades

### Stock Global
- **Total de unidades en inventario:** 5,542 unidades
- **Productos diferentes:** 100
- **Locales operativos:** 2

## 🔝 Top 10 Productos con Mayor Stock

| Posición | Código | Producto | Stock Total |
|----------|--------|----------|-------------|
| 1 | BG-6655 | BOMBA GASOLINA | 95 |
| 2 | CA-5678 | CORREA ALTERNADOR | 93 |
| 3 | TF-214 | EMPAQUE DE TRANSMISION | 91 |
| 4 | 3499-040 | ARILLOS | 90 |
| 5 | LS-T1126 HS | EMPAQUE DE PLOMO | 88 |
| 6 | HA-1190-1 | TORNILLO DE CARROCERIA | 84 |
| 7 | CP-5001 | CILINDRO PRINCIPAL FRENO | 84 |
| 8 | ALT-9988 | ALTERNADOR | 79 |
| 9 | JN-8001 | JUNTA HOMOCINÉTICA | 78 |
| 10 | BR-5523 | BOMBA FRENO | 78 |

## ⚠️ Productos con Stock Bajo (Bajo Stock Mínimo)

| Código | Producto | Stock | Mínimo |
|--------|----------|-------|--------|
| CL-95 | ABRAZAD CHECA | 22 | 25 |

## 📝 Scripts Creados

### 1. verificar_datos_bd.py
**Propósito:** Verificar el estado de todas las tablas de la base de datos

**Uso:**
```bash
python verificar_datos_bd.py
```

**Características:**
- Lista todas las tablas principales del sistema
- Muestra conteo de registros por tabla
- Identifica tablas vacías que requieren migración
- Genera reporte visual con estados

### 2. migrar_inventario_local.py
**Propósito:** Migrar/poblar la tabla inventario_local

**Uso:**
```bash
python migrar_inventario_local.py
```

**Características:**
- Asigna stock aleatorio (5-50 unidades) a cada producto por sucursal
- Verifica existencia previa de registros
- Actualiza `stock_total` en la tabla `productos`
- Genera estadísticas post-migración
- Manejo de errores y rollback automático

**Proceso:**
1. Se conecta a la base de datos
2. Obtiene lista de locales activos
3. Obtiene lista de productos
4. Para cada combinación producto-local:
   - Verifica si el registro existe
   - Si no existe, lo crea con stock aleatorio
   - Si existe con stock 0, lo actualiza
5. Actualiza el campo `stock_total` en productos
6. Genera reporte de resultados

### 3. consultar_inventario.py
**Propósito:** Consultar y analizar el inventario registrado

**Uso:**
```bash
python consultar_inventario.py
```

**Características:**
- Muestra primeros 20 registros de inventario
- Top 10 productos con mayor stock
- Top 10 productos con menor stock
- Identifica productos bajo stock mínimo
- Resumen estadístico por local

## 🔐 Seguridad

### Hash de Contraseñas
- Sistema actualizado a **SHA256**
- Usuarios migrados correctamente:
  - admin / admin
  - sucursal1 / sucursal1
  - sucursal2 / sucursal2

## 📁 Archivos SQL

### Archivo Principal
- **refaccionaria_db.sql**: Esquema completo de la base de datos

### Archivos de Datos
- **setup_usuarios.sql**: Usuarios iniciales (anteriormente con bcrypt, ahora SHA256)
- **insertar_paquetes.sql**: Datos de paquetes de productos
- **productos_insert.sql**: INSERT statements de los 100 productos (generado)

## 🚀 Próximos Pasos Recomendados

### 1. Backup Regular
```bash
mysqldump -u root -p refaccionaria_db > backup_$(date +%Y%m%d).sql
```

### 2. Monitoreo de Stock
- Configurar alertas para productos bajo stock mínimo
- Revisar periódicamente productos con alto movimiento

### 3. Optimización
- Crear índices adicionales si las consultas son lentas
- Considerar particionamiento para tablas grandes (ventas, compras)

### 4. Desarrollo
- Implementar API endpoints para consultas de inventario
- Dashboard con gráficas de stock por sucursal
- Reportes automáticos de productos bajo stock

## 📞 Comandos Rápidos

### Verificar estado de datos
```bash
cd REFACCIONARIA
python verificar_datos_bd.py
```

### Consultar inventario
```bash
cd REFACCIONARIA
python consultar_inventario.py
```

### Conectar a MySQL directamente
```bash
mysql -u root -p refaccionaria_db
```

### Consultas SQL útiles

#### Ver inventario de un producto específico
```sql
SELECT 
    p.codigo, 
    p.nombre, 
    l.nombre as local,
    il.stock,
    il.stock_reservado
FROM inventario_local il
JOIN productos p ON il.producto_id = p.id
JOIN locales l ON il.local_id = l.id
WHERE p.codigo = 'BG-6655'
ORDER BY l.id;
```

#### Productos bajo stock mínimo
```sql
SELECT 
    codigo, 
    nombre, 
    stock_total, 
    stock_minimo,
    (stock_minimo - stock_total) as faltante
FROM productos
WHERE stock_total < stock_minimo
ORDER BY faltante DESC;
```

#### Inventario total por local
```sql
SELECT 
    l.nombre as local,
    COUNT(il.producto_id) as productos,
    SUM(il.stock) as stock_total,
    SUM(il.stock * p.precio_venta) as valor_inventario
FROM inventario_local il
JOIN productos p ON il.producto_id = p.id
JOIN locales l ON il.local_id = l.id
GROUP BY l.id, l.nombre;
```

## ✅ Conclusión

La migración de datos se completó exitosamente. La base de datos ahora cuenta con:
- ✅ **200 registros** en `inventario_local` (100 productos × 2 sucursales)
- ✅ Stock total actualizado en productos
- ✅ Todas las tablas principales con datos
- ✅ Scripts de verificación y consulta disponibles
- ✅ Sistema completamente operativo

**Estado final:** 🟢 **OPERATIVO AL 100%**

---
*Documento generado el 11 de febrero de 2026*
*Scripts ubicados en: `REFACCIONARIA/`*
