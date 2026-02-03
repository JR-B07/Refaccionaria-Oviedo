# 🎯 RESUMEN EJECUTIVO - QUÉ NECESITA INSTALAR EL CLIENTE

## 📌 RESPUESTA DIRECTA: 3 COSAS IMPRESCINDIBLES

```
┌─────────────────────────────────────────────────────────────────┐
│  CLIENTE NECESITA INSTALAR ANTES DE RECIBIR EL SISTEMA         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PYTHON 3.8+                                                │
│     └─ Descarga: https://www.python.org/downloads/            │
│     └─ Tiempo: 3 minutos                                       │
│     └─ Importante: Marcar "Add Python to PATH"               │
│                                                                 │
│  2. MYSQL 8.0+                                                 │
│     └─ Descarga: https://dev.mysql.com/downloads/mysql/       │
│     └─ Tiempo: 3 minutos                                       │
│     └─ Importante: Guardar la contraseña del root            │
│     └─ Puerto: 3306 (no cambiar)                             │
│                                                                 │
│  3. NAVEGADOR WEB MODERNO                                      │
│     └─ Generalmente YA LO TIENE INSTALADO                    │
│     └─ Chrome, Firefox, Edge (cualquiera funciona)          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ TABLA COMPARATIVA

### ✅ QUÉ INSTALAR SEGÚN SISTEMA OPERATIVO

#### **WINDOWS (Más común)**

| Software | ¿Necesario? | Descarga | Tiempo |
|----------|-----------|----------|--------|
| **Python 3.10** | ✅ SÍ | https://www.python.org | 3 min |
| **MySQL 8.0** | ✅ SÍ | https://dev.mysql.com | 3 min |
| **Git** | ⚠️ Opcional | https://git-scm.com | 2 min |
| **Visual C++** | ⚠️ Generalmente NO | https://support.microsoft.com | - |
| **Navegador** | ✅ YA TIENE | - | - |

**TOTAL INSTALACIÓN: 6-10 minutos**

---

#### **MACOS**

| Software | ¿Necesario? | Comando | Tiempo |
|----------|-----------|---------|--------|
| **Python 3.10** | ✅ SÍ | `brew install python3` | 5 min |
| **MySQL 8.0** | ✅ SÍ | `brew install mysql` | 5 min |
| **Git** | ⚠️ Opcional | `brew install git` | 3 min |
| **Navegador** | ✅ YA TIENE | - | - |

**TOTAL INSTALACIÓN: 10-15 minutos**

---

#### **LINUX (Ubuntu/Debian)**

| Software | ¿Necesario? | Comando | Tiempo |
|----------|-----------|---------|--------|
| **Python 3.10** | ✅ SÍ | `sudo apt install python3` | 3 min |
| **MySQL 8.0** | ✅ SÍ | `sudo apt install mysql-server` | 5 min |
| **Git** | ⚠️ Opcional | `sudo apt install git` | 2 min |
| **Navegador** | ✅ YA TIENE | - | - |

**TOTAL INSTALACIÓN: 8-12 minutos**

---

## 📋 PASO A PASO PARA EL CLIENTE

### **PASO 1: Verificar que Python NO esté instalado**

```bash
Abrir CMD/Terminal y ejecutar:
python --version

Resultado esperado:
❌ "Python no es reconocido como comando"  → Instalar Python
✅ "Python 3.8.x o superior" → YA ESTÁ INSTALADO, OMITIR PASO 1
```

### **PASO 2: Instalar Python (si no lo tiene)**

**Para Windows:**
```
1. Ir a: https://www.python.org/downloads/
2. Descargar: python-3.10.13-amd64.exe (o versión más reciente)
3. Ejecutar el instalador
4. ⚠️ MARCAR LA CASILLA: "Add Python to PATH"
5. Click "Install Now"
6. Esperar a que termine
7. Verificar: python --version
```

**Para macOS:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
python3 --version
```

**Para Linux (Ubuntu):**
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

---

### **PASO 3: Verificar que MySQL NO esté instalado**

```bash
Abrir CMD/Terminal y ejecutar:
mysql --version

Resultado esperado:
❌ "MySQL no es reconocido" → Instalar MySQL
✅ "mysql Ver 8.0.x" → YA ESTÁ INSTALADO, OMITIR PASO 3
```

### **PASO 4: Instalar MySQL (si no lo tiene)**

**Para Windows:**
```
1. Ir a: https://dev.mysql.com/downloads/mysql/
2. Seleccionar: "Windows (x86, 64-bit), MSI Installer"
3. Descargar: mysql-installer-community-8.0.x-winx64.msi
4. Ejecutar instalador
5. Click "Next"
6. Seleccionar "Server only"
7. Click "Next" hasta "MySQL Server Configuration"
8. Dejar puerto: 3306
9. Tipo: "Development Machine"
10. ⚠️ CONTRASEÑA ROOT: Ingresa una segura (ej: MiSQL@2026)
11. ⚠️ GUARDAR ESTA CONTRASEÑA - LA NECESITARÁS LUEGO
12. Finalizar instalación
13. Verificar: mysql --version
```

**Para macOS:**
```bash
brew install mysql
mysql.server start
mysql --version
```

**Para Linux (Ubuntu):**
```bash
sudo apt install mysql-server
sudo systemctl start mysql
mysql --version
```

---

### **PASO 5: Verificar Navegador**

```
Abrir: Google Chrome, Mozilla Firefox o Microsoft Edge
Si tienes cualquiera de estos → LISTO
Si no tienes ninguno: Descargar Chrome (gratuito)
```

