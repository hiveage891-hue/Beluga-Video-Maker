@echo off
:: Pega o caminho de onde o .bat está e sobe um nível
set "BASE_DIR=%~dp0.."
cd /d "%BASE_DIR%"

echo Running from: %CD%

:: 1. Limpeza
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist gui.spec del /q gui.spec

:: 2. Pastas
if not exist input\avatares mkdir input\avatares
if not exist output mkdir output
if not exist assets\fonts mkdir assets\fonts

:: 3. Build (Nota: Windows usa ; no --add-data)
python -m PyInstaller --noconsole --onefile ^
    --hidden-import "PIL._tkinter_finder" ^
    --add-data "assets;assets" ^
    --add-data "input;input" ^
    gui.py

:: 4. Execução
if exist dist\gui.exe (
    start dist\gui.exe
) else (
    echo Error: Build failed.
    pause
)
