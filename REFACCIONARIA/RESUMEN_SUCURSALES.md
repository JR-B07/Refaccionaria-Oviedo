# 🎉 SISTEMA COMPLETO PARA 2 SUCURSALES

## ✅ LO QUE SE HA IMPLEMENTADO

### 1️⃣ Componente Reutilizable
**Ubicación:** `app/static/componentes/selector-sucursal.js`

Este archivo contiene funciones que puedes usar en cualquier vista:

```javascript
// Cargar selector en un <select id="sucursalSelect">
inicializarSelectorSucursal('sucursalSelect', (localId) => {
    console.log('Usuario cambió a sucursal:', localId);
});

// Obtener el ID de la sucursal seleccionada
const localId = obtenerLocalIdSeleccionado('sucursalSelect');

// Obtener el nombre de la sucursal
const nombre = obtenerNombreSucursal(localId); // "REFACCIONARIA OVIEDO"
```

---

### 2️⃣ Vistas Funcionales

#### 📋 **Nueva Venta** (`nueva_venta.html`)
- ✅ Selector de sucursal en toolbar
- ✅ Selecciona sucursal antes de crear venta
- ✅ Al guardar, incluye `local_id` en los datos
- ✅ Cada vendedor ve sus propias ventas por sucursal

**Cómo funciona:**
1. Entra a Nueva Venta
2. El selector muestra: "REFACCIONARIA OVIEDO" o "REFACCIÓN PARA OVIEDO"
3. El dropdown por defecto carga la sucursal del usuario
4. Al guardar una venta, se guarda con su `local_id`

#### 📊 **Cierres de Caja** (`cajas_cierre.html`)
- ✅ Dos pestañas, una para cada sucursal
- ✅ Selector en la parte superior
- ✅ Al cambiar selector, cambia a la pestaña correspondiente
- ✅ Cada tabla carga cierres solo de esa sucursal
- ✅ Menú con opciones por sucursal

**Cómo funciona:**
1. Entra a Cierres de Caja
2. Verás dos pestañas: "REFACCIONARIA OVIEDO" | "REFACCIÓN PARA OVIEDO"
3. El selector permite cambiar entre sucursales rápidamente
4. Cada pestaña muestra SOLO los cierres de esa sucursal
5. Al crear nuevo cierre, aparece en la pestaña correcta

#### 🔍 **Arqueos de Caja** (`arqueos_caja.html`)
- ✅ Selector de local para crear arqueos
- ✅ Filtro de local para listar arqueos
- ✅ Todos los arqueos se guardan con su `local_id`
- ✅ Ya tiene funciones para cargar locales desde API

**Cómo funciona:**
1. Entra a Arqueos
2. Selecciona local en "Nuevo Arqueo"
3. Crea el arqueo (se guarda con local_id)
4. En "Listar Arqueos" filtra por local también

---

## 🏗️ ARQUITECTURA

### Flujo de Datos

```
┌─────────────────────────────────────────┐
│  LOGIN                                   │
│  Usuario asignado a sucursal (local_id) │
│  Se guarda en localStorage.user.local_id│
└──────────────┬──────────────────────────┘
               │
        ┌──────▼─────────┐
        │ VISTAS PRINCIPALES
        │ - nueva_venta.html
        │ - cajas_cierre.html
        │ - arqueos_caja.html
        └──────┬─────────┘
               │
      ┌────────▼────────┐
      │ Selector Sucursal
      │ (componente .js)
      │ Lee local_id del usuario
      │ Permite cambiar sucursal
      └────────┬────────┘
               │
      ┌────────▼─────────────┐
      │ Cada acción envía:
      │ - POST /ventas        → {local_id: X}
      │ - POST /arqueos       → {local_id: X}
      │ - POST /cierres       → {local_id: X}
      │ - GET /cierres        → ?local_id=X
      └────────┬─────────────┘
               │
      ┌────────▼─────────────┐
      │ API Backend
      │ Filtra por local_id
      │ Cada sucursal ve solo
      │ sus propios datos
      └──────────────────────┘
```

### Bases de Datos

