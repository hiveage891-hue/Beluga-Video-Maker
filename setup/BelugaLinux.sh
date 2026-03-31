#!/bin/bash

# --- ACESSIBILIDADE DE CAMINHO ---
# Pega o diretório onde o script .sh está (./setup)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define a PASTA PRINCIPAL (um nível acima do /setup)
BASE_DIR="$(dirname "$SCRIPT_DIR")"
cd "$BASE_DIR"

echo "Running from: $BASE_DIR"

# 1. Limpeza de builds antigos
rm -rf build dist gui.spec

# 2. Garante as pastas necessárias
mkdir -p input/avatares output assets/fonts

# 3. Build com PyInstaller
python3 -m PyInstaller --noconsole --onefile \
    --hidden-import "PIL._tkinter_finder" \
    --add-data "assets:assets" \
    --add-data "input:input" \
    gui.py

# 4. Execução
if [ -f "dist/gui" ]; then
    chmod +x dist/gui
    ./dist/gui
else
    echo "Error: gui file not found in dist/"
    exit 1
fi
