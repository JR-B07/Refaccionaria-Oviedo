// js/sucursal_selector.js
// Selector de sucursal para administradores (multi-página)

async function initSucursalSelector() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (!user || user.rol !== 'administrador') return;

    // Buscar el badge y reemplazarlo por un select
    const badge = document.getElementById('sucursalBadge');
    if (!badge) return;

    // Crear el select
    const select = document.createElement('select');
    select.id = 'sucursalSelector';
    select.className = 'sucursal-selector';
    select.style.marginLeft = '8px';
    select.style.fontWeight = 'bold';
    select.style.borderRadius = '6px';
    select.style.padding = '3px 8px';
    select.style.fontSize = '13px';

    // Cargar sucursales
    try {
        const token = localStorage.getItem('access_token');
        const res = await fetch('/api/v1/locales/', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        const sucursales = await res.json();
        sucursales.forEach(suc => {
            const opt = document.createElement('option');
            opt.value = suc.id;
            opt.textContent = suc.nombre;
            if (String(suc.id) === String(localStorage.getItem('sucursal_id'))) {
                opt.selected = true;
            }
            select.appendChild(opt);
        });
    } catch (e) {
        select.innerHTML = '<option>Error</option>';
    }

    // Reemplazar badge por select
    badge.replaceWith(select);

    // Al cambiar sucursal
    select.addEventListener('change', function () {
        const selected = select.options[select.selectedIndex];
        localStorage.setItem('sucursal_id', selected.value);
        localStorage.setItem('sucursal_nombre', selected.textContent);
        location.reload();
    });
}

// Ejecutar en DOMContentLoaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSucursalSelector);
} else {
    initSucursalSelector();
}
