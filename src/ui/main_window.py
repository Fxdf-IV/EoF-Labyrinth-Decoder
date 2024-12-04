"""
Janela principal do decodificador
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.ui.labyrinth_tab import LabyrinthTab
from src.ui.intro_tab import IntroTab
from src.ui.text_tab import TextDecoderTab
from src.ui.image_tab import ImageDecoderTab
from src.ui.audio_tab import AudioDecoderTab

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_tabs()
        
    def setup_window(self):
        self.root.title("EoF Labyrinth Decoder")
        self.root.geometry("800x600")
        
        # Configuração do tema escuro
        style = ttk.Style()
        style.theme_use('alt')  # Usa o tema alternativo como base
        
        # Configurações gerais
        style.configure(".", 
            background='black',
            foreground='#00ff00',
            fieldbackground='black',
            troughcolor='black',
            arrowcolor='#00ff00')
        
        # Configuração específica para cada tipo de widget
        style.configure("TNotebook", background='black', borderwidth=0)
        style.configure("TNotebook.Tab", 
            background='black',
            foreground='#00ff00',
            borderwidth=1,
            bordercolor='#00ff00',
            padding=5)
        style.configure("TFrame", background='black')
        style.configure("TLabel", background='black', foreground='#00ff00')
        style.configure("TButton",
            background='black',
            foreground='#00ff00',
            bordercolor='#00ff00',
            relief='solid',
            borderwidth=1)
        
        # Configuração dos estados dos widgets
        style.map("TNotebook.Tab",
            background=[('selected', 'black'),
                       ('active', 'black'),
                       ('!selected', 'black')],
            foreground=[('selected', '#00ff00'),
                       ('active', '#00ff00'),
                       ('!selected', '#00ff00')])
                       
        style.map("TButton",
            background=[('active', 'black'),
                       ('pressed', 'black'),
                       ('disabled', 'black')],
            foreground=[('active', '#00ff00'),
                       ('pressed', '#00ff00'),
                       ('disabled', '#00ff00')])
        
        # Configuração da janela principal
        self.root.configure(background='black')
        
    def setup_tabs(self):
        # Notebook para as abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Aba inicial com informações
        intro_tab = IntroTab(self.notebook)
        self.notebook.add(intro_tab, text="Informações")
        
        # Aba do decodificador do labirinto
        labyrinth_tab = LabyrinthTab(self.notebook)
        self.notebook.add(labyrinth_tab, text="Labyrinth Decoder")
        
        # Aba do decodificador de texto
        text_tab = TextDecoderTab(self.notebook)
        self.notebook.add(text_tab, text="Text Decoder")
        
        # Aba do decodificador de imagem
        image_tab = ImageDecoderTab(self.notebook)
        self.notebook.add(image_tab, text="Image Decoder")
        
        # Aba do decodificador de áudio
        audio_tab = AudioDecoderTab(self.notebook)
        self.notebook.add(audio_tab, text="Audio Decoder")
        
    def run(self):
        self.root.mainloop()

def main():
    app = MainWindow()
    app.run()
    
if __name__ == "__main__":
    main()
