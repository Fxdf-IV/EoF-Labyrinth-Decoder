"""
Módulo para decodificação de texto em vários formatos
"""

import base64
import binascii
import logging
from typing import Optional

class TextDecoder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Tabela Morse
        self.morse_code = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
            '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
            '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
            '--..': 'Z', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
            '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
            '-----': '0', '.-.-.-': '.', '--..--': ',', '..--..': '?',
            '.----.': "'", '-.-.--': '!', '-..-.': '/', '-.--.': '(',
            '-.--.-': ')', '.-...': '&', '---...': ':', '-.-.-.': ';',
            '-...-': '=', '.-.-.': '+', '-....-': '-', '..--.-': '_',
            '.-..-.': '"', '...-..-': '$', '.--.-.': '@', '...---...': 'SOS'
        }

    def decode_base64(self, text: str) -> Optional[str]:
        """Decodifica texto em Base64"""
        try:
            decoded = base64.b64decode(text).decode('utf-8')
            return decoded
        except Exception as e:
            self.logger.error(f"Erro ao decodificar Base64: {str(e)}")
            return None

    def decode_hex(self, text: str) -> Optional[str]:
        """Decodifica texto em hexadecimal"""
        try:
            # Remove espaços e '0x' se presentes
            text = text.replace(' ', '').replace('0x', '')
            decoded = bytes.fromhex(text).decode('utf-8')
            return decoded
        except Exception as e:
            self.logger.error(f"Erro ao decodificar Hex: {str(e)}")
            return None

    def decode_binary(self, text: str) -> Optional[str]:
        """Decodifica texto em binário"""
        try:
            # Remove espaços
            text = text.replace(' ', '')
            
            # Verifica se é uma string binária válida
            if not all(bit in '01' for bit in text):
                raise ValueError("Texto contém caracteres não binários")
            
            # Garante que o comprimento é múltiplo de 8
            if len(text) % 8 != 0:
                raise ValueError("Comprimento do texto binário deve ser múltiplo de 8")
            
            # Converte para bytes e depois para string
            bytes_data = int(text, 2).to_bytes(len(text) // 8, byteorder='big')
            return bytes_data.decode('utf-8')
        except Exception as e:
            self.logger.error(f"Erro ao decodificar Binário: {str(e)}")
            return None

    def decode_morse(self, text: str) -> Optional[str]:
        """Decodifica código Morse"""
        try:
            # Remove espaços extras e divide em palavras
            words = text.strip().split('   ')
            decoded_words = []
            
            for word in words:
                # Divide a palavra em letras
                letters = word.strip().split(' ')
                decoded_letters = []
                
                for letter in letters:
                    if letter in self.morse_code:
                        decoded_letters.append(self.morse_code[letter])
                    else:
                        self.logger.warning(f"Símbolo Morse desconhecido: {letter}")
                
                if decoded_letters:
                    decoded_words.append(''.join(decoded_letters))
            
            return ' '.join(decoded_words)
        except Exception as e:
            self.logger.error(f"Erro ao decodificar Morse: {str(e)}")
            return None

    def caesar_cipher(self, text: str, shift: int = -3) -> str:
        """Decodifica cifra de César"""
        try:
            result = ""
            for char in text:
                if char.isalpha():
                    # Determina o caso (maiúsculo/minúsculo)
                    ascii_offset = ord('A') if char.isupper() else ord('a')
                    # Aplica a cifra de César
                    result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
                else:
                    result += char
            return result
        except Exception as e:
            self.logger.error(f"Erro ao decodificar Cifra de César: {str(e)}")
            return None

    def atbash_cipher(self, text: str) -> str:
        """Decodifica cifra Atbash"""
        try:
            result = ""
            for char in text:
                if char.isalpha():
                    # Determina o caso (maiúsculo/minúsculo)
                    if char.isupper():
                        result += chr(ord('Z') - (ord(char) - ord('A')))
                    else:
                        result += chr(ord('z') - (ord(char) - ord('a')))
                else:
                    result += char
            return result
        except Exception as e:
            self.logger.error(f"Erro ao decodificar Cifra Atbash: {str(e)}")
            return None
