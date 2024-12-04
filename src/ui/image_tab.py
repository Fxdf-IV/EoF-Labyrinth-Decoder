"""
Aba do decodificador de imagem
"""

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageEnhance
import cv2
import numpy as np
import os

from src.config import UI_CONFIG
from src.decoders.image_decoder import ImageDecoder

class ImageDecoderTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.decoder = ImageDecoder()
        self.parent = parent
        self.current_image = None
        self.original_cv_image = None
        self.current_cv_image = None
        
        # Configurar estilo global das scrollbars
        style = ttk.Style()
        style.configure("Custom.Vertical.TScrollbar",
                      background="black",
                      troughcolor="black",
                      arrowcolor="#00ff00")
        style.map("Custom.Vertical.TScrollbar",
                 background=[('active', '#003300')],
                 arrowcolor=[('active', '#00ff00')])
        
        # Configurar estilo
        style.configure("Dark.TFrame", background="black")
        style.configure("Dark.TLabelframe", background="black", foreground="#00ff00")
        style.configure("Dark.TLabelframe.Label", background="black", foreground="#00ff00")
        style.configure("Dark.TLabel", background="black", foreground="#00ff00")
        style.configure("Dark.TButton", background="black", foreground="#00ff00")
        style.configure("Dark.Horizontal.TScale", background="black", troughcolor="black")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface da aba"""
        # Frame principal
        main_frame = ttk.Frame(self, style="Dark.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame esquerdo para imagem e controles (50% da largura)
        left_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame direito para resultados (50% da largura)
        right_frame = ttk.Frame(main_frame, style="Dark.TFrame", width=600)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        right_frame.pack_propagate(False)  # Manter largura fixa
        
        # Frame de instruções
        instructions = ttk.Label(left_frame,
            text="Decodificador de Imagem\n\n" +
                 "Funcionalidades:\n" +
                 "- Análise de QR codes e dot codes\n" +
                 "- Detecção de padrões em imagens\n" +
                 "- Ajuste de brilho/contraste\n" +
                 "- Análise de cores hexadecimais\n" +
                 "- Detecção de sigilos e símbolos",
            justify=tk.LEFT,
            style="Dark.TLabel")
        instructions.pack(pady=5, anchor=tk.W)
        
        # Frame de controles
        controls_frame = ttk.LabelFrame(left_frame, text="Controles", padding=5,
                                      style="Dark.TLabelframe")
        controls_frame.pack(fill=tk.X, pady=5)
        
        # Botões com estilo escuro
        ttk.Button(controls_frame,
                  text="Carregar Imagem",
                  command=self.load_image,
                  style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_frame,
                  text="Analisar",
                  command=self.analyze_current_image,
                  style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        
        # Frame de ajustes
        adjustments_frame = ttk.LabelFrame(left_frame, text="Ajustes de Imagem",
                                         padding=5, style="Dark.TLabelframe")
        adjustments_frame.pack(fill=tk.X, pady=5)
        
        # Labels e controles com estilo escuro
        ttk.Label(adjustments_frame, text="Brilho:",
                 style="Dark.TLabel").grid(row=0, column=0, padx=5)
        self.brightness_var = tk.DoubleVar(value=1.0)
        brightness_scale = ttk.Scale(adjustments_frame, from_=-100.0, to=100.0,
                                   variable=self.brightness_var,
                                   command=self.update_image,
                                   style="Dark.Horizontal.TScale")
        brightness_scale.grid(row=0, column=1, sticky="ew", padx=5)
        
        ttk.Label(adjustments_frame, text="Contraste:",
                 style="Dark.TLabel").grid(row=1, column=0, padx=5)
        self.contrast_var = tk.DoubleVar(value=1.0)
        contrast_scale = ttk.Scale(adjustments_frame, from_=0.1, to=3.0,
                                 variable=self.contrast_var,
                                 command=self.update_image,
                                 style="Dark.Horizontal.TScale")
        contrast_scale.grid(row=1, column=1, sticky="ew", padx=5)
        
        ttk.Label(adjustments_frame, text="Gamma:",
                 style="Dark.TLabel").grid(row=2, column=0, padx=5)
        self.gamma_var = tk.DoubleVar(value=1.0)
        gamma_scale = ttk.Scale(adjustments_frame, from_=0.1, to=3.0,
                              variable=self.gamma_var,
                              command=self.update_image,
                              style="Dark.Horizontal.TScale")
        gamma_scale.grid(row=2, column=1, sticky="ew", padx=5)

        # Valores atuais dos ajustes
        self.brightness_label = ttk.Label(adjustments_frame, text="0",
                                        style="Dark.TLabel")
        self.brightness_label.grid(row=0, column=2, padx=5)
        
        self.contrast_label = ttk.Label(adjustments_frame, text="1.0",
                                      style="Dark.TLabel")
        self.contrast_label.grid(row=1, column=2, padx=5)
        
        self.gamma_label = ttk.Label(adjustments_frame, text="1.0",
                                   style="Dark.TLabel")
        self.gamma_label.grid(row=2, column=2, padx=5)
        
        # Botão de Reset com estilo escuro
        ttk.Button(adjustments_frame,
                  text="Reset",
                  command=self.reset_adjustments,
                  style="Dark.TButton").grid(row=3, column=0, columnspan=3, pady=5)
        
        adjustments_frame.columnconfigure(1, weight=1)
        
        # Frame da imagem
        self.image_frame = ttk.Frame(left_frame, style="Dark.TFrame")
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Área de resultados
        results_frame = ttk.LabelFrame(right_frame, text="Resultados",
                                     padding=5, style="Dark.TLabelframe")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar área de texto com cores escuras
        self.result_text = tk.Text(results_frame,
                                 bg="black",
                                 fg="#00ff00",
                                 insertbackground="#00ff00",
                                 selectbackground="#003300",
                                 selectforeground="#00ff00",
                                 font=("Courier", 10),
                                 width=70)  # Aumentar largura
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
    def load_image(self):
        """Carrega uma nova imagem"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Carregar imagem com OpenCV
                self.original_cv_image = cv2.imread(file_path)
                if self.original_cv_image is None:
                    # Tentar carregar com imdecode se imread falhar
                    img_array = np.fromfile(file_path, dtype=np.uint8)
                    self.original_cv_image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    if self.original_cv_image is None:
                        raise ValueError("Não foi possível carregar a imagem")
                
                self.current_cv_image = self.original_cv_image.copy()
                self.display_current_image()
                self.analyze_current_image()
                
            except Exception as e:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Erro ao carregar imagem: {str(e)}")
    
    def update_image(self, *args):
        """Atualiza a imagem com os ajustes atuais"""
        if self.original_cv_image is not None:
            try:
                # Aplicar ajustes
                img = self.original_cv_image.copy()
                
                # Ajuste de brilho e contraste
                brightness = self.brightness_var.get()
                contrast = self.contrast_var.get()
                
                # Atualizar labels com valores atuais
                self.brightness_label.config(text=f"{brightness:.1f}")
                self.contrast_label.config(text=f"{contrast:.1f}")
                self.gamma_label.config(text=f"{self.gamma_var.get():.1f}")
                
                # Aplicar brilho e contraste
                img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
                
                # Ajuste de gamma
                gamma = self.gamma_var.get()
                inv_gamma = 1.0 / gamma
                table = np.array([((i / 255.0) ** inv_gamma) * 255
                                for i in np.arange(0, 256)]).astype("uint8")
                img = cv2.LUT(img, table)
                
                self.current_cv_image = img
                self.display_current_image()
                
            except Exception as e:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Erro ao atualizar imagem: {str(e)}")
    
    def reset_adjustments(self):
        """Reseta todos os ajustes para seus valores padrão"""
        self.brightness_var.set(0.0)  # Valor central para brilho
        self.contrast_var.set(1.0)    # Valor neutro para contraste
        self.gamma_var.set(1.0)       # Valor neutro para gamma
        
        # Atualizar labels
        self.brightness_label.config(text="0.0")
        self.contrast_label.config(text="1.0")
        self.gamma_label.config(text="1.0")
        
        if self.original_cv_image is not None:
            self.current_cv_image = self.original_cv_image.copy()
            self.display_current_image()
    
    def display_current_image(self):
        """Exibe a imagem atual no frame"""
        if self.current_cv_image is not None:
            # Converter de BGR para RGB
            rgb_image = cv2.cvtColor(self.current_cv_image, cv2.COLOR_BGR2RGB)
            
            # Converter para PIL Image
            pil_image = Image.fromarray(rgb_image)
            
            # Redimensionar mantendo proporção
            display_size = (800, 600)
            pil_image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Converter para PhotoImage
            photo = ImageTk.PhotoImage(pil_image)
            
            # Limpar frame anterior
            for widget in self.image_frame.winfo_children():
                widget.destroy()
            
            # Criar label para exibir a imagem
            image_label = ttk.Label(self.image_frame, image=photo)
            image_label.image = photo
            image_label.pack()
    
    def analyze_current_image(self):
        """Analisa a imagem atual"""
        if self.current_cv_image is not None:
            try:
                # Analisar imagem atual
                results = self.decoder.analyze_image(self.current_cv_image)
                
                # Mostrar resultados
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Resultados da análise:\n\n")
                
                for key, value in results.items():
                    self.result_text.insert(tk.END, f"{key}: {value}\n")
                    
            except Exception as e:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Erro na análise: {str(e)}")
