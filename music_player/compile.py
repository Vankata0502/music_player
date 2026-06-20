import PyInstaller.__main__
import os

for folder in ["build", "dist"]:
    if os.path.exists(folder):
        try:
            import shutil
            shutil.rmtree(folder)
        except Exception:
            pass

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--icon=assets/play_button.ico',  # <- ТОЗИ нов ред слага иконата на самия .exe файл!
    '--add-data=assets;assets',
    '--hidden-import=pygame'
])
