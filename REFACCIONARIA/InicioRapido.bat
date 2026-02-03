@echo off
title Refaccionaria Oviedo - Inicio Rapido
color 0B
cls

echo.
echo ========================================================================
echo           REFACCIONARIA OVIEDO - INICIO RAPIDO
echo ========================================================================
echo.
echo  Abriendo sistema en tu navegador...
echo.

cd /d "%~dp0"
start python launch_browser.py

echo  Sistema iniciado!
echo  Se abrira automaticamente en tu navegador
echo.
echo  Para detener: Cierra esta ventana o presiona Ctrl+C
echo.

timeout /t 3 >nul
exit
