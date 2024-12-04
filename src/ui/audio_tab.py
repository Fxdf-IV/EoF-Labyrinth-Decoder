"""
Aba do decodificador de áudio
"""

import tkinter as tk
from tkinter import ttk, filedialog

from src.config import UI_CONFIG
from src.decoders.audio_decoder import AudioDecoder

class AudioDecoderTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.decoder = AudioDecoder()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface da aba"""
        # Frame de instruções
        instructions = ttk.Label(self,
            text="Decodificador de Áudio\n\n" +
                 "Funcionalidades:\n" +
                 "- Análise de espectrograma\n" +
                 "- Detecção de Morse em áudio\n" +
                 "- Análise de frequências\n" +
                 "- Detecção de padrões temporais",
            justify=tk.LEFT,
            style='TLabel')
        instructions.pack(pady=10, padx=10, anchor=tk.W)
        
        # Frame de controles
        controls = ttk.Frame(self)
        controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(controls,
            text="Carregar Áudio",
            command=self.load_audio,
            style='TButton').pack(side=tk.LEFT, padx=5)
        
        # Frame para visualização
        self.audio_frame = ttk.Frame(self)
        self.audio_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Área de resultados
        self.result_text = tk.Text(self,
            height=20,
            bg=UI_CONFIG['theme']['text_bg'],
            fg=UI_CONFIG['theme']['text_fg'],
            insertbackground=UI_CONFIG['theme']['text_fg'])
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar para resultados
        scrollbar = ttk.Scrollbar(self.result_text,
            orient="vertical",
            command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
    def load_audio(self):
        """Carrega e analisa um arquivo de áudio"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Áudio",
            filetypes=[
                ("Arquivos de áudio", "*.wav *.mp3 *.ogg *.flac"),
                ("Todos os arquivos", "*.*")
            ])
        
        if file_path:
            try:
                # Limpar visualização anterior
                for widget in self.audio_frame.winfo_children():
                    widget.destroy()
                
                # Processar o áudio
                results = self.decoder.analyze_audio(file_path)
                
                # Mostrar resultados
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Resultados da análise de áudio:\n\n")
                
                for key, value in results.items():
                    self.result_text.insert(tk.END, f"{key}: {value}\n")
                    
            except Exception as e:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Erro ao processar áudio: {str(e)}")