---

## ✅ VERIFICACIÓN PRE-INSTALACIÓN

**Ejecutar ANTES de instalar Refaccionaria Oviedo:**

**Windows:**
```bash
# Descargar: verificar_requerimientos.bat
# Doble clic en el archivo

# O en CMD:
verificar_requerimientos.bat
```

**macOS/Linux:**
```bash
# Descargar: verificar_requerimientos.sh
# En Terminal:
bash verificar_requerimientos.sh
```

---

## 🎯 CHECKLIST FINAL PARA EL CLIENTE

Antes de que TÚ instales el sistema, el cliente debe tener:

```
☐ Python 3.8 o superior instalado
  Verificar: python --version
  Resultado esperado: Python 3.x.x

☐ MySQL 8.0 o superior instalado y corriendo
  Verificar: mysql --version
  Resultado esperado: mysql Ver 8.0.x

☐ Contraseña del root de MySQL anotada
  Ejemplo: MiSQL@2026

☐ Navegador web instalado
  Chrome, Firefox o Edge

☐ 2 GB de RAM disponible
  Verificar en: Administrador de tareas

☐ 1 GB de espacio en disco libre
  Verificar en: Mi PC > Propiedades
```

Si tiene TODO esto ✅, la instalación será fluida.

---

## 🔧 INSTALACIÓN DEL SISTEMA (Después de lo anterior)

Una vez que el cliente tiene Python + MySQL, tú instalas:

```bash
# 1. Descargar el código
git clone https://github.com/JR-B07/Refaccionaria-Oviedo.git

# 2. Ir a la carpeta
cd Refaccionaria-Oviedo/REFACCIONARIA

# 3. Crear archivo .env (configuración)
# (Con la contraseña de MySQL del cliente)

# 4. Instalar dependencias Python
pip install -r requirements.txt

# 5. Crear base de datos
mysql -u root -p < refaccionaria_db.sql

# 6. Ejecutar
python launch_desktop.py
```

---

## ⏱️ CRONOGRAMA TOTAL

```
CLIENTE INSTALA:
├─ Python: 3 minutos
├─ MySQL: 3 minutos
├─ Navegador: 0 minutos (ya lo tiene)
└─ Verificación: 2 minutos
   SUBTOTAL: 8 minutos

TÚ INSTALAS:
├─ Descargar código: 2 minutos
├─ Instalar dependencias: 5 minutos
├─ Crear base de datos: 1 minuto
└─ Configurar .env: 1 minuto
   SUBTOTAL: 9 minutos

TOTAL: 17 minutos
```

---

## 🚨 ERRORES MÁS COMUNES Y CÓMO EVITARLOS

| Error | Causa | Solución |
|-------|-------|----------|
| "Python no es reconocido" | No está en PATH | Reinstalar marcando "Add Python to PATH" |
| "MySQL no es reconocido" | No está en PATH | Reiniciar CMD después de instalar |
| "ModuleNotFoundError" | Dependencias faltantes | Ejecutar: `pip install -r requirements.txt` |
| "Can't connect to MySQL" | MySQL no está corriendo | Ejecutar: `net start MySQL80` |
| "Access denied for user" | Contraseña incorrecta | Verificar contraseña en `.env` |

---

## 💡 TIPS IMPORTANTES

1. **Instalar como Administrador**
   - Click derecho en instaladores
   - Seleccionar "Ejecutar como administrador"

2. **Copiar bien la contraseña de MySQL**
   - No debe tener espacios
   - Puede tener caracteres especiales (cuidado)
   - Guardarla en un lugar seguro

3. **Reiniciar después de instalar**
   - Si algo falla, reiniciar la computadora
   - A veces las instalaciones requieren reinicio

4. **Usar CMD/Terminal como Administrador**
   - Windows: Click derecho > "Ejecutar como administrador"
   - macOS/Linux: Usar `sudo` si es necesario

---

## 📞 SOPORTE DURANTE LA INSTALACIÓN

Si el cliente tiene dudas:

1. Envía: GUIA_INSTALACION_CLIENTE.md (documento completo)
2. Envía: INSTALACION_RAPIDA.md (versión corta)
3. Envía: verificar_requerimientos.bat (para Windows)
4. Envía: verificar_requerimientos.sh (para macOS/Linux)

---

## 🎓 RESUMEN PARA EXPLICAR AL CLIENTE

**Versión Corta (30 segundos):**

> "Necesitas instalar dos programas:
> 1. Python (para ejecutar el sistema)
> 2. MySQL (para guardar los datos)
> 
> Luego yo instalo Refaccionaria Oviedo en tu computadora.
> 
> En total: 15 minutos."

**Versión Media (2 minutos):**

> "Python es el 'motor' del sistema.
> MySQL es la 'base de datos' donde guardamos todo.
> 
> Ambos son gratuitos.
> Yo te envío los enlaces de descarga.
> Tú los instalas (10 minutos).
> Yo termino la instalación del sistema (5 minutos).
> 
> Después estará listo para usar."

---

## ✨ CONCLUSIÓN

**CLIENTE DEBE INSTALAR:**
- ✅ Python 3.8+ 
- ✅ MySQL 8.0+

**CLIENTE YA TIENE:**
- ✅ Navegador web
- ✅ Sistema operativo

**TÚ INSTALAS TODO LO DEMÁS.**

---

**Fecha:** 3 de febrero de 2026  
**Sistema:** Refaccionaria Oviedo ERP v1.0
