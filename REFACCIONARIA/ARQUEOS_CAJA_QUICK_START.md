# 🚀 QUICK START - ARQUEOS DE CAJA

## ¡Comienza en 5 minutos!

### 1️⃣ Reinicia el servidor
```bash
python run.py
```
La tabla `arqueos_caja` se creará automáticamente en la base de datos.

### 2️⃣ Abre la vista en tu navegador
```
http://localhost:8000/static/arqueos_caja.html
```

### 3️⃣ Crea tu primer arqueo
1. Click en botón **"+ Nuevo Arqueo"**
2. Selecciona **Caja** y **Local**
3. Ingresa los **montos declarados** (según sistema)
4. Ingresa los **montos contados** (verificación física)
5. El sistema calcula automáticamente las **diferencias**
6. Click **"Guardar Arqueo"**

### 4️⃣ Revisa el listado
- Click en tab **"Listar Arqueos"**
- Filtra por Caja/Local si deseas
- Click **"Filtrar"**

---

## 📋 Formas de Pago Soportadas

El sistema registra automáticamente 8 formas de pago:
1. 💰 **Efectivo**
2. 🏦 **Cheque**
3. 💳 **Tarjeta de Crédito**
4. 💳 **Débito**
5. 🏪 **Depósito**
6. 📝 **Crédito** (A cuenta)
7. 📄 **Vale** (Vales de venta)
8. ⭐ **Lealtad** (Puntos/Lealtad)

---

## 🧮 Cómo Funcionan los Cálculos

### Diferencia por Forma de Pago
```
Diferencia = Monto Contado - Monto Declarado

Ejemplos:
- Efectivo: 5,050 - 5,000 = +50 (sobrante)
- Cheque: 990 - 1,000 = -10 (faltante)
```

### Diferencia Total
```
Diferencia Total = 
    (Efectivo Contado + Cheque Contado + ...)
    - (Efectivo Declarado + Cheque Declarado + ...)
```

**El sistema calcula TODO automáticamente mientras escribes** ✨

---

## 🟢 Estados del Arqueo

| Estado | Significado | Color |
|--------|------------|-------|
| **Equilibrado** | Diferencia total = $0 | Verde ✓ |
| **Discrepancia** | Hay diferencia | Rojo ✗ |
| **Reconciliado** | Fue validado/revisado | Azul ℹ️ |

---

## 📊 Interfaz Rápida

### Tab 1: Listar Arqueos
Tabla con todos tus arqueos:
- Ver fecha, caja, turno
- Ver montos y diferencias
- Botones: Ver / Eliminar

### Tab 2: Nuevo Arqueo
Formulario para crear:
- Selecciona caja y local
- Ingresa 8 montos declarados
- Ingresa 8 montos contados
- Agrega observaciones (opcional)
- Guardar

### Tab 3: Reportes
(En desarrollo)
- Resumen general
- Estadísticas

---

## ⌨️ Atajos de Teclado

- **Tab** → Navegar entre campos
- **Enter** → En último campo, guardar
- **ESC** → No hay efecto, pero puedes click "Volver"

---

## 🔍 Filtros Disponibles

En la tab "Listar Arqueos":
```
Filtrar por:
- Caja específica (Caja 1, Caja 2, etc)
- Local específico (Oviedo, Otra sucursal, etc)
- O ambos simultáneamente
```

---

## 🆘 Errores Comunes y Soluciones

### ❌ "Se cargan los locales vacíos"
→ Asegúrate de tener locales registrados en el sistema

### ❌ "No se guarda el arqueo"
→ Verifica que llenaste Caja y Local (campos requeridos *)

### ❌ "Los números no se calculan"
→ Usa puntos (.) como separador decimal, no comas

### ❌ "Aparece error 404"
→ Reinicia el servidor

---

## 📱 ¿Funciona en Móvil?

✅ **SÍ** - La interfaz es responsive y se adapta a cualquier tamaño de pantalla

---

## 💾 ¿Dónde se guardan los datos?

Los arqueos se guardan automáticamente en:
- Base de datos: tabla `arqueos_caja`
- Registra automáticamente: usuario, fecha, hora

---

## 🎯 Próximos Pasos

1. Integrar en el menú principal del dashboard
2. (Opcional) Configurar permisos por rol
3. (Opcional) Agregar más reportes

---

## 📞 ¿Problemas?

1. Abre la consola del navegador (**F12**)
2. Busca mensajes de error en rojo
3. Verifica que el servidor está corriendo
4. Reinicia el servidor si es necesario

---

**¡Listo para usar!** 🎉

Ve a: `http://localhost:8000/static/arqueos_caja.html`
