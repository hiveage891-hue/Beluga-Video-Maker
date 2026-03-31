# Beluga Video Maker 🐱‍💻

Um gerador de vídeos estilo conversas do Discord (Beluga/Hecker) feito em Python.

## 🚀 Como Usar
1. Instale as dependências: `pip install customtkinter pillow moviepy numpy`
2. Coloque as fontes em `assets/fonts/`
3. Coloque os avatares em `input/avatares/`
4. Execute o script: `./setup/BelugaLinux.sh`

## 🛠 Estrutura
- **gui.py**: Interface CustomTkinter para configurar a cena.
- **scripts/desenhador.py**: Motor de renderização de frames 1920x1080.
- **scripts/editor_video.py**: Compilador de vídeo com áudio usando MoviePy.