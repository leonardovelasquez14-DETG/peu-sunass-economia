@echo off
chcp 65001 > nul
cd /d "%~dp0"
title Simulador PEU SUNASS - Economia (BackBone Academy)

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 simulador.py
    goto :fin
)

where python >nul 2>nul
if %errorlevel%==0 (
    python simulador.py
    goto :fin
)

where python3 >nul 2>nul
if %errorlevel%==0 (
    python3 simulador.py
    goto :fin
)

echo.
echo [ERROR] No se encontro Python 3 instalado en este equipo.
echo Descargalo gratis en: https://www.python.org/downloads/
echo Durante la instalacion, marca "Add python.exe to PATH".
echo.

:fin
pause
