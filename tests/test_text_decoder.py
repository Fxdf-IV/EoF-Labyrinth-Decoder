import unittest
from src.decoders.text_decoder import TextDecoder

class TestTextDecoder(unittest.TestCase):
    def setUp(self):
        self.decoder = TextDecoder()
        
    def test_morse_decode(self):
        """Testa decodificação de código Morse"""
        morse_text = "... --- ..."  # SOS
        result = self.decoder.decode_morse(morse_text)
        self.assertEqual(result, "SOS")
        
        morse_text = ".... . .-.. .-.. ---"  # HELLO
        result = self.decoder.decode_morse(morse_text)
        self.assertEqual(result, "HELLO")
        
    def test_bacon_decode(self):
        """Testa decodificação da cifra de Bacon"""
        bacon_text = "AABAA AABBA"  # HI
        result = self.decoder.decode_bacon(bacon_text)
        self.assertEqual(result, "HI")
        
    def test_vigenere_decode(self):
        """Testa decodificação da cifra de Vigenère"""
        encrypted = "LXFOPVEFRNHR"  # HELLO WORLD com chave "KEY"
        key = "KEY"
        result = self.decoder.decode_vigenere(encrypted, key)
        self.assertEqual(result, "HELLOWORLD")
        
    def test_tap_code_decode(self):
        """Testa decodificação de Tap Code"""
        tap_text = ".... .. ... ... ... ..."  # SOS
        result = self.decoder.decode_tap(tap_text)
        self.assertEqual(result, "SOS")
        
    def test_braille_decode(self):
        """Testa decodificação de Braille"""
        braille_text = "⠓⠑⠇⠇⠕"  # HELLO
        result = self.decoder.decode_braille(braille_text)
        self.assertEqual(result, "HELLO")
        
    def test_auto_detection(self):
        """Testa auto-detecção do formato de codificação"""
        # Morse
        text = "... --- ..."
        format_type = self.decoder.detect_format(text)
        self.assertEqual(format_type, "morse")
        
        # Bacon
        text = "AABAA BABAA AABBA"
        format_type = self.decoder.detect_format(text)
        self.assertEqual(format_type, "bacon")
        
        # Tap Code
        text = ".... .. ... ... ... .."
        format_type = self.decoder.detect_format(text)
        self.assertEqual(format_type, "tap")
        
        # Braille
        text = "⠓⠑⠇⠇⠕"
        format_type = self.decoder.detect_format(text)
        self.assertEqual(format_type, "braille")
        
    def test_invalid_input(self):
        """Testa tratamento de entradas inválidas"""
        # Morse inválido
        with self.assertRaises(ValueError):
            self.decoder.decode_morse("... --- ...")
            
        # Bacon inválido
        with self.assertRaises(ValueError):
            self.decoder.decode_bacon("AABCC")
            
        # Vigenère inválido
        with self.assertRaises(ValueError):
            self.decoder.decode_vigenere("ABC", "")
            
        # Tap Code inválido
        with self.assertRaises(ValueError):
            self.decoder.decode_tap("...")
            
        # Braille inválido
        with self.assertRaises(ValueError):
            self.decoder.decode_braille("...")
            
    def test_special_characters(self):
        """Testa tratamento de caracteres especiais"""
        # Morse com caracteres especiais
        morse_text = "... --- ... -.-.--"  # SOS!
        result = self.decoder.decode_morse(morse_text)
        self.assertEqual(result, "SOS!")
        
        # Vigenère com espaços
        encrypted = "LXFOP VEFRNHR"  # "HELLO WORLD" com chave "KEY"
        key = "KEY"
        result = self.decoder.decode_vigenere(encrypted, key)
        self.assertEqual(result, "HELLO WORLD")

if __name__ == '__main__':
    unittest.main()
