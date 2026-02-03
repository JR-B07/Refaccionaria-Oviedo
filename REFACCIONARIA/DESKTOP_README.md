# 🖥️ Aplicación de Escritorio - Refaccionaria Oviedo

## 📋 Descripción

Sistema ERP de Refaccionaria Oviedo convertido en aplicación de escritorio nativa con interfaz gráfica moderna.

---

## 🚀 Inicio Rápido

### Opción 1: Ejecutable Windows (Recomendado)
Simplemente haz doble clic en:
```
Refaccionaria.bat
```

### Opción 2: Línea de comandos
```bash
python launch_desktop.py
```

---

## ✅ Requisitos

- **Python 3.8 o superior**
- **MySQL 8.0** (servidor debe estar activo)
- **Dependencias:** Se instalan automáticamente

---

## 📦 Instalación Manual

Si necesitas instalar las dependencias manualmente:

```bash
pip install pywebview requests uvicorn fastapi sqlalchemy
```

---

## 🎨 Características

✅ **Ventana nativa** - No necesita navegador externo
✅ **Logo personalizado** - Usa el logo de Refaccionaria Oviedo
✅ **Inicio automático** - Servidor FastAPI se inicia automáticamente
✅ **Cierre limpio** - Al cerrar la ventana se detiene el servidor
✅ **Responsive** - Ventana redimensionable (mínimo 1024x768)
✅ **Puerto configurable** - Por defecto usa puerto 8000

---

## ⚙️ Configuración

### Cambiar Puerto

Edita `launch_desktop.py`:

```python
HOST = "127.0.0.1"
PORT = 8000  # Cambiar aquí
```

### Cambiar Tamaño de Ventana

En `launch_desktop.py`:

```python
width=1440,   # Ancho en píxeles
height=900,   # Alto en píxeles
```

---

## 📂 Estructura de Archivos

```
REFACCIONARIA/
├── Refaccionaria.bat           # Launcher Windows
├── launch_desktop.py           # Aplicación principal
├── desktop_app.py              # Versión simple
├── app/
│   └── static/
│       └── images/
│           └── logo-refaccionaria.png  # Logo del sistema
└── ...
```

---

## 🔧 Solución de Problemas

### Error: "Python no encontrado"
- Instala Python desde: https://www.python.org/downloads/
- Asegúrate de marcar "Add Python to PATH" durante la instalación

### Error: "No se pudo iniciar el servidor"
- Verifica que el puerto 8000 no esté en uso
- Comprueba que MySQL esté corriendo
- Revisa el archivo `.env` para credenciales de base de datos

### Error: "pywebview no encontrado"
Instala manualmente:
```bash
pip install pywebview
```

En Linux/Mac también necesitarás:
```bash
# Linux
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0

# Mac
brew install python-tk
```

---

## 🖱️ Uso

1. **Inicia la aplicación** con `Refaccionaria.bat`
2. **Espera** a que el servidor se inicie (10-15 segundos)
3. **Usa el sistema** normalmente como en el navegador
4. **Cierra** la ventana cuando termines (el servidor se detiene automáticamente)

---

## 📊 Ventajas vs Navegador Web

| Característica | Escritorio | Navegador |
|----------------|-----------|-----------|
| Instalación | ✅ Una vez | ❌ No necesaria |
| Logo/Icono | ✅ Personalizado | ⚠️ Favicon genérico |
| Experiencia | ✅ Aplicación nativa | ⚠️ Pestaña del navegador |
| Notificaciones | ✅ Sistema | ⚠️ Navegador |
| Arranque | ✅ Automático | ❌ Manual |
| Cierre | ✅ Limpio | ⚠️ Deja servidor corriendo |

---

## 🔐 Seguridad

- El servidor **solo** escucha en `127.0.0.1` (localhost)
- **No es accesible** desde la red externa
- Mismas credenciales que en el modo web

---

## 📝 Notas

- La primera vez puede tardar más en abrir (carga de módulos)
- Requiere conexión a MySQL activa
- Los cambios en el código requieren reiniciar la aplicación
- Los logs se muestran en la consola (si se abre desde CMD)

---

## 🆘 Soporte

Si encuentras problemas:

1. Verifica que MySQL esté corriendo
2. Comprueba el archivo `.env`
3. Revisa los logs en la consola
4. Prueba primero en modo web: `python run.py`

---

## 📅 Versión

**v1.0.0** - Aplicación de escritorio inicial
- ✅ Ventana nativa con pywebview
- ✅ Logo personalizado
- ✅ Inicio/cierre automático de servidor
- ✅ Configuración responsive

---

**Desarrollado para Refaccionaria Oviedo** 🏪
