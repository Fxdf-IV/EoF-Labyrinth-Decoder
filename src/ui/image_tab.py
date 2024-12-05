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
                 "- Ajuste de brilho/contraste/gamma\n" +
                 "- Ajuste de saturação/nuance\n" +
                 "- Inversão de cores e rotação\n" +
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
                  
        ttk.Button(controls_frame,
                  text="Inverter Cores",
                  command=self.invert_colors,
                  style="Dark.TButton").pack(side=tk.LEFT, padx=5)
                  
        ttk.Button(controls_frame,
                  text="Rotacionar",
                  command=self.rotate_image,
                  style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        
        # Botão para carregar imagem teste
        ttk.Button(controls_frame,
                  text="Carregar Imagem Teste",
                  command=self.load_test_image,
                  style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        
        # Frame de ajustes
        adjustments_frame = ttk.LabelFrame(left_frame, text="Ajustes de Imagem",
                                         padding=5, style="Dark.TLabelframe")
        adjustments_frame.pack(fill=tk.X, pady=5)
        
        # Labels e controles com estilo escuro
        ttk.Label(adjustments_frame, text="Brilho:",
                 style="Dark.TLabel").grid(row=0, column=0, padx=5)
        self.brightness_var = tk.DoubleVar(value=0.0)
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
        
        ttk.Label(adjustments_frame, text="Saturação:",
                 style="Dark.TLabel").grid(row=3, column=0, padx=5)
        self.saturation_var = tk.DoubleVar(value=1.0)
        saturation_scale = ttk.Scale(adjustments_frame, from_=0.0, to=3.0,
                                   variable=self.saturation_var,
                                   command=self.update_image,
                                   style="Dark.Horizontal.TScale")
        saturation_scale.grid(row=3, column=1, sticky="ew", padx=5)
        
        ttk.Label(adjustments_frame, text="Nuance:",
                 style="Dark.TLabel").grid(row=4, column=0, padx=5)
        self.hue_var = tk.DoubleVar(value=0.0)
        hue_scale = ttk.Scale(adjustments_frame, from_=-180.0, to=180.0,
                            variable=self.hue_var,
                            command=self.update_image,
                            style="Dark.Horizontal.TScale")
        hue_scale.grid(row=4, column=1, sticky="ew", padx=5)

        # Valores atuais dos ajustes
        self.brightness_label = ttk.Label(adjustments_frame, text="0.0",
                                        style="Dark.TLabel")
        self.brightness_label.grid(row=0, column=2, padx=5)
        
        self.contrast_label = ttk.Label(adjustments_frame, text="1.0",
                                      style="Dark.TLabel")
        self.contrast_label.grid(row=1, column=2, padx=5)
        
        self.gamma_label = ttk.Label(adjustments_frame, text="1.0",
                                   style="Dark.TLabel")
        self.gamma_label.grid(row=2, column=2, padx=5)
        
        self.saturation_label = ttk.Label(adjustments_frame, text="1.0",
                                        style="Dark.TLabel")
        self.saturation_label.grid(row=3, column=2, padx=5)
        
        self.hue_label = ttk.Label(adjustments_frame, text="0.0",
                                 style="Dark.TLabel")
        self.hue_label.grid(row=4, column=2, padx=5)
        
        # Botão de Reset com estilo escuro
        ttk.Button(adjustments_frame,
                  text="Reset",
                  command=self.reset_adjustments,
                  style="Dark.TButton").grid(row=5, column=0, columnspan=3, pady=5)
        
        adjustments_frame.columnconfigure(1, weight=1)
        
        # Frame da imagem com loading
        self.image_frame = ttk.Frame(left_frame, style="Dark.TFrame")
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Label de loading
        self.loading_label = ttk.Label(self.image_frame, text="Carregando imagem...",
                                     style="Dark.TLabel")
        
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
                # Mostrar loading
                self.loading_label.pack(expand=True)
                self.update_idletasks()
                
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
            finally:
                # Esconder loading
                self.loading_label.pack_forget()
    
    def update_image(self, *args):
        """Atualiza a imagem com os ajustes atuais"""
        if self.original_cv_image is not None:
            try:
                # Mostrar loading
                self.loading_label.pack(expand=True)
                self.update_idletasks()
                
                # Aplicar ajustes
                img = self.original_cv_image.copy()
                
                # Ajuste de brilho e contraste
                brightness = self.brightness_var.get()
                contrast = self.contrast_var.get()
                
                # Atualizar labels com valores atuais
                self.brightness_label.config(text=f"{brightness:.1f}")
                self.contrast_label.config(text=f"{contrast:.1f}")
                self.gamma_label.config(text=f"{self.gamma_var.get():.1f}")
                self.saturation_label.config(text=f"{self.saturation_var.get():.1f}")
                self.hue_label.config(text=f"{self.hue_var.get():.1f}")
                
                # Converter para HSV para ajustes de cor
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
                
                # Ajuste de saturação
                saturation = self.saturation_var.get()
                hsv[:,:,1] = np.clip(hsv[:,:,1] * saturation, 0, 255)
                
                # Ajuste de nuance (hue)
                hue_shift = self.hue_var.get()
                hsv[:,:,0] = np.mod(hsv[:,:,0] + hue_shift, 180)  # Hue vai de 0 a 180 no OpenCV
                
                # Converter de volta para BGR
                img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
                
                # Ajuste de brilho e contraste
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
            finally:
                # Esconder loading
                self.loading_label.pack_forget()

    def reset_adjustments(self):
        """Reseta todos os ajustes para seus valores padrão"""
        self.brightness_var.set(0.0)  # Valor central para brilho
        self.contrast_var.set(1.0)    # Valor neutro para contraste
        self.gamma_var.set(1.0)       # Valor neutro para gamma
        self.saturation_var.set(1.0)  # Valor neutro para saturação
        self.hue_var.set(0.0)         # Valor neutro para nuance
        
        # Atualizar labels
        self.brightness_label.config(text="0.0")
        self.contrast_label.config(text="1.0")
        self.gamma_label.config(text="1.0")
        self.saturation_label.config(text="1.0")
        self.hue_label.config(text="0.0")
        
        if self.original_cv_image is not None:
            self.current_cv_image = self.original_cv_image.copy()
            self.display_current_image()
            
    def invert_colors(self):
        """Inverte as cores da imagem"""
        if self.current_cv_image is not None:
            try:
                # Mostrar loading
                self.loading_label.pack(expand=True)
                self.update_idletasks()
                
                # Inverter cores
                self.current_cv_image = cv2.bitwise_not(self.current_cv_image)
                self.display_current_image()
                
            except Exception as e:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Erro ao inverter cores: {str(e)}")
            finally:
                # Esconder loading
                self.loading_label.pack_forget()
                
    def rotate_image(self):
        """Rotaciona a imagem em 90 graus"""
        if self.current_cv_image is not None:
            try:
                # Mostrar loading
                self.loading_label.pack(expand=True)
                self.update_idletasks()
                
                # Rotacionar imagem
                self.current_cv_image = cv2.rotate(self.current_cv_image, cv2.ROTATE_90_CLOCKWISE)
                self.display_current_image()
                
            except Exception as e:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Erro ao rotacionar imagem: {str(e)}")
            finally:
                # Esconder loading
                self.loading_label.pack_forget()
    
    def display_current_image(self):
        """Exibe a imagem atual no frame"""
        if self.current_cv_image is not None:
            try:
                # Limpar frame anterior
                for widget in self.image_frame.winfo_children():
                    if widget != self.loading_label:  # Mantém o label de loading
                        widget.destroy()
                
                # Converter de BGR para RGB
                rgb_image = cv2.cvtColor(self.current_cv_image, cv2.COLOR_BGR2RGB)
                
                # Converter para PIL Image
                pil_image = Image.fromarray(rgb_image)
                
                # Redimensionar mantendo proporção
                display_size = (800, 600)
                pil_image.thumbnail(display_size, Image.Resampling.LANCZOS)
                
                # Converter para PhotoImage
                photo = ImageTk.PhotoImage(pil_image)
                
                # Criar label para exibir a imagem
                image_label = ttk.Label(self.image_frame, image=photo, style="Dark.TLabel")
                image_label.image = photo
                image_label.pack(expand=True)
                
            except Exception as e:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Erro ao exibir imagem: {str(e)}")

    def analyze_current_image(self):
        """Analisa a imagem atual"""
        if self.current_cv_image is not None:
            try:
                print("Iniciando análise da imagem atual para QR Codes...")  # Log de depuração
                # Mostrar loading
                self.loading_label.pack(expand=True)
                self.update_idletasks()
                
                # Limpar resultados anteriores
                self.result_text.delete(1.0, tk.END)
                
                # Preparar imagem para análise de QR
                img_for_qr = self.current_cv_image.copy()
                
                # Converter para escala de cinza
                gray = cv2.cvtColor(img_for_qr, cv2.COLOR_BGR2GRAY)
                
                # Tentar detectar QR codes
                qr = cv2.QRCodeDetector()
                retval, decoded_info, points, straight_qrcode = qr.detectAndDecodeMulti(gray)
                print(f"QRCodeDetector retorno: {retval}, Info: {decoded_info}")  # Log de depuração
                
                if not retval:  # Se não detectou, tentar com a imagem original
                    retval, decoded_info, points, straight_qrcode = qr.detectAndDecodeMulti(self.current_cv_image)
                    print(f"Tentativa com imagem original, retorno: {retval}, Info: {decoded_info}")  # Log de depuração
                
                if retval and any(decoded_info):  # QR Code encontrado
                    self.result_text.insert(tk.END, "QR Code(s) detectado(s):\n\n")
                    
                    for i, info in enumerate(decoded_info):
                        if info:  # Se há informação decodificada
                            self.result_text.insert(tk.END, f"QR Code {i+1}: {info}\n")
                            
                            # Desenhar contorno do QR code na imagem
                            if points is not None and len(points) > i:
                                pts = points[i].astype(int)
                                # Desenhar contorno em verde
                                cv2.polylines(self.current_cv_image, [pts], True, (0, 255, 0), 2)
                    
                    # Atualizar a exibição da imagem com os contornos
                    self.display_current_image()
                else:
                    # Tentar com ZBar como backup
                    try:
                        import pyzbar.pyzbar as pyzbar
                        decoded_objects = pyzbar.decode(gray)
                        print(f"Pyzbar detectou: {decoded_objects}")  # Log de depuração
                        
                        if decoded_objects:
                            self.result_text.insert(tk.END, "QR/Barcode(s) detectado(s):\n\n")
                            
                            for obj in decoded_objects:
                                # Decodificar dados
                                data = obj.data.decode('utf-8')
                                self.result_text.insert(tk.END, f"Tipo: {obj.type}\nDados: {data}\n\n")
                                
                                # Desenhar contorno
                                points = obj.polygon
                                if points:
                                    pts = np.array(points, np.int32)
                                    pts = pts.reshape((-1, 1, 2))
                                    cv2.polylines(self.current_cv_image, [pts], True, (0, 255, 0), 2)
                            
                            # Atualizar a exibição da imagem com os contornos
                            self.display_current_image()
                        else:
                            self.result_text.insert(tk.END, "Falha ao detectar QR-Codes. Tente usar seu dispositivo móvel para escanear o código.\n")
                            # Análise adicional de padrões
                            patterns = self.decoder.detect_patterns(self.current_cv_image)
                            if patterns:
                                self.result_text.insert(tk.END, f"Padrões detectados: {patterns}\n")
                            else:
                                self.result_text.insert(tk.END, "Nenhum padrão significativo detectado\n")
                    except ImportError:
                        self.result_text.insert(tk.END, "Falha ao detectar QR-Codes. Tente usar seu dispositivo móvel para escanear o código.\n")
                        # Análise adicional de padrões
                        patterns = self.decoder.detect_patterns(self.current_cv_image)
                        if patterns:
                            self.result_text.insert(tk.END, f"Padrões detectados: {patterns}\n")
                        else:
                            self.result_text.insert(tk.END, "Nenhum padrão significativo detectado\n")
                
                # Análise adicional da imagem
                self.analyze_image_properties()
                
            except Exception as e:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Erro na análise: {str(e)}")
            finally:
                # Esconder loading
                self.loading_label.pack_forget()
    
    def analyze_image_properties(self):
        """Analisa propriedades adicionais da imagem"""
        try:
            # Análise de cores dominantes
            img = cv2.cvtColor(self.current_cv_image, cv2.COLOR_BGR2RGB)
            pixels = img.reshape(-1, 3)
            pixels = np.float32(pixels)
            
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            K = 3  # Número de cores dominantes
            _, labels, centers = cv2.kmeans(pixels, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            # Converter cores para hexadecimal
            self.result_text.insert(tk.END, "\nCores dominantes (hex):\n")
            for center in centers:
                color_hex = '#{:02x}{:02x}{:02x}'.format(int(center[0]), int(center[1]), int(center[2]))
                self.result_text.insert(tk.END, f"{color_hex}\n")
            
            # Análise de brilho médio
            gray = cv2.cvtColor(self.current_cv_image, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            self.result_text.insert(tk.END, f"\nBrilho médio: {brightness:.1f}\n")
            
            # Análise de contraste
            contrast = np.std(gray)
            self.result_text.insert(tk.END, f"Contraste: {contrast:.1f}\n")
            
            # Dimensões da imagem
            height, width = self.current_cv_image.shape[:2]
            self.result_text.insert(tk.END, f"\nDimensões: {width}x{height} pixels\n")
            
        except Exception as e:
            self.result_text.insert(tk.END, f"\nErro na análise de propriedades: {str(e)}\n")

    def load_test_image(self):
        """Carrega a imagem de teste predefinida"""
        test_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'images', 'IMAGEM TESTE.jpg'))
        print(f"Tentando carregar a imagem de teste a partir de: {test_image_path}")  # Log de depuração
        if os.path.exists(test_image_path):
            try:
                # Mostrar loading
                self.loading_label.pack(expand=True)
                self.update_idletasks()

                # Carregar imagem com OpenCV
                self.original_cv_image = cv2.imread(test_image_path)
                if self.original_cv_image is None:
                    print("OpenCV não conseguiu carregar a imagem com imread.")  # Log de depuração
                    # Tentar carregar com imdecode se imread falhar
                    img_array = np.fromfile(test_image_path, dtype=np.uint8)
                    self.original_cv_image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    if self.original_cv_image is None:
                        raise ValueError("Não foi possível carregar a imagem")

                self.current_cv_image = self.original_cv_image.copy()
                self.display_current_image()
                self.analyze_current_image()  # Certificar-se de que o QR-Code seja analisado

            except Exception as e:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Erro ao carregar imagem de teste: {str(e)}")
            finally:
                # Esconder loading
                self.loading_label.pack_forget()
        else:
            print("Imagem de teste não encontrada.")
