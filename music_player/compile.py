import PyInstaller.__main__
import os

# Изчистване на старите папки автоматично
for folder in ["build", "dist"]:
    if os.path.exists(folder):
        try:
            import shutil
            shutil.rmtree(folder)
        except Exception:
            pass

# Стартиране на PyInstaller директно през Python
PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--add-data=assets;assets',
    '--hidden-import=pygame'
])