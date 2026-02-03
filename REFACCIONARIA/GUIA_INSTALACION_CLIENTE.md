# 🚀 GUÍA COMPLETA DE INSTALACIÓN - REFACCIONARIA OVIEDO

## ✅ REQUISITOS PREVIOS - LO QUE DEBE INSTALAR EL CLIENTE

### 📋 Lista de Verificación Rápida

```
ANTES DE INSTALAR EL SISTEMA:

☐ Python 3.8 o superior
☐ MySQL 8.0 o superior
☐ Visual C++ Redistributable (Windows)
☐ Navegador web moderno (Chrome, Firefox, Edge)
```

---

## 1️⃣ **PYTHON - PASO MÁS IMPORTANTE**

### ¿Por qué se necesita Python?
El sistema está escrito en Python (FastAPI). Sin Python, el sistema no puede ejecutarse.

### Instalación en Windows

#### **Opción A: Instalador oficial (RECOMENDADO)**

1. **Descargar:**
   - Ve a: https://www.python.org/downloads/
   - Descarga la última versión de Python 3.10+ (windows installer)
   - Archivo: `python-3.10.13-amd64.exe` (o versión más reciente)

2. **Instalar:**
   - Doble clic en el instalador
   - ✅ **IMPORTANTE: Marcar "Add Python to PATH"**
   - Click en "Install Now"
   - Esperar a que termine (2-3 minutos)

3. **Verificar instalación:**
   ```bash
   Abrir CMD y ejecutar:
   python --version
   
   Debería mostrar: Python 3.10.x (o superior)
   ```

#### **Opción B: Microsoft Store**
```
1. Abrir Microsoft Store
2. Buscar "Python"
3. Descargar "Python 3.10" (o versión más reciente)
4. Esperar instalación
5. Verificar: python --version
```

### Instalación en macOS

```bash
# Usando Homebrew (recomendado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install python3

# Verificar
python3 --version
```

### Instalación en Linux (Ubuntu/Debian)

```bash
# Actualizar repositorios
sudo apt update

# Instalar Python
sudo apt install python3 python3-pip python3-venv

# Verificar
python3 --version
pip3 --version
```

---

## 2️⃣ **MYSQL - BASE DE DATOS**

### ¿Por qué se necesita MySQL?
Almacena todos los datos: productos, usuarios, ventas, etc.

### Instalación en Windows

#### **Opción A: MySQL Community Server (RECOMENDADO)**

1. **Descargar:**
   - Ve a: https://dev.mysql.com/downloads/mysql/
   - Selecciona: "Windows (x86, 64-bit), MSI Installer"
   - Descarga: `mysql-installer-community-8.0.x-winx64.msi`

2. **Instalar:**
   - Doble clic en el instalador
   - Click "Next"
   - Seleccionar: "Server only"
   - Click "Next" hasta "MySQL Server Configuration"
   
3. **Configuración Importante:**
   - Puerto: **3306** (por defecto, no cambiar)
   - Tipo de servidor: "Development Machine"
   - MySQL Protocol Port: 3306
   - Click "Next"
   
4. **Configuración MySQL:**
   - Root Password: **Escribe una contraseña segura** (ej: "MiSQL@2026")
   - ⚠️ GUARDAR ESTA CONTRASEÑA - LA NECESITARÁS LUEGO
   - Click "Next" y finalizar

5. **Verificar instalación:**
   ```bash
   Abrir CMD y ejecutar:
   mysql --version
   
   Debería mostrar: mysql Ver 8.0.x
   ```

#### **Opción B: Docker + MySQL (Alternativa moderna)**

```bash
# Instalar Docker Desktop desde: https://www.docker.com/products/docker-desktop

# Una vez instalado, ejecutar en CMD:
docker run -d ^
  --name mysql-refaccionaria ^
  -e MYSQL_ROOT_PASSWORD=MiSQL@2026 ^
  -p 3306:3306 ^
  mysql:8.0
```

### Instalación en macOS

```bash
# Opción 1: Homebrew
brew install mysql

# Opción 2: DMG Installer
# Descargar desde: https://dev.mysql.com/downloads/mysql/

# Iniciar MySQL
mysql.server start
```

### Instalación en Linux (Ubuntu)

```bash
# Instalar
sudo apt install mysql-server

# Iniciar el servicio
sudo systemctl start mysql

# Verificar
mysql --version
```

---

## 3️⃣ **GIT - PARA CLONAR EL PROYECTO (Opcional pero recomendado)**

### ¿Por qué Git?
Facilita descargar y actualizar el código del sistema.

### Instalación en Windows

1. **Descargar:**
   - Ve a: https://git-scm.com/download/win
   - Descarga: `Git-2.40.x-64-bit.exe` (o versión más reciente)

