# 📋 CHECKLIST DE INSTALACIÓN RÁPIDA

## ⚡ Instalación en 5 Pasos (15 minutos)

### 1️⃣ PYTHON (3 minutos)
```
□ Descargar: https://www.python.org/downloads/
□ Instalar: python-3.10.exe
□ ✅ IMPORTANTE: Marcar "Add Python to PATH"
□ Verificar: Abrir CMD y ejecutar: python --version
```

### 2️⃣ MYSQL (3 minutos)
```
□ Descargar: https://dev.mysql.com/downloads/mysql/
□ Instalar: mysql-installer-community-8.0.exe
□ Puerto: 3306 (no cambiar)
□ Contraseña root: Ej: MiSQL@2026 (GUARDAR)
□ Verificar: Abrir CMD y ejecutar: mysql --version
```

### 3️⃣ DESCARGAR REFACCIONARIA (2 minutos)
```
□ Opción A: Con Git (si lo instalaste)
   git clone https://github.com/JR-B07/Refaccionaria-Oviedo.git

□ Opción B: Sin Git (descarga manual)
   Ve a: https://github.com/JR-B07/Refaccionaria-Oviedo
   Click: Code > Download ZIP
   Descomprime la carpeta
```

### 4️⃣ INSTALAR DEPENDENCIAS (5 minutos)
```
□ Abre CMD en la carpeta REFACCIONARIA
□ Ejecuta: pip install -r requirements.txt
□ Espera a que termine (5 minutos aprox)
```

### 5️⃣ EJECUTAR SISTEMA (2 minutos)
```
□ En CMD ejecuta: python launch_desktop.py
□ Se abre automáticamente la aplicación
□ Login con usuario: admin@refaccionaria.com
□ Contraseña: admin123 (cambiar después)
```

---

## 📦 Archivos Configuración Necesarios

### Archivo: `.env` (Crear en carpeta REFACCIONARIA)

```
MYSQL_SERVER=localhost
MYSQL_USER=root
MYSQL_PASSWORD=MiSQL@2026
MYSQL_DATABASE=refaccionaria_db
MYSQL_PORT=3306

DATABASE_URL=mysql+pymysql://root:MiSQL@2026@localhost:3306/refaccionaria_db

JWT_SECRET_KEY=tu-clave-secreta-super-larga-aqui-cambiar-en-produccion

DEBUG=False
ENVIRONMENT=production
```

---

## 🆘 Si Algo Falla

### Python no funciona
```
1. Desinstala Python
2. Reinstala marcando: ✅ "Add Python to PATH"
3. Reinicia CMD
4. Ejecuta: python --version
```

### MySQL no funciona
```
1. Verifica que MySQL esté corriendo
2. Cmd: net start MySQL80
3. O busca "services.msc" y encuentra "MySQL80"
```

### Errores de módulos
```
1. Asegúrate de estar en la carpeta REFACCIONARIA
2. Ejecuta: pip install -r requirements.txt
3. Espera a que termine completamente
```

---

## ✅ Verificación Previa

Antes de instalar, ejecuta:

**Windows:**
```bash
verificar_requerimientos.bat
```

**macOS/Linux:**
```bash
bash verificar_requerimientos.sh
```

---

## 💾 Software Necesario

| Software | Versión | Descarga |
|----------|---------|----------|
| **Python** | 3.8+ | https://www.python.org/downloads/ |
| **MySQL** | 8.0+ | https://dev.mysql.com/downloads/mysql/ |
| **Git** | Último | https://git-scm.com/download/ |
| **Navegador** | Chrome/Firefox | Ya instalado |
| **Editor (Opcional)** | VS Code | https://code.visualstudio.com/ |

---

## 🎯 Lo Mínimo Indispensable

✅ **OBLIGATORIO:**
- Python 3.8+
- MySQL 8.0+
- Carpeta del proyecto

❌ **NO OBLIGATORIO:**
- Git (puedes descargar ZIP)
- Editor de código
- Visual C++ (generalmente no es necesario)

---

## 📊 Requisitos Hardware

| Componente | Mínimo | Recomendado |
|-----------|--------|-------------|
| **RAM** | 2 GB | 4 GB |
| **Disco** | 1 GB | 2 GB SSD |
| **CPU** | 2 núcleos | 4 núcleos |
| **Internet** | No necesario | Para actualizaciones |

---

**Tiempo total de instalación: 15-20 minutos**

**Soporte:** Si tienes dudas, consulta GUIA_INSTALACION_CLIENTE.md
