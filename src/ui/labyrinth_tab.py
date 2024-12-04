"""
Interface do decodificador do labirinto
"""

import tkinter as tk
from tkinter import ttk, filedialog
from src.decoders.labyrinth_decoder import LabyrinthDecoder

class LabyrinthTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.decoder = LabyrinthDecoder()
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal com scroll
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botão de seleção de pasta
        select_btn = ttk.Button(main_frame, text="Selecionar Pasta", command=self.select_folder)
        select_btn.pack(pady=10)
        
        # Canvas e scrollbar para resultados
        self.canvas = tk.Canvas(main_frame, background='black')
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Área de resultados
        self.results_text = tk.Text(self.scrollable_frame, 
                                  wrap=tk.WORD, 
                                  width=80, 
                                  height=30,
                                  background='black',
                                  foreground='#00ff00',
                                  font=('Courier', 10))
        self.results_text.pack(pady=10, padx=10)
        
        # Configuração final do scroll
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def select_folder(self):
        folder = filedialog.askdirectory(title="Selecione a pasta do Labirinto")
        if folder:
            self.explore_paths(folder)
            
    def explore_paths(self, folder_path):
        # Limpa resultados anteriores
        self.results_text.delete(1.0, tk.END)
        
        # Explora os caminhos
        results = self.decoder.explore_paths(folder_path)
        
        # Formata e exibe os resultados
        for i in range(len(results['items'])):
            self.results_text.insert(tk.END, f"\n{results['items'][i]}\n\n")
            self.results_text.insert(tk.END, f"{results['paths'][i]}\n")
            self.results_text.insert(tk.END, f"{results['sequences'][i]}\n")
            self.results_text.insert(tk.END, f"{results['files'][i]}\n\n")
            self.results_text.insert(tk.END, f"{results['computer_hints'][i]}\n\n")
            self.results_text.insert(tk.END, f"{results['technical_hints'][i]}\n")
            self.results_text.insert(tk.END, "\n" + "-"*50 + "\n")