2. **Instalar:**
   - Doble clic en el instalador
   - Click "Next" en todas las opciones por defecto
   - Click "Install"

3. **Verificar:**
   ```bash
   git --version
   
   Debería mostrar: git version 2.40.x
   ```

### Instalación en macOS/Linux

```bash
# macOS
brew install git

# Linux (Ubuntu)
sudo apt install git

# Verificar
git --version
```

---

## 4️⃣ **VISUAL C++ REDISTRIBUTABLE (Solo Windows)**

Necesario para algunas librerías Python.

1. **Descargar:**
   - https://support.microsoft.com/en-us/help/2977003
   - O busca: "Visual C++ Redistributable 2022"

2. **Instalar:**
   - Doble clic
   - Aceptar términos
   - Click "Install"

---

## 5️⃣ **NAVEGADOR WEB MODERNO**

El sistema se ejecuta en el navegador. Necesitas:

- ✅ **Google Chrome 90+** (RECOMENDADO)
- ✅ **Mozilla Firefox 88+**
- ✅ **Microsoft Edge 90+**
- ❌ **Internet Explorer (NO compatible)**

---

## 📋 VERIFICACIÓN PRE-INSTALACIÓN

Ejecuta este script para verificar que todo está listo:

```bash
# Windows - Guardar como: verificar_requerimientos.bat
@echo off
echo Verificando requisitos del sistema...
echo.

echo [1/3] Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado
    pause
    exit /b 1
)

echo.
echo [2/3] Verificando MySQL...
mysql --version
if %errorlevel% neq 0 (
    echo ERROR: MySQL no está instalado
    pause
    exit /b 1
)

echo.
echo [3/3] Verificando Git...
git --version
if %errorlevel% neq 0 (
    echo ERROR: Git no está instalado
    pause
    exit /b 1
)

echo.
echo ✅ TODOS LOS REQUISITOS ESTÁN INSTALADOS
pause
```

---

## 🔧 INSTALACIÓN DEL SISTEMA PASO A PASO

Una vez que tengas los prerequisitos, sigue estos pasos:

### **Paso 1: Descargar el código**

```bash
# Opción A: Con Git (si lo instalaste)
cd C:\Usuarios\TuNombre\Documentos
git clone https://github.com/JR-B07/Refaccionaria-Oviedo.git
cd Refaccionaria-Oviedo/REFACCIONARIA

# Opción B: Sin Git (descarga manual)
# 1. Ve a: https://github.com/JR-B07/Refaccionaria-Oviedo
# 2. Click "Code" > "Download ZIP"
# 3. Descomprime en C:\Usuarios\TuNombre\Documentos
# 4. Abre la carpeta Refaccionaria-Oviedo\REFACCIONARIA
```

### **Paso 2: Configurar archivo .env**

```bash
# En la carpeta REFACCIONARIA, crear archivo: .env

MYSQL_SERVER=localhost
MYSQL_USER=root
MYSQL_PASSWORD=MiSQL@2026
MYSQL_DATABASE=refaccionaria_db
MYSQL_PORT=3306

DATABASE_URL=mysql+pymysql://root:MiSQL@2026@localhost:3306/refaccionaria_db

JWT_SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-aqui

DEBUG=False
ENVIRONMENT=production
```

### **Paso 3: Instalar dependencias Python**

```bash
# Abrir CMD en la carpeta REFACCIONARIA
cd C:\Usuarios\TuNombre\Documentos\Refaccionaria-Oviedo\REFACCIONARIA

# Instalar dependencias
pip install -r requirements.txt

# Esto descargará e instalará todas las librerías necesarias
# Toma 2-5 minutos la primera vez
```

### **Paso 4: Crear base de datos**

```bash
# Windows: Abrir CMD
mysql -u root -p < refaccionaria_db.sql

# Ingresa tu contraseña de MySQL

# Si prefieres hacerlo manualmente:
# 1. Abrir MySQL Workbench
# 2. Conectar con usuario: root, contraseña: MiSQL@2026
# 3. File > Open SQL Script > refaccionaria_db.sql
# 4. Click "Execute"
```

### **Paso 5: Iniciar el sistema**

```bash
# Opción A: Modo Escritorio (RECOMENDADO)
python launch_desktop.py

# Opción B: Modo Navegador
python launch_browser.py

# Opción C: Modo Web estándar
python run.py
```

---

## 📦 RESUMEN COMPLETO DE INSTALACIÓN

### **Para Windows (Recomendado)**

