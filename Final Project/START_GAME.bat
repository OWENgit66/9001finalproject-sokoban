@echo off
chcp 65001 >nul
title Sokoban Game
color 0B

echo.
echo  =====================================
echo      Sokoban Game Launcher
echo  =====================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.x from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python detected
echo.

REM Check and install dependencies
echo [*] Checking dependencies...
python -m pip install -r requirements.txt --quiet --upgrade
if errorlevel 1 (
    echo [WARNING] Failed to install some dependencies
    echo.
)

echo.
echo [*] Starting game...
echo.
echo  =====================================
echo.

REM Run the game
py Sokoban.py

if errorlevel 1 (
    echo.
    echo  =====================================
    echo [ERROR] Game crashed!
    echo.
    echo Please check:
    echo 1. Resource files exist (Picture/Player.png, etc.)
    echo 2. Level file exists (levels.txt)
    echo.
    pause
)



