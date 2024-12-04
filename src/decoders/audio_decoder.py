"""
Decodificador de áudio com suporte a análise de frequências e padrões
"""

import numpy as np
from scipy.io import wavfile
import logging
from typing import Dict, Any

class AudioDecoder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Configurações para detecção de Morse
        self.morse_config = {
            'dot_duration': 0.1,  # segundos
            'dash_duration': 0.3,  # segundos
            'threshold': 0.1      # amplitude mínima
        }
        
        # Tabela Morse inversa
        self.morse_decode = {
            '.-': 'A',     '-...': 'B',   '-.-.': 'C',
            '-..': 'D',    '.': 'E',      '..-.': 'F',
            '--.': 'G',    '....': 'H',   '..': 'I',
            '.---': 'J',   '-.-': 'K',    '.-..': 'L',
            '--': 'M',     '-.': 'N',     '---': 'O',
            '.--.': 'P',   '--.-': 'Q',   '.-.': 'R',
            '...': 'S',    '-': 'T',      '..-': 'U',
            '...-': 'V',   '.--': 'W',    '-..-': 'X',
            '-.--': 'Y',   '--..': 'Z',
            '.----': '1',  '..---': '2',  '...--': '3',
            '....-': '4',  '.....': '5',  '-....': '6',
            '--...': '7',  '---..': '8',  '----.': '9',
            '-----': '0'
        }

    def analyze_audio(self, file_path: str) -> Dict[str, Any]:
        """
        Analisa um arquivo de áudio usando vários métodos
        """
        try:
            # Carregar arquivo WAV
            sample_rate, audio_data = wavfile.read(file_path)
            
            # Converter para mono se estéreo
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            results = {}
            
            # Informações básicas
            results["Taxa de Amostragem"] = f"{sample_rate} Hz"
            results["Duração"] = f"{len(audio_data)/sample_rate:.2f} segundos"
            
            # Análise de amplitude
            results["Amplitude Máxima"] = f"{np.max(np.abs(audio_data)):.2f}"
            results["Amplitude Média"] = f"{np.mean(np.abs(audio_data)):.2f}"
            
            # Análise espectral
            frequencies = self.analyze_frequencies(audio_data, sample_rate)
            results["Frequências Dominantes"] = frequencies
            
            # Detecção de Morse
            morse = self.detect_morse(audio_data, sample_rate)
            if morse:
                results["Código Morse Detectado"] = morse
            
            return results
            
        except Exception as e:
            self.logger.error(f"Erro ao analisar áudio: {str(e)}")
            raise

    def analyze_frequencies(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """
        Analisa as frequências presentes no áudio
        """
        try:
            # Calcular FFT
            fft_data = np.fft.fft(audio_data)
            freqs = np.fft.fftfreq(len(fft_data), 1/sample_rate)
            
            # Pegar apenas frequências positivas
            pos_mask = freqs > 0
            freqs = freqs[pos_mask]
            fft_data = np.abs(fft_data[pos_mask])
            
            # Encontrar picos
            from scipy.signal import find_peaks
            peaks, _ = find_peaks(fft_data, height=np.max(fft_data)/10)
            
            # Pegar as 5 frequências mais fortes
            peak_freqs = freqs[peaks]
            peak_magnitudes = fft_data[peaks]
            
            # Ordenar por magnitude
            sorted_indices = np.argsort(peak_magnitudes)[::-1][:5]
            
            result = []
            for idx in sorted_indices:
                freq = peak_freqs[idx]
                mag = peak_magnitudes[idx]
                result.append(f"{freq:.1f} Hz")
            
            return ", ".join(result)
            
        except Exception as e:
            self.logger.error(f"Erro na análise de frequências: {str(e)}")
            return "Erro na análise de frequências"

    def detect_morse(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """
        Detecta código Morse no áudio
        """
        try:
            # Normalizar áudio
            audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Calcular envelope do sinal
            from scipy.signal import hilbert
            envelope = np.abs(hilbert(audio_data))
            
            # Binarizar o sinal
            threshold = self.morse_config['threshold']
            binary_signal = envelope > threshold
            
            # Encontrar pulsos
            from scipy.signal import find_peaks
            peaks, _ = find_peaks(envelope, height=threshold)
            
            # Converter durações em dots e dashes
            dot_samples = int(self.morse_config['dot_duration'] * sample_rate)
            dash_samples = int(self.morse_config['dash_duration'] * sample_rate)
            
            morse_code = []
            current_signal = []
            
            for i in range(1, len(peaks)):
                duration = peaks[i] - peaks[i-1]
                
                if duration < dot_samples * 1.5:
                    current_signal.append('.')
                elif duration < dash_samples * 1.5:
                    current_signal.append('-')
                else:
                    # Espaço entre letras
                    if current_signal:
                        morse_code.append(''.join(current_signal))
                        current_signal = []
            
            # Adicionar último caractere
            if current_signal:
                morse_code.append(''.join(current_signal))
            
            # Decodificar
            text = []
            for code in morse_code:
                if code in self.morse_decode:
                    text.append(self.morse_decode[code])
            
            return "".join(text) if text else "Nenhum código Morse detectado"
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de Morse: {str(e)}")
            return "Erro na detecção de Morse"
