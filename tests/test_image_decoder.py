import unittest
import os
import numpy as np
from PIL import Image
from src.decoders.image_decoder import ImageDecoder

class TestImageDecoder(unittest.TestCase):
    def setUp(self):
        self.decoder = ImageDecoder()
        self.test_dir = "test_images"
        
        # Criar diretório para imagens de teste
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
            
        # Criar imagem de teste com padrão de pontos
        self.dot_pattern = Image.new('RGB', (100, 100), color='white')
        pixels = self.dot_pattern.load()
        for i in range(0, 100, 10):
            for j in range(0, 100, 10):
                pixels[i,j] = (0, 0, 0)  # Pontos pretos
        self.dot_pattern.save(os.path.join(self.test_dir, "dot_pattern.png"))
        
        # Criar imagem com texto para OCR
        self.text_image = Image.new('RGB', (200, 50), color='white')
        pixels = self.text_image.load()
        # Simular texto "TEST" em pixels pretos
        self.text_image.save(os.path.join(self.test_dir, "text.png"))
        
    def tearDown(self):
        # Limpar arquivos de teste
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)
    
    def test_dot_pattern_detection(self):
        """Testa detecção de padrões de pontos"""
        image_path = os.path.join(self.test_dir, "dot_pattern.png")
        patterns = self.decoder.detect_dot_patterns(image_path)
        
        self.assertGreater(len(patterns), 0)
        
    def test_qr_code_detection(self):
        """Testa detecção de QR codes"""
        # Criar imagem com QR code
        qr_path = os.path.join(self.test_dir, "qr.png")
        self.decoder.generate_qr_code("Test QR Code", qr_path)
        
        result = self.decoder.detect_qr_code(qr_path)
        self.assertEqual(result, "Test QR Code")
        
    def test_ocr_text_detection(self):
        """Testa extração de texto via OCR"""
        image_path = os.path.join(self.test_dir, "text.png")
        text = self.decoder.extract_text(image_path)
        
        self.assertIsInstance(text, str)
        
    def test_color_analysis(self):
        """Testa análise de cores hexadecimais"""
        # Criar imagem com cores específicas
        color_image = Image.new('RGB', (100, 100), color='#FF0000')
        color_path = os.path.join(self.test_dir, "color.png")
        color_image.save(color_path)
        
        colors = self.decoder.analyze_colors(color_path)
        self.assertIn('#FF0000', colors)
        
    def test_morse_pattern_detection(self):
        """Testa detecção de padrões Morse visuais"""
        # Criar imagem com padrão Morse
        morse_image = Image.new('RGB', (300, 50), color='white')
        pixels = morse_image.load()
        # Simular "SOS" em Morse (... --- ...)
        morse_path = os.path.join(self.test_dir, "morse.png")
        morse_image.save(morse_path)
        
        morse_code = self.decoder.detect_morse_pattern(morse_path)
        self.assertIsInstance(morse_code, str)
        
    def test_binary_pattern_detection(self):
        """Testa detecção de padrões binários"""
        # Criar imagem com padrão binário
        binary_image = Image.new('RGB', (80, 10), color='white')
        pixels = binary_image.load()
        # Simular padrão binário "01010101"
        for i in range(0, 80, 10):
            if (i//10) % 2 == 0:
                for y in range(10):
                    pixels[i,y] = (0, 0, 0)
        binary_path = os.path.join(self.test_dir, "binary.png")
        binary_image.save(binary_path)
        
        binary = self.decoder.detect_binary_pattern(binary_path)
        self.assertIsInstance(binary, str)
        self.assertTrue(all(c in '01' for c in binary))

if __name__ == '__main__':
    unittest.main()
