"""
Aba do decodificador de imagem
"""

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

from src.config import UI_CONFIG
from src.decoders.image_decoder import ImageDecoder

class ImageDecoderTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.decoder = ImageDecoder()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface da aba"""
        # Frame de instruções
        instructions = ttk.Label(self,
            text="Decodificador de Imagem\n\n" +
                 "Funcionalidades:\n" +
                 "- Análise de QR codes e dot codes\n" +
                 "- Detecção de padrões em imagens\n" +
                 "- Ajuste de brilho/contraste\n" +
                 "- Análise de cores hexadecimais\n" +
                 "- Detecção de sigilos e símbolos",
            justify=tk.LEFT,
            style='TLabel')
        instructions.pack(pady=10, padx=10, anchor=tk.W)
        
        # Frame de controles
        controls = ttk.Frame(self)
        controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(controls,
            text="Carregar Imagem",
            command=self.load_image,
            style='TButton').pack(side=tk.LEFT, padx=5)
        
        # Frame para exibir a imagem
        self.image_frame = ttk.Frame(self)
        self.image_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Área de resultados
        self.result_text = tk.Text(self,
            height=10,
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
        
    def load_image(self):
        """Carrega e analisa uma imagem"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Imagem",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Todos os arquivos", "*.*")
            ])
        
        if file_path:
            try:
                # Carregar e processar a imagem
                image = Image.open(file_path)
                
                # Redimensionar mantendo proporção
                display_size = (800, 600)
                image.thumbnail(display_size, Image.Resampling.LANCZOS)
                
                # Converter para PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Limpar frame anterior
                for widget in self.image_frame.winfo_children():
                    widget.destroy()
                
                # Exibir imagem
                image_label = ttk.Label(self.image_frame, image=photo)
                image_label.image = photo  # Manter referência
                image_label.pack(pady=10)
                
                # Processar a imagem
                results = self.decoder.analyze_image(file_path)
                
                # Mostrar resultados
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Resultados da análise:\n\n")
                
                for key, value in results.items():
                    self.result_text.insert(tk.END, f"{key}: {value}\n")
                    
            except Exception as e:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Erro ao carregar imagem: {str(e)}")
