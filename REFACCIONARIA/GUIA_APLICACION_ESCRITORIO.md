# 🖥️ APLICACIÓN DE ESCRITORIO - GUÍA COMPLETA

## ✅ Sistema Convertido a Aplicación de Escritorio

Se ha configurado el sistema para ejecutarse como una aplicación de escritorio con **2 modos de operación**:

---

## 🚀 MODO 1: Aplicación de Escritorio Nativa (Recomendado)

### Características
- ✅ Ventana nativa independiente (no usa navegador)
- ✅ Logo personalizado de Refaccionaria Oviedo
- ✅ Cierre automático del servidor
- ✅ Experiencia tipo aplicación de escritorio

### Cómo Usar
1. **Doble clic en:** `Refaccionaria.bat`
2. Espera 10-15 segundos a que se abra la ventana
3. Usa el sistema normalmente
4. Al cerrar la ventana, el servidor se detiene automáticamente

### Requisito
- Requiere la librería `pywebview` (se instala automáticamente al primer uso)

### Archivos
- `Refaccionaria.bat` - Lanzador principal
- `launch_desktop.py` - Aplicación de escritorio
- `desktop_app.py` - Versión alternativa

---

## 🌐 MODO 2: Inicio Rápido con Navegador

### Características
- ✅ Abre automáticamente tu navegador predeterminado
- ✅ Sin dependencias adicionales
- ✅ Más rápido de iniciar
- ⚠️ Requiere cerrar manualmente el servidor (Ctrl+C)

### Cómo Usar
1. **Doble clic en:** `InicioRapido.bat`
2. Se abre automáticamente en tu navegador
3. Para detener: Cierra la ventana de consola o presiona Ctrl+C

### Archivos
- `InicioRapido.bat` - Lanzador navegador
- `launch_browser.py` - Script de inicio

---

## 📁 Archivos Creados

```
REFACCIONARIA/
├── 🚀 Refaccionaria.bat          # Launcher Modo Escritorio
├── 🌐 InicioRapido.bat           # Launcher Modo Navegador
├── 📱 launch_desktop.py          # App de escritorio principal
├── 🖥️ desktop_app.py             # App de escritorio simple
├── 🌍 launch_browser.py          # Launcher navegador
├── 📖 DESKTOP_README.md          # Documentación completa
└── app/static/images/
    └── 🖼️ logo-refaccionaria.png # Logo del sistema
```

---

## ⚙️ Configuración

### Cambiar Puerto (si 8000 está ocupado)

Edita cualquier archivo de lanzamiento y cambia:
```python
PORT = 8000  # Cambiar a 8001, 8002, etc.
```

### Cambiar Tamaño de Ventana

En `launch_desktop.py`:
```python
width=1440,   # Ancho
height=900,   # Alto
min_size=(1024, 768)  # Tamaño mínimo
```

---

## 🎨 Logo Personalizado

El sistema usa el logo ubicado en:
```
app/static/images/logo-refaccionaria.png
```

Para cambiar el logo:
1. Reemplaza el archivo con tu nuevo logo
2. Mantén el nombre `logo-refaccionaria.png`
3. Formato recomendado: PNG con transparencia
4. Tamaño recomendado: 512x512 px o superior

---

## 📋 Comparación de Modos

| Característica | Modo Escritorio | Modo Navegador |
|----------------|----------------|----------------|
| **Ventana** | Nativa independiente | Pestaña del navegador |
| **Logo** | Personalizado | Favicon |
| **Instalación** | pywebview requerido | Sin dependencias |
| **Inicio** | 15 segundos | 5 segundos |
| **Cierre** | Automático | Manual (Ctrl+C) |
| **Experiencia** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🔧 Solución de Problemas

### Error: "Puerto 8000 ya en uso"
```bash
# Opción 1: Cerrar el servidor existente
taskkill /F /IM python.exe

# Opción 2: Cambiar puerto en los archivos de configuración
```

### Error: "pywebview no encontrado"
El archivo `Refaccionaria.bat` lo instala automáticamente, pero si falla:
```bash
pip install pywebview
```

### Error: "No se puede conectar a la base de datos"
1. Verifica que MySQL esté corriendo
2. Comprueba las credenciales en `.env`
3. Asegúrate que existe la base de datos `refaccionaria_db`

---

## 🎯 Recomendaciones de Uso

### Para Usuarios Finales
➡️ Usa `Refaccionaria.bat` (Modo Escritorio)
- Mejor experiencia de usuario
- Parece una aplicación profesional
- Cierre limpio y automático

### Para Desarrollo/Testing
➡️ Usa `InicioRapido.bat` (Modo Navegador)
- Inicio más rápido
- Fácil acceso a herramientas del navegador
- Mejor para debugging

### Para Producción
➡️ Considera usar el servidor web tradicional:
```bash
python run.py
# o
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📊 Ventajas de la Aplicación de Escritorio

✅ **Profesional** - Parece software instalado, no una web
✅ **Conveniente** - Un solo doble clic para iniciar todo
✅ **Automático** - No necesitas abrir navegador manualmente
✅ **Limpio** - Cierre automático sin procesos zombie
✅ **Branding** - Logo personalizado visible
✅ **Offline-first** - Toda la lógica es local

---

## 🔐 Seguridad

- El servidor **solo** escucha en `127.0.0.1` (localhost)
- **No es accesible** desde otras máquinas de la red
- Mismas credenciales de login que siempre
- Base de datos local protegida

---

## 📈 Próximos Pasos Opcionales

Si quieres mejorar aún más:

1. **Crear instalador .exe** con PyInstaller
2. **Icono personalizado** en el .exe
3. **Auto-actualización** desde servidor remoto
4. **Notificaciones de escritorio** para alertas
5. **Integración con Windows** (inicio automático)

---

## 📞 Soporte

**Archivos de documentación:**
- `DESKTOP_README.md` - Guía de usuario detallada
- Este archivo - Guía técnica completa

**Troubleshooting:**
1. Verifica MySQL corriendo
2. Comprueba puerto disponible
3. Revisa archivo .env
4. Consulta logs en consola

---

## ✨ Resumen Ejecutivo

**ANTES:** Sistema web que requería:
1. Abrir terminal
2. Ejecutar `python run.py`
3. Abrir navegador manualmente
4. Ir a http://localhost:8000
5. Recordar cerrar el servidor

**AHORA:** 
1. Doble clic en `Refaccionaria.bat`
2. ✅ ¡Listo!

---

**Sistema desarrollado para Refaccionaria Oviedo** 🏪
**Versión Desktop: 1.0.0**
**Fecha: 3 de febrero de 2026**
