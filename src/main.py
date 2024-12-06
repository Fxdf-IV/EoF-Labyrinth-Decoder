"""
Arquivo principal do EoF Enigma Decoder
"""

import tkinter as tk
import os
import sys
import ui
from pathlib import Path

# Adicionar o diretório src ao PYTHONPATH
src_dir = Path(__file__).parent
sys.path.append(str(src_dir))

from ui.main_window import MainWindow

def main():
    try:
        # Criar janela principal
        root = tk.Tk()
        app = MainWindow(root)
        
        # Criar e iniciar a aplicação
        app.run()
        
        # Iniciar loop principal
        root.mainloop()
        
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
