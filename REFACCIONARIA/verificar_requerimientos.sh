#!/bin/bash

# Script de verificación de requisitos para macOS/Linux
# Ejecutar: bash verificar_requerimientos.sh

echo ""
echo "========================================================================"
echo "              VERIFICADOR DE REQUISITOS"
echo "                  Refaccionaria Oviedo"
echo "========================================================================"
echo ""

requirements_ok=true

# Verificar Python
echo "[1/5] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "   ❌ ERROR: Python no está instalado"
    echo "      Instala con: brew install python3 (macOS)"
    echo "      O: sudo apt install python3 (Linux)"
    requirements_ok=false
else
    echo "   ✅ $(python3 --version)"
fi

# Verificar pip
echo ""
echo "[2/5] Verificando pip (gestor de paquetes Python)..."
if ! command -v pip3 &> /dev/null; then
    echo "   ❌ ERROR: pip no está instalado"
    requirements_ok=false
else
    echo "   ✅ $(pip3 --version)"
fi

# Verificar MySQL
echo ""
echo "[3/5] Verificando MySQL..."
if ! command -v mysql &> /dev/null; then
    echo "   ❌ ERROR: MySQL no está instalado"
    echo "      Instala con: brew install mysql (macOS)"
    echo "      O: sudo apt install mysql-server (Linux)"
    requirements_ok=false
else
    echo "   ✅ $(mysql --version)"
fi

# Verificar Git (Opcional)
echo ""
echo "[4/5] Verificando Git (Opcional)..."
if ! command -v git &> /dev/null; then
    echo "   ⚠️  Git no encontrado (no es crítico)"
    echo "      Instala con: brew install git (macOS)"
    echo "      O: sudo apt install git (Linux)"
else
    echo "   ✅ $(git --version)"
fi

# Verificar espacio en disco
echo ""
echo "[5/5] Verificando espacio en disco..."
if [ "$(uname)" == "Darwin" ]; then
    disk_free=$(df / | awk 'NR==2 {print int($4/1024/1024)}')" GB"
    echo "   ✅ Espacio disponible: $disk_free"
else
    disk_free=$(df / | awk 'NR==2 {print int($4/1024/1024)}')" GB"
    echo "   ✅ Espacio disponible: $disk_free"
fi

echo ""
echo "========================================================================"

if [ "$requirements_ok" = false ]; then
    echo ""
    echo "❌ FALTA INSTALAR REQUISITOS"
    echo ""
    echo "Por favor instala los programas marcados como ERROR antes de continuar."
    echo ""
    echo "Después, ejecuta este script nuevamente."
    echo ""
    exit 1
else
    echo ""
    echo "✅ TODOS LOS REQUISITOS ESTÁN INSTALADOS"
    echo ""
    echo "Próximos pasos:"
    echo "   1. Abre Terminal en la carpeta del proyecto"
    echo "   2. Ejecuta: pip3 install -r requirements.txt"
    echo "   3. Configura el archivo .env"
    echo "   4. Crea la base de datos"
    echo "   5. Ejecuta: python3 launch_desktop.py"
    echo ""
    echo "Para más información, lee: GUIA_INSTALACION_CLIENTE.md"
    echo ""
    exit 0
fi
