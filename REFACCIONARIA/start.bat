@echo off
setlocal enabledelayedexpansion
title Refaccionaria - Servidor API

cd /d "%~dp0"

color 0B
cls

echo.
echo ========================================
echo   REFACCIONARIA - SERVIDOR API
echo ========================================
echo.

REM Verificar MySQL
echo Verificando MySQL...
sc query MySQL >nul 2>&1
if not errorlevel 1 (
    sc query MySQL | find "RUNNING" >nul
    if errorlevel 1 (
        echo Iniciando MySQL...
        net start MySQL >nul 2>&1
        if not errorlevel 1 (
            echo MySQL iniciado
        )
    ) else (
        echo MySQL ya esta ejecutandose
    )
) else (
    sc query MySQL80 >nul 2>&1
    if not errorlevel 1 (
        sc query MySQL80 | find "RUNNING" >nul
        if errorlevel 1 (
            echo Iniciando MySQL80...
            net start MySQL80 >nul 2>&1
            if not errorlevel 1 (
                echo MySQL80 iniciado
            )
        ) else (
            echo MySQL80 ya esta ejecutandose
        )
    ) else (
        echo [ADVERTENCIA] MySQL no esta instalado
    )
)

echo.
echo Verificando dependencias...
python -c "import uvicorn" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -q fastapi uvicorn sqlalchemy pymysql requests webview python-dotenv >nul 2>&1
)

echo.
echo Iniciando servidor en puerto 8001...
echo API disponible en: http://127.0.0.1:8001
echo Documentacion en: http://127.0.0.1:8001/docs
echo.
echo (Los logs se guardaran en server.log)
echo.

python start.py >> server.log 2>&1
