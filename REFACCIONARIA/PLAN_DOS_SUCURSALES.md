# Plan de Implementación: Sistema para 2 Sucursales

## ✅ COMPLETADO

### Componentes Creados ✅
- `selector-sucursal.js` - Componente reutilizable con funciones:
  - `inicializarSelectorSucursal(selectId, callback)` - Carga el selector
  - `obtenerLocalIdDefecto()` - Obtiene local_id del usuario o URL
  - `obtenerLocalIdSeleccionado(selectId)` - Lee el valor seleccionado
  - `obtenerNombreSucursal(localId)` - Traduce ID a nombre
  - `obtenerLocalIdUsuario()` - Extrae local_id de localStorage

- `selector-sucursal.css` - Estilos para selector (opcional)

### Vistas Integradas ✅
1. **nueva_venta.html**
   - ✅ Script del componente cargado
   - ✅ Selector en toolbar
   - ✅ Función `cambiarSucursal(value)` implementada
   - ✅ `local_id` se agrega a datos guardados
   - ✅ Inicialización en DOMContentLoaded

2. **cajas_cierre.html**
   - ✅ Script del componente cargado
   - ✅ Dos tablas separadas con pestañas (ya existente)
   - ✅ Selector de sucursal integrado
   - ✅ Cambio automático de pestaña al seleccionar sucursal
   - ✅ Funciones `inicializarSucursales()` y `cambiarSucursal()` activas

3. **arqueos_caja.html**
   - ✅ Script del componente cargado
   - ✅ Ya tiene `cargarLocales()` que llena los selects
   - ✅ Selects existentes: `#local_id` y `#filterLocal`
   - ✅ Función `guardarArqueo(event)` ya envía local_id

## 📋 FUNCIONAL

### Características Implementadas:

**1. Usuario + Sucursal**
- Usuario tiene `local_id` en la BD
- Login debe asignar `local_id` al usuario
- localStorage.user debe contener `local_id`

**2. Venta (nueva_venta.html)**
- Selector muestra ambas sucursales
- Al guardar venta, incluye `local_id`
- API espera POST con `local_id`

**3. Cierres de Caja (cajas_cierre.html)**
- Dos tablas separadas (pestaña por sucursal)
- Selector cambia automáticamente entre pestañas
- API filtra por `local_id`

**4. Arqueos de Caja (arqueos_caja.html)**
- Selector de local para crear arqueos
- Filtro de local para listar arqueos
- Todos se guardan con `local_id`

## 🔧 PRÓXIMOS PASOS (Si necesitas continuar)

### Vistas que NECESITAN selector:
```
- traspasos.html (transferir entre sucursales)
- tickets.html (filtrar por sucursal)
- vales_venta.html (emitir por sucursal)
- reportes.html (filtrar reportes por sucursal)
- rrhh.html (personal por sucursal)
```

### Vistas que NO necesitan selector (compartidas):
```
- productos.html (inventario compartido)
- paquetes.html (paquetes compartidos)
- proveedores.html (proveedores compartidos)
- clientes.html (clientes compartidos)
```

## 🔌 Validación de Backend Requerida

Verifica que tus endpoints API tengan:

```python
# Modelos - Agrega local_id donde sea necesario
- Usuario.local_id ✅
- CierreCaja.local_id ✅
- Venta.local_id (NECESARIO)
- Arqueo.local_id (NECESARIO)
- Traspaso.local_id_origen, local_id_destino (NECESARIO)

# Endpoints que DEBEN filtrar por local_id
- GET /api/v1/cajas/cierres?local_id={id} ✅
- GET /api/v1/arqueos?local_id={id} (Necesario)
- GET /api/v1/ventas?local_id={id} (Necesario)
- POST /api/v1/ventas (Necesario recibir local_id)
- POST /api/v1/cajas/cierres (Necesario recibir local_id)

# Endpoints SIN local_id (compartidos)
- GET /api/v1/productos (todos los productos)
- GET /api/v1/paquetes (todos los paquetes)
```

## 🚀 USO DEL COMPONENTE

En cualquier HTML nuevo, para agregar selector de sucursal:

```html
<head>
    <script src="componentes/selector-sucursal.js"></script>
    <link rel="stylesheet" href="componentes/selector-sucursal.css">
</head>

<body>
    <!-- En el HTML -->
    <select id="sucursalSelect"></select>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // Opción 1: Sin callback
            inicializarSelectorSucursal('sucursalSelect');

            // Opción 2: Con callback personalizado
            inicializarSelectorSucursal('sucursalSelect', (localId) => {
                console.log('Sucursal seleccionada:', localId);
                // Recargar datos, cambiar tab, etc.
            });
        });
    </script>
</body>
```

## 📊 Funciones Disponibles del Componente

```javascript
// Inicializar selector
inicializarSelectorSucursal('idSelector', callback)

// Obtener valores
obtenerLocalIdSeleccionado('idSelector')      // El valor actual
obtenerLocalIdDefecto()                       // Del usuario o URL
obtenerLocalIdUsuario()                       // Del localStorage
obtenerNombreSucursal(localId)               // "REFACCIONARIA OVIEDO"
```

## ✨ Estado Actual

**Proyecto funcional para 2 sucursales:**
- ✅ Usuarios asignados a sucursales
- ✅ Ventas por sucursal
- ✅ Cierres de caja por sucursal (con interfaz de pestañas)
- ✅ Arqueos por sucursal
- ✅ Componente reutilizable para otros módulos
- ⏳ Pendiente: Traspasos entre sucursales
- ⏳ Pendiente: Verificar inventario compartido

---

**Fecha de implementación:** 26 de enero de 2026

