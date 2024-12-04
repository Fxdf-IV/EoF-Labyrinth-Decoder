import unittest
import numpy as np
import os
import tempfile
from src.decoders.text_decoder import TextDecoder
from src.decoders.image_decoder import ImageDecoder
from src.decoders.audio_decoder import AudioDecoder
from src.decoders.labyrinth_decoder import LabyrinthDecoder

class TestTextDecoder(unittest.TestCase):
    def setUp(self):
        self.decoder = TextDecoder()
    
    def test_base64_detection(self):
        text = "SGVsbG8gV29ybGQ="  # "Hello World" em Base64
        encodings = self.decoder.detect_encoding(text)
        self.assertIn('base64', encodings)
    
    def test_base64_decoding(self):
        text = "SGVsbG8gV29ybGQ="
        result = self.decoder.decode_base64(text)
        self.assertEqual(result, "Hello World")
    
    def test_morse_detection(self):
        text = "... --- ..."  # "SOS" em Morse
        encodings = self.decoder.detect_encoding(text)
        self.assertIn('morse', encodings)
    
    def test_morse_decoding(self):
        text = "... --- ..."
        result = self.decoder.decode_morse(text)
        self.assertEqual(result.strip(), "SOS")
    
    def test_caesar_cipher(self):
        text = "KHOOR"  # "HELLO" com shift 3
        result = self.decoder.caesar_cipher(text, 3)
        self.assertEqual(result, "HELLO")
    
    def test_atbash_cipher(self):
        text = "SVOOL"  # "HELLO" em Atbash
        result = self.decoder.atbash_cipher(text)
        self.assertEqual(result, "HELLO")
    
    def test_vigenere_cipher(self):
        text = "RIJVS"  # "HELLO" com chave "KEY"
        result = self.decoder.vigenere_cipher(text, "KEY")
        self.assertEqual(result, "HELLO")

class TestImageDecoder(unittest.TestCase):
    def setUp(self):
        self.decoder = ImageDecoder()
        # Criar uma imagem de teste
        self.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        # Adicionar alguns padrões para teste
        self.test_image[40:60, 40:60] = 255  # Quadrado branco
    
    def test_load_image(self):
        # Salvar imagem temporária
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            import cv2
            cv2.imwrite(tmp.name, self.test_image)
            
            # Testar carregamento
            loaded = self.decoder.load_image(tmp.name)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.shape, self.test_image.shape)
            
            # Limpar
            os.unlink(tmp.name)
    
    def test_enhance_image(self):
        enhanced = self.decoder.enhance_image(self.test_image)
        self.assertIn('gray', enhanced)
        self.assertIn('binary', enhanced)
        self.assertIn('edges', enhanced)
    
    def test_detect_patterns(self):
        patterns = self.decoder.detect_patterns(self.test_image)
        self.assertIn('symbols', patterns)
        self.assertIn('colors', patterns)

class TestAudioDecoder(unittest.TestCase):
    def setUp(self):
        self.decoder = AudioDecoder()
        # Criar um sinal de teste
        duration = 1.0
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        self.test_audio = np.sin(2 * np.pi * 440 * t)  # Tom A4 (440 Hz)
    
    def test_load_audio(self):
        # Salvar áudio temporário
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            import soundfile as sf
            sf.write(tmp.name, self.test_audio, 44100)
            
            # Testar carregamento
            loaded, sr = self.decoder.load_audio(tmp.name)
            self.assertIsNotNone(loaded)
            self.assertEqual(len(loaded), len(self.test_audio))
            
            # Limpar
            os.unlink(tmp.name)
    
    def test_detect_morse_code(self):
        # Criar um sinal Morse simples (SOS)
        duration = 3.0
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        morse_signal = np.zeros_like(t)
        
        # Adicionar pulsos para "... --- ..."
        for i in range(3):  # Três pontos
            start = i * 0.2
            morse_signal[int(start * sample_rate):int((start + 0.1) * sample_rate)] = 1
        
        morse = self.decoder.detect_morse_code(morse_signal, sample_rate)
        self.assertIsNotNone(morse)
        self.assertIn('.', morse)
    
    def test_analyze_audio_structure(self):
        analysis = self.decoder.analyze_audio_structure(self.test_audio, 44100)
        self.assertIn('duration', analysis)
        self.assertIn('sample_rate', analysis)
        self.assertIn('segments', analysis)

class TestLabyrinthDecoder(unittest.TestCase):
    def setUp(self):
        self.decoder = LabyrinthDecoder()
        # Criar um labirinto de teste
        self.test_labyrinth = [
            ["#", "#", "#", "#", "#"],
            ["#", "S", " ", "E", "#"],
            ["#", "#", "#", "#", "#"]
        ]
    
    def test_find_path(self):
        path = self.decoder.find_path(self.test_labyrinth)
        self.assertIsNotNone(path)
        self.assertTrue(len(path) > 0)
    
    def test_validate_path(self):
        path = [(1, 1), (1, 2), (1, 3)]  # S -> E
        valid = self.decoder.validate_path(self.test_labyrinth, path)
        self.assertTrue(valid)

if __name__ == '__main__':
    unittest.main()
