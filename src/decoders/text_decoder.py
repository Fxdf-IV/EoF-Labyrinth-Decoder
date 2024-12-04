"""
Módulo para decodificação de texto em vários formatos
"""

import base64
import binascii
import logging
from typing import Optional
import codecs

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
        
        # Dicionário de tradução Braille
        self.braille_dict = {
            '⠨⠨': '[MAIÚSCULO]',  # Indicador de maiúsculo
            '⠁': 'a', '⠃': 'b', '⠉': 'c', '⠙': 'd', '⠑': 'e',
            '⠋': 'f', '⠛': 'g', '⠓': 'h', '⠊': 'i', '⠚': 'j',
            '⠅': 'k', '⠇': 'l', '⠍': 'm', '⠝': 'n', '⠕': 'o',
            '⠏': 'p', '⠟': 'q', '⠗': 'r', '⠎': 's', '⠞': 't',
            '⠥': 'u', '⠧': 'v', '⠭': 'x', '⠵': 'z',
            '⠼': '[NÚMERO]',  # Indicador de número
            '⠚': '0', '⠁': '1', '⠃': '2', '⠉': '3', '⠙': '4',
            '⠑': '5', '⠋': '6', '⠛': '7', '⠓': '8', '⠊': '9',
            '⠂': ',', '⠄': "'", '⠲': '.', '⠖': '!', '⠢': '?', '⠱': '-',
            ' ': ' '
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

    def decode_caesar(self, text):
        """Decodifica texto usando cifra de César"""
        try:
            # Verifica se tem o deslocamento especificado
            if ':' in text:
                shift, text = text.split(':', 1)
                shift = int(shift)
                result = ""
                for char in text.upper():
                    if char.isalpha():
                        # Converte para 0-25, aplica o shift e volta para ASCII
                        ascii_val = ord(char) - ord('A')
                        shifted = (ascii_val - shift) % 26
                        result += chr(shifted + ord('A'))
                    else:
                        result += char
                return result
            else:
                # Se não tem shift, tenta todos os possíveis
                results = []
                for shift in range(26):
                    result = ""
                    for char in text.upper():
                        if char.isalpha():
                            ascii_val = ord(char) - ord('A')
                            shifted = (ascii_val - shift) % 26
                            result += chr(shifted + ord('A'))
                        else:
                            result += char
                    results.append(f"Shift {shift}: {result}")
                return "\n".join(results)
        except Exception as e:
            return f"Erro na decodificação César: {str(e)}"

    def decode_atbash(self, text):
        """Decodifica texto usando cifra Atbash"""
        try:
            result = ""
            for char in text.upper():
                if char.isalpha():
                    # Inverte a posição no alfabeto (A->Z, B->Y, etc)
                    ascii_val = ord(char) - ord('A')
                    inverted = 25 - ascii_val
                    result += chr(inverted + ord('A'))
                else:
                    result += char
            return result
        except Exception as e:
            return f"Erro na decodificação Atbash: {str(e)}"

    def decode_vigenere(self, text):
        """Decodifica texto usando cifra de Vigenère"""
        try:
            if ':' not in text:
                return "Erro: Formato deve ser KEY:texto"
            
            key, text = text.split(':', 1)
            key = key.upper()
            text = text.upper()
            
            if not key:
                return "Erro: Chave não fornecida"
                
            result = ""
            key_index = 0
            
            for char in text:
                if char.isalpha():
                    # Pega o valor do deslocamento da chave (0-25)
                    key_shift = ord(key[key_index % len(key)]) - ord('A')
                    # Converte o caractere para 0-25, remove o shift e volta para ASCII
                    ascii_val = ord(char) - ord('A')
                    shifted = (ascii_val - key_shift) % 26
                    result += chr(shifted + ord('A'))
                    key_index += 1
                else:
                    result += char
                    
            return result
        except Exception as e:
            return f"Erro na decodificação Vigenère: {str(e)}"

    def decode_rot13(self, text):
        """Decodifica texto usando ROT13"""
        try:
            result = ""
            for char in text.upper():
                if char.isalpha():
                    # Desloca 13 posições
                    ascii_val = ord(char) - ord('A')
                    shifted = (ascii_val + 13) % 26
                    result += chr(shifted + ord('A'))
                else:
                    result += char
            return result
        except Exception as e:
            return f"Erro na decodificação ROT13: {str(e)}"

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

    def decode_braille(self, text):
        """Decodifica texto Braille"""
        try:
            # Dicionário de caracteres Braille
            braille_dict = {
                # Letras minúsculas
                '⠁': 'a', '⠃': 'b', '⠉': 'c', '⠙': 'd', '⠑': 'e',
                '⠋': 'f', '⠛': 'g', '⠓': 'h', '⠊': 'i', '⠚': 'j',
                '⠅': 'k', '⠇': 'l', '⠍': 'm', '⠝': 'n', '⠕': 'o',
                '⠏': 'p', '⠟': 'q', '⠗': 'r', '⠎': 's', '⠞': 't',
                '⠥': 'u', '⠧': 'v', '⠺': 'w', '⠭': 'x', '⠽': 'y', '⠵': 'z',
                
                # Números
                '⠼⠚': '0', '⠼⠁': '1', '⠼⠃': '2', '⠼⠉': '3', '⠼⠙': '4',
                '⠼⠑': '5', '⠼⠋': '6', '⠼⠛': '7', '⠼⠓': '8', '⠼⠊': '9',
                
                # Pontuação
                '⠂': ',', '⠄': "'", '⠲': '.', '⠖': '!', '⠢': '?', '⠱': '-',
                '⠤': '-', '⠦': '"', '⠴': '"', '⠶': '()', '⠷': '(', '⠾': ')',
                
                # Espaço
                ' ': ' '
            }

            # Flag para maiúsculo
            is_caps = False
            result = ""
            i = 0
            
            while i < len(text):
                # Verifica se é indicador de maiúsculo
                if text[i:i+2] == '⠨⠨':
                    is_caps = True
                    i += 2
                    continue
                
                # Verifica se é número
                if text[i:i+2] in braille_dict:
                    result += braille_dict[text[i:i+2]]
                    i += 2
                # Verifica caractere único
                elif text[i] in braille_dict:
                    char = braille_dict[text[i]]
                    if is_caps:
                        char = char.upper()
                        is_caps = False
                    result += char
                    i += 1
                else:
                    # Se não reconhecer, mantém o caractere original
                    result += text[i]
                    i += 1

            return result
        except Exception as e:
            return f"Erro na decodificação Braille: {str(e)}"

    def decode_ascii(self, text):
        """Decodifica texto em ASCII"""
        try:
            # Divide o texto em números
            ascii_codes = [int(code) for code in text.split()]
            
            # Converte cada código em caractere
            result = ''.join(chr(code) for code in ascii_codes)
            
            return result
        except ValueError:
            return "Erro: Formato inválido. Use números ASCII separados por espaço."
        except Exception as e:
            return f"Erro ao decodificar: {str(e)}"
            
    def decode_base64_braille(self, text):
        """Decodifica texto em Base64"""
        try:
            # Remove espaços e quebras de linha
            text = text.strip()
            
            # Decodifica o texto
            decoded_bytes = base64.b64decode(text)
            result = decoded_bytes.decode('utf-8')
            
            return result
        except Exception as e:
            return f"Erro ao decodificar Base64: {str(e)}"

    def decode_morse_braille(self, text):
        """Decodifica texto em código Morse"""
        try:
            # Divide o texto em palavras
            words = text.strip().split('/')
            result = []
            
            # Processa cada palavra
            for word in words:
                # Divide a palavra em letras
                letters = word.strip().split()
                
                # Traduz cada letra
                decoded_word = ''
                for letter in letters:
                    if letter in self.morse_code:
                        decoded_word += self.morse_code[letter]
                    else:
                        decoded_word += '?'
                        
                result.append(decoded_word)
                
            return ' '.join(result)
        except Exception as e:
            return f"Erro ao decodificar Morse: {str(e)}"

    def decode_caesar_braille(self, text):
        """Decodifica texto usando cifra de César"""
        try:
            # Verifica se há um deslocamento especificado
            if ':' in text:
                shift, text = text.split(':', 1)
                shift = int(shift)
                shifts = [shift]
            else:
                # Se não houver deslocamento, tenta todos
                shifts = range(1, 26)
                
            results = []
            for shift in shifts:
                result = ''
                for char in text.upper():
                    if char.isalpha():
                        # Desloca o caractere
                        ascii_val = ord(char) - shift
                        if ascii_val < ord('A'):
                            ascii_val += 26
                        result += chr(ascii_val)
                    else:
                        result += char
                        
                if len(shifts) == 1:
                    return result
                else:
                    results.append(f"Deslocamento {shift}: {result}")
                    
            return "\n".join(results)
        except Exception as e:
            return f"Erro ao decodificar César: {str(e)}"

    def decode_atbash_braille(self, text):
        """Decodifica texto usando cifra Atbash"""
        try:
            result = ''
            for char in text.upper():
                if char.isalpha():
                    # Inverte a letra no alfabeto
                    ascii_val = ord('Z') - (ord(char) - ord('A'))
                    result += chr(ascii_val)
                else:
                    result += char
            return result
        except Exception as e:
            return f"Erro ao decodificar Atbash: {str(e)}"

    def decode_vigenere_braille(self, text):
        """Decodifica texto usando cifra de Vigenère"""
        try:
            # Verifica se há uma chave especificada
            if ':' not in text:
                return "Erro: Formato inválido. Use CHAVE:TEXTO"
                
            key, text = text.split(':', 1)
            key = key.upper()
            text = text.upper()
            
            result = ''
            key_index = 0
            
            for char in text:
                if char.isalpha():
                    # Calcula o deslocamento baseado na chave
                    shift = ord(key[key_index % len(key)]) - ord('A')
                    
                    # Desloca o caractere
                    ascii_val = ord(char) - shift
                    if ascii_val < ord('A'):
                        ascii_val += 26
                        
                    result += chr(ascii_val)
                    key_index += 1
                else:
                    result += char
                    
            return result
        except Exception as e:
            return f"Erro ao decodificar Vigenère: {str(e)}"

    def decode_binary_braille(self, text):
        """Decodifica texto em binário"""
        try:
            # Remove espaços e outros caracteres
            binary = ''.join(c for c in text if c in '01')
            
            # Verifica se o comprimento é múltiplo de 8
            if len(binary) % 8 != 0:
                return "Erro: O texto binário deve ter um número de bits múltiplo de 8"
                
            # Converte grupos de 8 bits em caracteres
            result = ''
            for i in range(0, len(binary), 8):
                byte = binary[i:i+8]
                result += chr(int(byte, 2))
                
            return result
        except Exception as e:
            return f"Erro ao decodificar binário: {str(e)}"

    def decode_hex_braille(self, text):
        """Decodifica texto em hexadecimal"""
        try:
            # Remove 0x, espaços e outros caracteres
            hex_text = ''.join(c for c in text if c in '0123456789abcdefABCDEF')
            
            # Verifica se o comprimento é par
            if len(hex_text) % 2 != 0:
                return "Erro: O texto hexadecimal deve ter um número par de caracteres"
                
            # Converte pares de caracteres em bytes
            result = bytes.fromhex(hex_text).decode('utf-8')
            return result
        except Exception as e:
            return f"Erro ao decodificar hexadecimal: {str(e)}"

    def decode_rot13_braille(self, text):
        """Decodifica texto usando ROT13"""
        try:
            return codecs.encode(text, 'rot_13')
        except Exception as e:
            return f"Erro ao decodificar ROT13: {str(e)}"
"""  """