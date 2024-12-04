"""
Aba do decodificador de texto
"""

import tkinter as tk
from tkinter import ttk

from src.config import UI_CONFIG
from src.decoders.text_decoder import TextDecoder

class TextDecoderTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.decoder = TextDecoder()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface da aba"""
        # Frame de instruções
        instructions = ttk.Label(self,
            text="Decodificador de Texto\n\n" +
                 "Suporta os seguintes formatos:\n" +
                 "- Código Morse\n" +
                 "- Cifra de Bacon\n" +
                 "- Cifra de Vigenère\n" +
                 "- Tap Code\n" +
                 "- Braille\n" +
                 "- Análise de bandeiras e símbolos",
            justify=tk.LEFT,
            style='TLabel')
        instructions.pack(pady=10, padx=10, anchor=tk.W)
        
        # Frame de entrada
        input_frame = ttk.Frame(self)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(input_frame,
            text="Texto para decodificar:",
            style='TLabel').pack(anchor=tk.W)
        
        # Área de entrada
        self.text_input = tk.Text(input_frame,
            height=10,
            bg=UI_CONFIG['theme']['text_bg'],
            fg=UI_CONFIG['theme']['text_fg'],
            insertbackground=UI_CONFIG['theme']['text_fg'])
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar para entrada
        input_scroll = ttk.Scrollbar(self.text_input,
            orient="vertical",
            command=self.text_input.yview)
        input_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_input.configure(yscrollcommand=input_scroll.set)
        
        # Frame de controles
        controls = ttk.Frame(self)
        controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(controls,
            text="Decodificar",
            command=self.decode_text,
            style='TButton').pack(side=tk.LEFT, padx=5)
        
        # Área de resultados
        ttk.Label(self,
            text="Resultados:",
            style='TLabel').pack(anchor=tk.W, padx=10)
        
        self.text_output = tk.Text(self,
            height=10,
            bg=UI_CONFIG['theme']['text_bg'],
            fg=UI_CONFIG['theme']['text_fg'],
            insertbackground=UI_CONFIG['theme']['text_fg'])
        self.text_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar para saída
        output_scroll = ttk.Scrollbar(self.text_output,
            orient="vertical",
            command=self.text_output.yview)
        output_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_output.configure(yscrollcommand=output_scroll.set)
        
    def decode_text(self):
        """Decodifica o texto inserido"""
        text = self.text_input.get("1.0", tk.END).strip()
        if text:
            try:
                # Limpar área de resultados
                self.text_output.delete(1.0, tk.END)
                self.text_output.insert(tk.END, "Analisando texto...\n\n")
                
                # Processar texto
                results = self.decoder.decode_text(text)
                
                # Mostrar resultados
                self.text_output.delete(1.0, tk.END)
                self.text_output.insert(tk.END, "Resultados da decodificação:\n\n")
                
                for method, result in results.items():
                    self.text_output.insert(tk.END, f"\n{method}:\n")
                    self.text_output.insert(tk.END, f"{result}\n")
                    self.text_output.insert(tk.END, "-" * 50 + "\n")
                    
            except Exception as e:
                self.text_output.delete(1.0, tk.END)
                self.text_output.insert(tk.END, f"Erro: {str(e)}")
