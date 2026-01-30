# 🔗 Cómo Integrar "ARQUEOS DE CAJA" en el Dashboard

## Opción 1: Agregar un Botón en el Dashboard (Recomendado)

Si tu `dashboard.html` tiene botones de menú, agrega este código:

```html
<!-- Botón para Arqueos de Caja -->
<div class="menu-item">
    <a href="/static/arqueos_caja.html">
        <span class="icon">📋</span>
        <span class="label">Arqueos de Caja</span>
    </a>
</div>
```

O si usa tarjetas:

```html
<div class="card-menu">
    <a href="/static/arqueos_caja.html" class="card">
        <div class="card-icon">📋</div>
        <h3>Arqueos de Caja</h3>
        <p>Registra y audita la conciliación de cajas</p>
    </a>
</div>
```

---

## Opción 2: Agregar en un Menú Desplegable

Si tienes un menú de "Reportes" o "Administración":

```html
<li class="menu-item">
    <a href="/static/reportes.html">Reportes</a>
    <ul class="submenu">
        <!-- Otros items -->
        <li><a href="/static/arqueos_caja.html">📋 Arqueos de Caja</a></li>
    </ul>
</li>
```

---

## Opción 3: Link Directo en Navbar

En la barra de navegación superior:

```html
<nav class="navbar">
    <!-- Otros links -->
    <a href="/static/arqueos_caja.html" class="nav-link">
        Arqueos de Caja
    </a>
</nav>
```

---

## Opción 4: Agregar a una Tabla de Módulos

Si tienes una tabla o grid de módulos disponibles:

```html
<tr>
    <td>
        <a href="/static/arqueos_caja.html">
            <strong>📋 ARQUEOS DE CAJA</strong>
        </a>
    </td>
    <td>Registra y audita conciliación de cajas por turno</td>
    <td><span class="status-active">Disponible</span></td>
</tr>
```

---

## Pasos para Integrar (Paso a Paso)

### 1. Localiza el archivo `dashboard.html`
```
app/static/dashboard.html
```

### 2. Abre el archivo en el editor

### 3. Busca la sección del menú/navegación
Busca dónde están otros botones como:
- Ventas
- Compras
- Productos
- Cierres de Caja
- etc.

### 4. Copia un ejemplo existente
Por ejemplo, si existe "Cierres de Caja", copia:
```html
<a href="/static/cajas_cierre.html">
    <span class="icon">🔐</span>
    <span class="label">Cierres de Caja</span>
</a>
```

### 5. Cambia la ruta y nombre
```html
<a href="/static/arqueos_caja.html">
    <span class="icon">📋</span>
    <span class="label">Arqueos de Caja</span>
</a>
```

### 6. Guarda el archivo

### 7. Recarga el navegador
```
Ctrl+F5 (para forzar recarga completa)
```

---

## Iconos Sugeridos

Puedes usar cualquiera de estos:
- 📋 Portapapeles
- 🔍 Lupa
- 📊 Gráficos
- ✓ Checkmark
- 💰 Dinero
- 🏪 Tienda
- 📝 Documento
- 🗂️ Carpeta

---

## Orden Recomendado en el Menú

Sugerencia de dónde colocar "Arqueos de Caja":

```
Ventas
├── Nueva Venta
├── Tickets
└── Devoluciones

Dinero
├── Arqueos de Caja  ← AQUÍ (con Cierres de Caja)
└── Cierres de Caja

Inventario
├── Productos
├── Compras
├── Traspasos
└── Paquetes
```

---

## Código CSS para Estilo

Si necesitas estilos personalizados:

```css
/* Botón de Arqueos */
.menu-item a[href="/static/arqueos_caja.html"] {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    background: linear-gradient(135deg, #f5f5f5 0%, #fff 100%);
    border: 2px solid #c41e3a;
    border-radius: 8px;
    color: #c41e3a;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
}

.menu-item a[href="/static/arqueos_caja.html"]:hover {
    background: linear-gradient(135deg, #c41e3a 0%, #8b1428 100%);
    color: #fff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(196, 30, 58, 0.3);
}
```

---

## Verificación Post-Integración

✅ Pasos para verificar que funciona:

1. Abre dashboard.html
2. Busca el nuevo botón/link "Arqueos de Caja"
3. Click en él
4. Debe abrirse `/static/arqueos_caja.html`
5. Verifica que funciona correctamente

---

## Permisos y Control de Acceso

Si tienes sistema de permisos, agrega:

```javascript
// En tu script de permisos
PERMITIR_MODULOS.push({
    nombre: 'Arqueos de Caja',
    url: '/static/arqueos_caja.html',
    roles: ['gerente_caja', 'administrador', 'cajerero'],
    icono: '📋'
});
```

O en el HTML condicional:

```html
{% if usuario.rol in ['gerente_caja', 'administrador'] %}
    <a href="/static/arqueos_caja.html" class="btn-menu">
        📋 Arqueos de Caja
    </a>
{% endif %}
```

---

## Ejemplo Completo de Integración

### Antes (Sin Arqueos)
```html
<div class="menu-section">
    <h3>Dinero</h3>
    <a href="/static/cajas_cierre.html">🔐 Cierres de Caja</a>
</div>
```

### Después (Con Arqueos)
```html
<div class="menu-section">
    <h3>Dinero</h3>
    <a href="/static/arqueos_caja.html">📋 Arqueos de Caja</a>
    <a href="/static/cajas_cierre.html">🔐 Cierres de Caja</a>
</div>
```

---

## ¿Necesitas Ayuda?

Si no encuentras dónde agregar el botón:

1. Abre `dashboard.html` con Ctrl+F
2. Busca "cajas_cierre" o "reportes"
3. El código de menú está cerca
4. Copia esa estructura y adapta para arqueos

---

## 🔄 Alternativa: Usar un Router

Si usas un sistema de routing (ej: Vue Router, React Router):

```javascript
{
    path: '/arqueos-caja',
    component: ArqueosCaja,
    name: 'Arqueos de Caja',
    icon: '📋',
    roles: ['gerente_caja', 'administrador'],
    meta: { 
        title: 'Arqueos de Caja',
        description: 'Audita la conciliación de cajas'
    }
}
```

---

**¡Listo!** Ahora tus usuarios pueden acceder directamente desde el dashboard 🎉
