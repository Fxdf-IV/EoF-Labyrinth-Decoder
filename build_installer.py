import PyInstaller.__main__
import os

# Configuração do executável
PyInstaller.__main__.run([
    'src/main.py',
    '--onefile',
    '--windowed',
    '--icon=icon.ico',
    '--name=EoFEnigmaDecoder',
    '--add-data=resources;resources',
    '--hidden-import=PIL._tkinter_finder'
])