**Usuarios:**
```
id | nombre | local_id | ...
1  | Juan   | 1        |  ← REFACCIONARIA OVIEDO
2  | María  | 2        |  ← REFACCIÓN PARA OVIEDO
3  | Pedro  | 1        |  ← REFACCIONARIA OVIEDO
```

**Ventas, Cierres, Arqueos:**
```
id | fecha | local_id | ...
1  | ...   | 1        |  ← Sucursal 1
2  | ...   | 2        |  ← Sucursal 2
3  | ...   | 1        |  ← Sucursal 1
```

**Productos, Paquetes, Proveedores:**
```
id | nombre | ...
1  | Aceite | ... ← SIN local_id (COMPARTIDO)
2  | Bujía  | ...
```

---

## 🚀 CÓMO AGREGAR A OTRAS VISTAS

### Para agregar selector a una nueva vista:

**1. En el `<head>`:**
```html
<script src="componentes/selector-sucursal.js"></script>
```

**2. En el HTML (donde quieras el selector):**
```html
<select id="sucursalSelect"></select>
```

**3. En el `<script>` (en DOMContentLoaded):**
```javascript
document.addEventListener('DOMContentLoaded', () => {
    inicializarSelectorSucursal('sucursalSelect', (localId) => {
        console.log('Nueva sucursal:', localId);
        // Recargar datos, cambiar tab, etc.
    });
});
```

**4. Cuando guardes datos:**
```javascript
const localId = obtenerLocalIdSeleccionado('sucursalSelect');
const datos = {
    // tus datos...
    local_id: localId
};
```

---

## 📱 Vistas que NECESITAN este tratamiento

```
✅ LISTO:
- nueva_venta.html      ✓ Selector + local_id
- cajas_cierre.html     ✓ Dos tablas + selector
- arqueos_caja.html     ✓ Locales integrados

⏳ POR HACER (si lo necesitas):
- traspasos.html        → Transferencia entre sucursales
- tickets.html          → Filtrar por sucursal
- vales_venta.html      → Emitir por sucursal
- reportes.html         → Reportes por sucursal
- rrhh.html             → Personal por sucursal

🔄 COMPARTIDAS (NO agregar selector):
- productos.html        → Inventario compartido
- paquetes.html         → Paquetes compartidos
- proveedores.html      → Proveedores compartidos
- clientes.html         → Clientes compartidos
```

---

## 🔧 VERIFICACIONES NECESARIAS

Para que todo funcione correctamente, verifica que:

### ✅ Backend (Python/FastAPI)

1. **Modelo Usuario:**
   ```python
   class Usuario(Base):
       local_id = Column(Integer, ForeignKey("locales.id"))
   ```

2. **Modelo Venta:**
   ```python
   class Venta(Base):
       local_id = Column(Integer, ForeignKey("locales.id"))
   ```

3. **Modelo Arqueo:**
   ```python
   class Arqueo(Base):
       local_id = Column(Integer, ForeignKey("locales.id"))
   ```

4. **Endpoints filtren por local_id:**
   ```python
   # GET /api/v1/ventas?local_id=1
   if local_id:
       query = query.filter(Venta.local_id == local_id)
   
   # POST /api/v1/ventas
   venta.local_id = payload.local_id  # ← Recibe del frontend
   ```

### ✅ Frontend (localStorage)

```javascript
// Después del login, localStorage debe tener:
localStorage.user = JSON.stringify({
    id: 1,
    username: "juan",
    local_id: 1,  // ← IMPORTANTE
    // ...otros datos
});
```

---

## 📞 RESUMEN RÁPIDO

| Qué | Dónde | Estado |
|-----|-------|--------|
| Componente selector | `componentes/selector-sucursal.js` | ✅ |
| Nueva venta | `nueva_venta.html` | ✅ |
| Cierres de caja | `cajas_cierre.html` | ✅ |
| Arqueos | `arqueos_caja.html` | ✅ |
| Documentación | `PLAN_DOS_SUCURSALES.md` | ✅ |

---

**¡Tu sistema está listo para 2 sucursales! 🎉**

Cada sucursal tiene:
- ✅ Usuarios asignados
- ✅ Ventas por sucursal
- ✅ Cierres de caja separados
- ✅ Arqueos independientes
- ✅ Inventario compartido

---

Fecha: 26 de enero de 2026
