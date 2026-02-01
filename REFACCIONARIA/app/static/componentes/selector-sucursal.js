/**
 * Componente Selector de Sucursal
 * Uso: Incluir en el HTML y llamar a inicializarSelectorSucursal()
 */

let SUCURSALES = [];

// Cargar sucursales desde la API al iniciar
async function cargarSucursales() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/v1/locales/', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        if (response.ok) {
            SUCURSALES = await response.json();
            console.log('✅ Sucursales cargadas desde API:', SUCURSALES);
        } else {
            console.error('Error al cargar sucursales:', response.status);
            SUCURSALES = [];
        }
    } catch (error) {
        console.error('Error conectando a la API de sucursales:', error);
        SUCURSALES = [];
    }
}

/**
 * Inicializa el selector de sucursal
 * @param {string} selectId - ID del elemento select
 * @param {function} callback - Función a ejecutar cuando cambie la sucursal
 */
async function inicializarSelectorSucursal(selectId = 'sucursalSelect', callback = null) {
    // Cargar sucursales si no están cargadas
    if (SUCURSALES.length === 0) {
        await cargarSucursales();
    }

    const select = document.getElementById(selectId);
    if (!select) {
        console.warn(`Selector con ID "${selectId}" no encontrado`);
        return null;
    }

    // Limpiar opciones existentes
    select.innerHTML = '';

    // Agregar opciones
    SUCURSALES.forEach(sucursal => {
        const option = document.createElement('option');
        option.value = sucursal.id;
        option.textContent = sucursal.nombre;
        select.appendChild(option);
    });

    // Establecer valor por defecto
    const localIdDefecto = obtenerLocalIdDefecto();
    select.value = localIdDefecto;

    // Agregar listener si se proporciona callback
    if (callback && typeof callback === 'function') {
        select.addEventListener('change', (e) => {
            const localId = parseInt(e.target.value, 10);
            callback(localId);
        });
    }

    console.log(`✅ Selector ${selectId} inicializado`);
    return localIdDefecto;
}

/**
 * Obtiene el local_id del usuario o del URL
 * @returns {number} ID de la sucursal
 */
function obtenerLocalIdDefecto() {
    // Primero, revisar si viene en la URL
    const urlParams = new URLSearchParams(window.location.search);
    const urlLocalId = urlParams.get('local_id');
    if (urlLocalId) {
        const localId = parseInt(urlLocalId, 10);
        if (!isNaN(localId) && SUCURSALES.find(s => s.id === localId)) {
            return localId;
        }
    }

    // Si no viene en URL, usar del usuario
    try {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        if (user && user.local_id) {
            const localId = parseInt(user.local_id, 10);
            if (!isNaN(localId)) return localId;
        }
    } catch (e) {
        console.warn('Error al leer local_id del usuario:', e.message);
    }

    // Por defecto, sucursal 1
    return SUCURSALES[0].id;
}

/**
 * Obtiene el local_id actualmente seleccionado
 * @param {string} selectId - ID del elemento select
 * @returns {number} ID de la sucursal seleccionada
 */
function obtenerLocalIdSeleccionado(selectId = 'sucursalSelect') {
    const select = document.getElementById(selectId);
    if (!select) return obtenerLocalIdDefecto();
    return parseInt(select.value, 10);
}

/**
 * Obtiene el nombre de la sucursal por su ID
 * @param {number} localId - ID de la sucursal
 * @returns {string} Nombre de la sucursal
 */
function obtenerNombreSucursal(localId) {
    const sucursal = SUCURSALES.find(s => s.id === localId);
    return sucursal ? sucursal.nombre : 'Desconocida';
}

/**
 * Obtiene el local_id del usuario desde localStorage
 * @returns {number} ID del local del usuario
 */
function obtenerLocalIdUsuario() {
    try {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        return user.local_id ? parseInt(user.local_id, 10) : 1;
    } catch (e) {
        return 1;
    }
}
