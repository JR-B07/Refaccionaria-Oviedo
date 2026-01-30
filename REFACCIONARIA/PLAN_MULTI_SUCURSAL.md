# IMPLEMENTACIÓN MULTI-SUCURSAL - FASE 1
## Sistema de 2 Sucursales

---

## ✅ PASO 1: ESTRUCTURA BASE (COMPLETADO)

### Scripts Creados:
1. **`scripts/crear_sucursales.py`**
   - Crea las 2 sucursales iniciales en la base de datos
   - Verifica si ya existen antes de crear

2. **`scripts/asignar_sucursales_usuarios.py`**
   - Asigna sucursal a usuarios existentes
   - Por defecto asigna a Sucursal Principal

3. **`setup_sucursales.bat`**
   - Ejecuta ambos scripts automáticamente
   - Fácil de usar para configuración inicial

### Cómo ejecutar:
```bash
# Opción 1: Ejecutar el batch (Windows)
setup_sucursales.bat

# Opción 2: Ejecutar manualmente
python scripts/crear_sucursales.py
python scripts/asignar_sucursales_usuarios.py
```

---

## 📋 PASO 2: MODIFICACIONES AL LOGIN (SIGUIENTE)

### Cambios necesarios:
1. **Backend (`app/api/v1/auth.py`)**:
   - Incluir `local_id` y `local_nombre` en la respuesta del login
   - Agregar endpoint para obtener sucursales disponibles

2. **Frontend (`app/static/js/login.js`)**:
   - Guardar `sucursal_id` y `sucursal_nombre` en localStorage
   - Mostrar sucursal del usuario después del login

3. **Dashboard**:
   - Mostrar sucursal actual en el header
   - (Opcional) Permitir cambiar de sucursal si el usuario tiene permisos

---

## 📋 PASO 3: SELECTOR DE SUCURSAL EN VISTAS (DESPUÉS)

### Módulos a modificar (en orden de prioridad):

1. **Ventas**
   - Filtrar ventas por sucursal
   - Mostrar selector en lista de ventas
   - Registrar sucursal_id en nueva venta

2. **Inventario/Productos**
   - Ver inventario por sucursal
   - Stock separado por sucursal

3. **Compras**
   - Filtrar compras por sucursal
   - Asignar compra a sucursal

4. **Devoluciones**
   - Filtrar por sucursal
   - Ya tienes la vista de devoluciones_compra.html

5. **Reportes**
   - Agregar filtro de sucursal en todos los reportes
   - Ventas Netas (ya creado)
   - Ventas Detalladas (ya creado)

6. **Caja**
   - Arqueos por sucursal
   - Cierres por sucursal
   - Retiros por sucursal

---

## 🎯 ESTADO ACTUAL

### ✅ Completado:
- Modelo de datos (Local/Sucursal) - Ya existía
- Relación Usuario -> Sucursal - Ya existía
- Scripts de configuración inicial

### 🔄 En progreso:
- Implementación del selector de sucursal

### ⏳ Pendiente:
- Modificar API endpoints para filtrar por sucursal
- Actualizar vistas frontend
- Agregar selector de sucursal en reportes

---

## 📝 NOTAS IMPORTANTES

1. **Compatibilidad**: El sistema actual ya tiene soporte para sucursales en el modelo de datos
2. **Migración**: Los usuarios existentes se asignarán a la Sucursal Principal por defecto
3. **Permisos**: Los administradores podrán ver datos de todas las sucursales
4. **Implementación gradual**: Se irá módulo por módulo para evitar problemas

---

## 🚀 SIGUIENTES PASOS INMEDIATOS

1. **Ejecutar setup_sucursales.bat** para crear las sucursales
2. **Modificar el login** para incluir información de sucursal
3. **Agregar selector visual** en el dashboard
4. **Comenzar con el módulo de Ventas** (el más usado)

---

¿Deseas que continúe con el Paso 2 (modificaciones al login)?
