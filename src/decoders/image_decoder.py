"""
Decodificador de imagens com suporte a múltiplos formatos e análises
"""

import cv2
import numpy as np
from PIL import Image
import logging
from typing import Dict, Any

class ImageDecoder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analisa uma imagem usando vários métodos
        """
        try:
            # Carregar imagem com OpenCV
            img_cv = cv2.imread(image_path)
            if img_cv is None:
                raise ValueError("Não foi possível carregar a imagem")
            
            # Carregar imagem com PIL para algumas análises
            img_pil = Image.open(image_path)
            
            results = {}
            
            # Análise de dimensões
            results["Dimensões"] = f"{img_cv.shape[1]}x{img_cv.shape[0]} pixels"
            
            # Análise de cores dominantes
            colors = self.analyze_colors(img_cv)
            results["Cores Dominantes"] = colors
            
            # Detecção de padrões
            patterns = self.detect_patterns(img_cv)
            results["Padrões Detectados"] = patterns
            
            # Análise de texto
            text = self.detect_text(img_cv)
            if text:
                results["Texto Detectado"] = text
            
            return results
            
        except Exception as e:
            self.logger.error(f"Erro ao analisar imagem: {str(e)}")
            raise

    def analyze_colors(self, img: np.ndarray) -> str:
        """
        Analisa as cores dominantes na imagem
        """
        try:
            # Converter para RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Redimensionar para acelerar o processamento
            height, width = img_rgb.shape[:2]
            if height * width > 1000000:  # Se maior que 1MP
                scale = np.sqrt(1000000 / (height * width))
                new_size = (int(width * scale), int(height * scale))
                img_rgb = cv2.resize(img_rgb, new_size)
            
            # Reshape para lista de pixels
            pixels = img_rgb.reshape(-1, 3)
            
            # Encontrar cores únicas e suas contagens
            colors, counts = np.unique(pixels, axis=0, return_counts=True)
            
            # Pegar as 5 cores mais frequentes
            top_indices = counts.argsort()[-5:][::-1]
            
            result = []
            for idx in top_indices:
                r, g, b = colors[idx]
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                percentage = (counts[idx] / len(pixels)) * 100
                result.append(f"{hex_color} ({percentage:.1f}%)")
            
            return ", ".join(result)
            
        except Exception as e:
            self.logger.error(f"Erro na análise de cores: {str(e)}")
            return "Erro na análise de cores"

    def detect_patterns(self, img: np.ndarray) -> str:
        """
        Detecta padrões na imagem
        """
        try:
            patterns = []
            
            # Converter para escala de cinza
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detectar bordas
            edges = cv2.Canny(gray, 50, 150)
            
            # Detectar linhas
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, 
                                  minLineLength=100, maxLineGap=10)
            if lines is not None and len(lines) > 0:
                patterns.append(f"{len(lines)} linhas")
            
            # Detectar círculos
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                                     param1=50, param2=30, 
                                     minRadius=0, maxRadius=0)
            if circles is not None:
                patterns.append(f"{len(circles[0])} círculos")
            
            # Detectar contornos
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, 
                                         cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                patterns.append(f"{len(contours)} contornos")
            
            return ", ".join(patterns) if patterns else "Nenhum padrão significativo detectado"
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de padrões: {str(e)}")
            return "Erro na detecção de padrões"

    def detect_text(self, img: np.ndarray) -> str:
        """
        Detecta texto na imagem usando técnicas básicas de OCR
        """
        try:
            # Converter para escala de cinza
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Binarização adaptativa
            binary = cv2.adaptiveThreshold(gray, 255, 
                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 11, 2)
            
            # Encontrar contornos que podem ser texto
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_SIMPLE)
            
            # Filtrar contornos que podem ser caracteres
            text_regions = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if 10 < w < 100 and 10 < h < 100:  # Tamanho típico de caracteres
                    aspect_ratio = float(w)/h
                    if 0.25 < aspect_ratio < 3:  # Proporção típica de caracteres
                        text_regions.append((x, y, w, h))
            
            if text_regions:
                return f"Detectadas {len(text_regions)} possíveis regiões de texto"
            else:
                return "Nenhum texto detectado"
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de texto: {str(e)}")
            return "Erro na detecção de texto"