```
PASO 1: Instalar Python 3.10+
   Descargar de: https://www.python.org/downloads/
   ✅ Marcar "Add Python to PATH"

PASO 2: Instalar MySQL 8.0+
   Descargar de: https://dev.mysql.com/downloads/mysql/
   ✅ Guardar contraseña del root
   ✅ Puerto: 3306

PASO 3: Instalar Visual C++ Redistributable
   https://support.microsoft.com/en-us/help/2977003

PASO 4: Instalar Git (Opcional pero recomendado)
   https://git-scm.com/download/win

PASO 5: Descargar Refaccionaria Oviedo
   git clone https://github.com/JR-B07/Refaccionaria-Oviedo.git

PASO 6: Instalar dependencias
   pip install -r requirements.txt

PASO 7: Configurar base de datos
   mysql -u root -p < refaccionaria_db.sql

PASO 8: Ejecutar sistema
   python launch_desktop.py
```

---

## 🆘 TROUBLESHOOTING - ERRORES COMUNES

### **Error: "Python no es reconocido"**

❌ **Problema:** Python no está en el PATH

✅ **Solución:**
1. Desinstalar Python
2. Reinstalar marcando: ✅ "Add Python to PATH"
3. Reiniciar CMD

---

### **Error: "MySQL no es reconocido"**

❌ **Problema:** MySQL no está en el PATH

✅ **Solución:**
```bash
# Agregar manualmente MySQL al PATH
# 1. Click derecho en "Este equipo" > Propiedades
# 2. Variables de entorno > Nueva
# 3. Nombre: PATH
# 4. Valor: C:\Program Files\MySQL\MySQL Server 8.0\bin
# 5. Reiniciar CMD
```

---

### **Error: "ModuleNotFoundError: No module named 'fastapi'**

❌ **Problema:** Las dependencias no están instaladas

✅ **Solución:**
```bash
pip install -r requirements.txt
```

---

### **Error: "Can't connect to MySQL server"**

❌ **Problema:** MySQL no está corriendo

✅ **Solución Windows:**
```bash
# Iniciar servicio MySQL
net start MySQL80

# O abrir Services (services.msc) y buscar "MySQL80"
```

✅ **Solución macOS/Linux:**
```bash
# macOS
mysql.server start

# Linux
sudo systemctl start mysql
```

---

### **Error: "Access denied for user 'root'@'localhost'"**

❌ **Problema:** Contraseña incorrecta en .env

✅ **Solución:**
```bash
# Verificar contraseña
mysql -u root -p

# Si olvidaste la contraseña, desinstala y reinstala MySQL
```

---

## 💾 VERSIONES RECOMENDADAS

| Software | Versión Mínima | Versión Recomendada |
|----------|---------------|-------------------|
| Python | 3.8 | 3.10 o 3.11 |
| MySQL | 8.0 | 8.0.26+ |
| Git | 2.30+ | 2.40+ |
| Visual C++ | 2015 | 2022 |
| Chrome | 90+ | Última |

---

## 📊 TABLA DE COMPATIBILIDAD

| Sistema Operativo | Python | MySQL | Git | Status |
|------------------|--------|-------|-----|--------|
| Windows 10/11 64-bit | ✅ | ✅ | ✅ | ✅ Recomendado |
| Windows 10/11 32-bit | ⚠️ Lento | ⚠️ | ✅ | ⚠️ Funciona |
| macOS 10.15+ | ✅ | ✅ | ✅ | ✅ OK |
| Linux Ubuntu 20.04+ | ✅ | ✅ | ✅ | ✅ OK |
| Windows 7 | ❌ | ❌ | ❌ | ❌ No soportado |

---

## 🎯 MÍNIMO INDISPENSABLE

Si el cliente **SOLO** quiere ejecutar el sistema sin actualizar código:

✅ **NECESITA:**
1. Python 3.8+
2. MySQL 8.0+
3. Archivo `refaccionaria_db.sql`
4. Carpeta del proyecto

❌ **NO NECESITA:**
- Visual C++ (solo si tiene errores)
- Git (puede descargar ZIP)
- Navegador especial (cualquier moderno funciona)

---

## 📞 SOPORTE RÁPIDO

**Si algo falla, envía:**
1. Pantalla del error
2. Resultado de: `python --version`
3. Resultado de: `mysql --version`
4. Archivo `.env` (sin contraseña real)

---

## ✅ CHECKLIST FINAL

Antes de ir a instalar el sistema, el cliente debe tener:

```
☐ Python 3.8+ instalado y verificado
☐ MySQL 8.0+ instalado, corriendo y contraseña guardada
☐ Visual C++ Redistributable instalado
☐ Navegador web moderno instalado
☐ 2 GB RAM disponible
☐ 1 GB espacio en disco
☐ Conexión a internet para descargar dependencias
☐ Permisos de administrador en la computadora
```

Una vez tenga esto, el sistema se instala en **menos de 10 minutos**.

---

**Fecha:** 3 de febrero de 2026  
**Versión:** 1.0  
**Sistema:** Refaccionaria Oviedo ERP
