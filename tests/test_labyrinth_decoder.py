import unittest
import os
from src.decoders.labyrinth_decoder import LabyrinthDecoder

class TestLabyrinthDecoder(unittest.TestCase):
    def setUp(self):
        self.decoder = LabyrinthDecoder()
    
    def test_valid_keywords(self):
        """Testa se as palavras-chave são reconhecidas corretamente"""
        self.assertTrue(self.decoder.is_valid_keyword("Krev"))
        self.assertTrue(self.decoder.is_valid_keyword("Smrt"))
        self.assertFalse(self.decoder.is_valid_keyword("Invalid"))

if __name__ == '__main__':
    unittest.main()
