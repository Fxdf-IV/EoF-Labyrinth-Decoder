"""
Janela principal do aplicativo
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

from src.ui.labyrinth_tab import LabyrinthTab
from src.ui.intro_tab import IntroTab
from src.ui.text_tab import TextTab
from src.ui.image_tab import ImageDecoderTab as ImageTab
from src.ui.audio_tab import AudioDecoderTab as AudioTab

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_style()
        self.setup_notebook()
        
    def setup_window(self):
        """Configura a janela principal"""
        # Configurações da janela
        self.root.title("EoF Labyrinth Decoder")
        self.root.geometry("1024x768")
        
        # Configura o grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Cor de fundo
        self.root.configure(bg='black')
        
    def setup_style(self):
        """Configura o estilo da interface"""
        style = ttk.Style()
        
        # Configura o tema
        style.theme_use('default')
        
        # Configuração do notebook
        style.configure('TNotebook',
                      background='black',
                      borderwidth=0)
        style.configure('TNotebook.Tab',
                      background='black',
                      foreground='#00ff00',
                      padding=[10, 2],
                      font=('Consolas', 10))
        style.map('TNotebook.Tab',
                 background=[('selected', '#003300')],
                 foreground=[('selected', '#00ff00')])
        
        # Configuração dos frames
        style.configure('TFrame',
                      background='black')
        
        # Configuração das labels
        style.configure('TLabel',
                      background='black',
                      foreground='#00ff00',
                      font=('Consolas', 10))
        
        # Configuração dos botões
        style.configure('TButton',
                      background='black',
                      foreground='#00ff00',
                      borderwidth=1,
                      font=('Consolas', 10))
        style.map('TButton',
                 background=[('active', '#003300')],
                 foreground=[('active', '#00ff00')])
                 
        # Configuração da scrollbar
        style.configure('TScrollbar',
                      background='black',
                      bordercolor='#00ff00',
                      arrowcolor='#00ff00',
                      troughcolor='black')
                      
        # Configuração do radiobutton
        style.configure('TRadiobutton',
                      background='black',
                      foreground='#00ff00',
                      font=('Consolas', 10))
        
    def setup_notebook(self):
        """Configura o notebook com as abas"""
        # Cria o notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Adiciona as abas
        self.intro_tab = IntroTab(self.notebook)
        self.notebook.add(self.intro_tab, text="Informações")
        
        self.labyrinth_tab = LabyrinthTab(self.notebook)
        self.notebook.add(self.labyrinth_tab, text="Labyrinth Decoder")
        
        self.text_tab = TextTab(self.notebook)
        self.notebook.add(self.text_tab, text="Text Decoder")
        
        self.image_tab = ImageTab(self.notebook)
        self.notebook.add(self.image_tab, text="Image Decoder")
        
        self.audio_tab = AudioTab(self.notebook)
        self.notebook.add(self.audio_tab, text="Audio Decoder")
        
    def run(self):
        self.root.mainloop()

def main():
    root = tk.Tk()
    app = MainWindow(root)
    app.run()
    
if __name__ == "__main__":
    main()
