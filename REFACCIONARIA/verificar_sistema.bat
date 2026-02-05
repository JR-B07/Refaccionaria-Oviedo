@echo off
setlocal enabledelayedexpansion
title Refaccionaria - Verificador de Sistema

cd /d "%~dp0"
color 0B
cls

echo.
echo ========================================
echo   VERIFICADOR DEL SISTEMA
echo   Refaccionaria ERP
echo ========================================
echo.

echo Ejecutando diagnostico completo...
echo.

python diagnostico.py

echo.
pause