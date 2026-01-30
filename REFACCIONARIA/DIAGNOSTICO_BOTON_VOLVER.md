# 🔧 DIAGNÓSTICO - Botón "Volver" No Funciona

## 📋 Pasos para Diagnosticar

### 1. Abrir Consola del Navegador
1. Abre la página: `http://localhost:8000/static/cajas_cierre.html`
2. Presiona **F12** (o Ctrl+Shift+I)
3. Ve a la pestaña **Console**

### 2. Hacer Click en "← Volver"
Deberías ver en consola:
```
🔙 Botón Volver clickeado - Navegando a /cajas
📍 URL actual: http://localhost:8000/static/cajas_cierre.html
✅ Navegación iniciada
```

### 3. Verificar qué pasa después

#### CASO A: Redirige al login
```
📄 Página cajas.html cargada
🔑 Token encontrado: NO
⚠️ No hay token - Redirigiendo al login
```

**PROBLEMA:** No has hecho login
**SOLUCIÓN:** 
1. Ve a `http://localhost:8000/login`
2. Login con usuario: `vendedor` / password: `password123`
3. Intenta de nuevo

#### CASO B: Se carga cajas.html pero está en blanco
```
📄 Página cajas.html cargada
🔑 Token encontrado: SÍ
👤 Usuario: {id: 3, username: "vendedor", ...}
✅ Página cajas.html lista
```

**PROBLEMA:** El HTML se carga pero no se ve
**POSIBLES CAUSAS:**
- CSS no carga
- JavaScript tiene error
- Token expiró

**SOLUCIÓN:**
Verifica en la pestaña **Network** (F12):
- ¿Se carga cajas.html? (Status 200)
- ¿Hay errores 404 o 500?

#### CASO C: No pasa nada (no navega)
**PROBLEMA:** JavaScript no se ejecuta
**SOLUCIÓN:**
En consola, ejecuta manualmente:
```javascript
window.location.href = '/cajas';
```

Si esto funciona, el problema es el evento onclick.

#### CASO D: Error en consola
```
Uncaught ReferenceError: goBack is not defined
```

**PROBLEMA:** La función no existe
**SOLUCIÓN:** Verifica que el archivo cajas_cierre.html tiene la función (línea ~729)

### 4. Verificar Token

En la consola del navegador:
```javascript
// Ver si hay token
localStorage.getItem('access_token')

// Ver usuario
JSON.parse(localStorage.getItem('user'))
```

Si no hay token:
```javascript
// Login manual
localStorage.setItem('access_token', 'test_token');
localStorage.setItem('user', JSON.stringify({
  id: 3,
  username: 'vendedor',
  name: 'Juan',
  role: 'vendedor',
  local_id: 1
}));

// Recargar
window.location.reload();
```

### 5. Verificar Endpoint del Backend

Abre en el navegador:
```
http://localhost:8000/cajas
```

Debería mostrar la página con 4 opciones (CIERRES, ARQUEOS, RETIROS, VALES)

Si muestra JSON o error 404:
- El backend no está sirviendo el HTML correctamente
- Verifica app/main.py línea 142

### 6. Forzar Navegación

Si nada funciona, en consola ejecuta paso a paso:
```javascript
// 1. Verificar URL actual
console.log(window.location.href);

// 2. Navegar
window.location.href = '/cajas';

// 3. Si no funciona, intenta con replace
window.location.replace('/cajas');

// 4. Si no funciona, intenta absoluta
window.location.href = 'http://localhost:8000/cajas';
```

## 🎯 Soluciones Rápidas

### Solución 1: Cache del navegador
```
Ctrl + Shift + R (hard reload)
o
Ctrl + F5
```

### Solución 2: Limpiar localStorage y login de nuevo
```javascript
localStorage.clear();
window.location.href = '/login';
```

### Solución 3: Deshabilitar extensiones del navegador
- Adblockers
- Privacy extensions
- Pueden estar bloqueando la navegación

### Solución 4: Probar en modo incógnito
```
Ctrl + Shift + N (Chrome)
Ctrl + Shift + P (Firefox)
```

## 📝 Información Necesaria para Debug

Si el problema persiste, necesito saber:

1. **¿Qué ves en la consola cuando haces click en "Volver"?**
   ```
   [Copiar y pegar los mensajes de consola]
   ```

2. **¿A dónde te lleva? ¿O no hace nada?**
   - [ ] Me lleva al login
   - [ ] Se queda en la misma página
   - [ ] Muestra página en blanco
   - [ ] Muestra error
   - [ ] Otro: ___________

3. **¿Hiciste login antes?**
   - [ ] Sí
   - [ ] No

4. **¿Qué URL ves en la barra del navegador después de hacer click?**
   ```
   http://localhost:8000/___________
   ```

5. **Screenshot de la consola (F12 → Console)**

---

**Creado:** 26 de enero de 2026  
**Archivo:** `cajas_cierre.html` línea 729
