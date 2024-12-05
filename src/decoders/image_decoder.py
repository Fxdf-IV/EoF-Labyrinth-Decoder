"""
Decodificador de imagens com suporte a múltiplos formatos e análises
"""

import cv2
import numpy as np
from PIL import Image
import logging
from typing import Dict, Any, Union
import io
import os
from pathlib import Path

class ImageDecoder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_image(self, image: Union[str, Image.Image, np.ndarray]) -> Dict[str, Any]:
        """
        Analisa uma imagem usando vários métodos
        """
        try:
            # Se for um objeto PIL.Image, converter para formato OpenCV
            if isinstance(image, Image.Image):
                img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            # Se for um array numpy (OpenCV)
            elif isinstance(image, np.ndarray):
                img_cv = image.copy()
            # Se for um caminho de arquivo
            else:
                # Carregar imagem com OpenCV
                img_cv = cv2.imread(str(image))
                if img_cv is None:
                    # Tentar carregar com imdecode se imread falhar
                    img_array = np.fromfile(str(image), dtype=np.uint8)
                    img_cv = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    if img_cv is None:
                        raise ValueError("Não foi possível carregar a imagem")

            results = {}
            
            # Análise de dimensões
            results["Dimensões"] = f"{img_cv.shape[1]}x{img_cv.shape[0]} pixels"
            
            # Análise de cores dominantes
            colors = self.analyze_colors(img_cv)
            results["Cores Dominantes"] = colors
            
            # Detecção de padrões
            patterns = self.detect_patterns(img_cv)
            if patterns:
                results["Padrões Detectados"] = patterns
            
            # Análise de texto
            text = self.detect_text(img_cv)
            if text:
                results["Texto Detectado"] = text
            
            # Análise de QR Code
            qr = self.detect_qr_code(img_cv)
            if qr:
                results["QR Code"] = qr
                
            # Análise de padrões ocultos
            hidden = self.detect_hidden_patterns(img_cv)
            if hidden:
                results["Padrões Ocultos"] = hidden
            
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
        Detecta padrões na imagem com parâmetros ajustados para maior precisão
        """
        try:
            patterns = []
            
            # Converter para escala de cinza
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detectar bordas com parâmetros ajustados
            edges = cv2.Canny(gray, 100, 200)
            
            # Detectar linhas com parâmetros ajustados
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 80, 
                                  minLineLength=50, maxLineGap=5)
            if lines is not None and len(lines) > 0:
                patterns.append(f"{len(lines)} linhas")
            
            # Detectar círculos com parâmetros ajustados
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                                     param1=100, param2=30, 
                                     minRadius=5, maxRadius=100)
            if circles is not None:
                patterns.append(f"{len(circles[0])} círculos")
            
            # Detectar contornos com filtragem adicional
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, 
                                         cv2.CHAIN_APPROX_SIMPLE)
            # Filtrar contornos pequenos
            contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 50]
            if len(contours) > 0:
                patterns.append(f"{len(contours)} contornos")
            
            return ", ".join(patterns) if patterns else "Nenhum padrão significativo detectado"
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de padrões: {str(e)}")
            return "Erro na detecção de padrões"

    def detect_qr_code(self, img: np.ndarray) -> str:
        """
        Detecta QR Code na imagem usando OpenCV com pré-processamento agressivo
        """
        try:
            print("Iniciando detecção de QR Code...")  # Log de depuração
            # Converter para escala de cinza
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Criar detector
            qr_detector = cv2.QRCodeDetector()
            
            # Lista de pré-processamentos
            processed_images = []
            
            # 1. Imagem original em escala de cinza
            processed_images.append(gray)
            
            # 2. Aumentar contraste
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            contrast = clahe.apply(gray)
            processed_images.append(contrast)
            
            # 3. Binarização agressiva
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            processed_images.append(binary)
            
            # 4. Binarização adaptativa
            adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY, 11, 2)
            processed_images.append(adaptive)
            
            # 5. Desfoque + Binarização
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, blur_binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            processed_images.append(blur_binary)
            
            # 6. Dilatação para conectar componentes
            kernel = np.ones((3,3), np.uint8)
            dilated = cv2.dilate(binary, kernel, iterations=1)
            processed_images.append(dilated)
            
            # Tentar detectar em cada versão
            for processed in processed_images:
                # Tentar diferentes escalas
                scales = [1.0, 1.5, 2.0, 0.75]
                for scale in scales:
                    # Redimensionar
                    width = int(processed.shape[1] * scale)
                    height = int(processed.shape[0] * scale)
                    resized = cv2.resize(processed, (width, height), interpolation=cv2.INTER_CUBIC)
                    
                    # Tentar detectar
                    retval, decoded_info, points = qr_detector.detectAndDecode(resized)
                    if retval and decoded_info:
                        print(f"QR Code detectado: {decoded_info}")  # Log de depuração
                        return decoded_info
                    
                    # Tentar com detectAndDecodeMulti
                    retval, decoded_info, points, _ = qr_detector.detectAndDecodeMulti(resized)
                    if retval and decoded_info:
                        if isinstance(decoded_info, str):
                            print(f"QR Code detectado (multi): {decoded_info}")  # Log de depuração
                            return decoded_info
                        elif isinstance(decoded_info, list) and any(decoded_info):
                            print(f"QR Codes detectados (multi): {decoded_info}")  # Log de depuração
                            return next(d for d in decoded_info if d)
            
            # Se não encontrou, tentar uma última abordagem com detecção de contornos
            for processed in processed_images:
                # Encontrar contornos
                contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # Filtrar contornos quadrados
                for contour in contours:
                    # Calcular área e perímetro
                    area = cv2.contourArea(contour)
                    peri = cv2.arcLength(contour, True)
                    
                    # Se o contorno for muito pequeno, ignorar
                    if area < 10:
                        continue
                        
                    # Aproximar o contorno
                    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
                    
                    # Verificar se é aproximadamente um quadrado
                    if len(approx) == 4:
                        # Calcular a razão entre largura e altura
                        x, y, w, h = cv2.boundingRect(contour)
                        aspect_ratio = float(w)/h
                        
                        # Se for aproximadamente quadrado
                        if 0.8 < aspect_ratio < 1.2 and area < 200:
                            # Extrair região
                            qr_region = processed[y:y+h, x:x+w]
                            
                            # Redimensionar região
                            qr_region = cv2.resize(qr_region, (0,0), fx=2, fy=2)
                            
                            # Tentar decodificar
                            retval, decoded_info, _ = qr_detector.detectAndDecode(qr_region)
                            if retval and decoded_info:
                                print(f"QR Code detectado na região: {decoded_info}")  # Log de depuração
                                return decoded_info
            
            print("Nenhum QR Code detectado após todas as tentativas.")  # Log de depuração
            return "Falha ao detectar QR-Codes. Tente usar seu dispositivo móvel para escanear o código."
        except Exception as e:
            self.logger.error(f"Erro na detecção de QR Code: {str(e)}")
            return "Falha ao detectar QR-Codes. Tente usar seu dispositivo móvel para escanear o código."

    def detect_text(self, img: np.ndarray) -> str:
        """
        Detecta texto na imagem usando técnicas avançadas de processamento
        """
        try:
            # Converter para escala de cinza
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Aplicar blur para reduzir ruído
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Binarização com Otsu's method
            _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Operações morfológicas para melhorar a detecção
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filtrar e analisar regiões de texto
            text_regions = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                # Ajustar parâmetros para capturar mais regiões de texto
                if 5 < w < 300 and 5 < h < 300:
                    aspect_ratio = float(w)/h
                    if 0.1 < aspect_ratio < 15:
                        area = cv2.contourArea(cnt)
                        if area > 50:  # Filtrar áreas muito pequenas
                            text_regions.append((x, y, w, h))
            
            if text_regions:
                # Agrupar regiões próximas
                merged_regions = self.merge_nearby_regions(text_regions)
                return f"Detectadas {len(merged_regions)} regiões com possível texto"
            else:
                return "Nenhum texto detectado"
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de texto: {str(e)}")
            return "Erro na detecção de texto"

    def merge_nearby_regions(self, regions, distance_threshold=20):
        """
        Agrupa regiões de texto que estão próximas
        """
        if not regions:
            return []
            
        merged = []
        current_group = [regions[0]]
        
        for i in range(1, len(regions)):
            current_x, current_y, current_w, current_h = regions[i]
            prev_x, prev_y, prev_w, prev_h = current_group[-1]
            
            # Calcular distância entre regiões
            distance = min(
                abs(current_x - (prev_x + prev_w)),  # Distância horizontal
                abs(current_y - (prev_y + prev_h))   # Distância vertical
            )
            
            if distance <= distance_threshold:
                current_group.append(regions[i])
            else:
                merged.append(self.merge_region_group(current_group))
                current_group = [regions[i]]
        
        if current_group:
            merged.append(self.merge_region_group(current_group))
        
        return merged

    def merge_region_group(self, group):
        """
        Combina um grupo de regiões em uma única região
        """
        if not group:
            return None
            
        x_min = min(r[0] for r in group)
        y_min = min(r[1] for r in group)
        x_max = max(r[0] + r[2] for r in group)
        y_max = max(r[1] + r[3] for r in group)
        
        return (x_min, y_min, x_max - x_min, y_max - y_min)

    def detect_hidden_patterns(self, img: np.ndarray) -> str:
        """
        Detecta padrões ocultos ajustando brilho e contraste, com foco especial em padrões pequenos
        """
        try:
            # Converter para escala de cinza
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Lista de resultados encontrados
            findings = []
            
            # 1. Diminuir muito o brilho para revelar padrões escondidos
            darkened = cv2.convertScaleAbs(gray, alpha=1.5, beta=-100)
            
            # Aplicar threshold adaptativo no escuro
            dark_thresh = cv2.adaptiveThreshold(
                darkened,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2
            )
            
            # Encontrar contornos na imagem escura
            dark_contours, _ = cv2.findContours(
                dark_thresh,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            
            # Filtrar contornos pequenos e quadrados
            small_squares = []
            for contour in dark_contours:
                # Calcular área e perímetro
                area = cv2.contourArea(contour)
                peri = cv2.arcLength(contour, True)
                
                # Se o contorno for muito pequeno, ignorar
                if area < 10:
                    continue
                    
                # Aproximar o contorno
                approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
                
                # Verificar se é aproximadamente um quadrado
                if len(approx) == 4:
                    # Calcular a razão entre largura e altura
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = float(w)/h
                    
                    # Se for aproximadamente quadrado
                    if 0.8 < aspect_ratio < 1.2 and area < 200:
                        small_squares.append(contour)
            
            # Se encontrar vários quadrados pequenos
            if len(small_squares) > 5:
                findings.append("Padrões quadrados encontrados com baixa luminosidade")
                
                # Verificar se os quadrados estão próximos uns dos outros
                centers = []
                for square in small_squares:
                    M = cv2.moments(square)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        centers.append((cx, cy))
                
                # Se houver centros suficientes, verificar proximidade
                if len(centers) > 5:
                    # Ordenar centros por coordenada x
                    centers.sort(key=lambda p: p[0])
                    
                    # Verificar se há grupos próximos
                    groups = []
                    current_group = [centers[0]]
                    
                    for i in range(1, len(centers)):
                        prev_x, prev_y = centers[i-1]
                        curr_x, curr_y = centers[i]
                        
                        # Se os centros estão próximos
                        if abs(curr_x - prev_x) < 30 and abs(curr_y - prev_y) < 30:
                            current_group.append(centers[i])
                        else:
                            if len(current_group) > 2:
                                groups.append(current_group)
                            current_group = [centers[i]]
                    
                    if groups:
                        findings.append("Padrões quadrados agrupados detectados")
            
            if findings:
                return " | ".join(findings)
            return None
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de padrões ocultos: {str(e)}")
            return None
