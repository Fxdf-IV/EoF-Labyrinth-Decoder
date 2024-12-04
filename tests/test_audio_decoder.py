import unittest
import os
import numpy as np
from src.decoders.audio_decoder import AudioDecoder

class TestAudioDecoder(unittest.TestCase):
    def setUp(self):
        self.decoder = AudioDecoder()
        self.test_dir = "test_audio"
        
        # Criar diretório para arquivos de teste
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
            
        # Criar arquivo de áudio de teste com código Morse
        self.morse_audio_path = os.path.join(self.test_dir, "morse.wav")
        self.create_test_morse_audio()
        
        # Criar arquivo de áudio com frequências específicas
        self.freq_audio_path = os.path.join(self.test_dir, "frequencies.wav")
        self.create_test_frequency_audio()
        
    def tearDown(self):
        # Limpar arquivos de teste
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)
            
    def create_test_morse_audio(self):
        """Cria arquivo de áudio com código Morse"""
        # Simular "SOS" em Morse
        sample_rate = 44100
        duration = 0.1  # duração de cada bip
        
        # Gerar tons para pontos e traços
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = np.sin(2*np.pi*1000*t)
        
        # Montar sequência SOS (... --- ...)
        sequence = np.concatenate([
            tone, np.zeros_like(tone),  # .
            tone, np.zeros_like(tone),  # .
            tone, np.zeros_like(tone),  # .
            np.zeros_like(tone)*3,      # espaço
            tone*3, np.zeros_like(tone),  # -
            tone*3, np.zeros_like(tone),  # -
            tone*3, np.zeros_like(tone),  # -
            np.zeros_like(tone)*3,      # espaço
            tone, np.zeros_like(tone),  # .
            tone, np.zeros_like(tone),  # .
            tone, np.zeros_like(tone)   # .
        ])
        
        # Salvar arquivo
        self.decoder.save_wave(sequence, sample_rate, self.morse_audio_path)
        
    def create_test_frequency_audio(self):
        """Cria arquivo de áudio com frequências específicas"""
        sample_rate = 44100
        duration = 1.0
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Criar sinal com múltiplas frequências
        signal = (
            np.sin(2*np.pi*440*t) +   # A4 note
            np.sin(2*np.pi*880*t) +   # A5 note
            np.sin(2*np.pi*1760*t)    # A6 note
        )
        
        # Normalizar
        signal = signal / np.max(np.abs(signal))
        
        # Salvar arquivo
        self.decoder.save_wave(signal, sample_rate, self.freq_audio_path)
        
    def test_spectrogram_generation(self):
        """Testa geração de espectrograma"""
        spectrogram = self.decoder.generate_spectrogram(self.freq_audio_path)
        
        self.assertIsNotNone(spectrogram)
        self.assertTrue(isinstance(spectrogram, np.ndarray))
        
    def test_morse_detection(self):
        """Testa detecção de código Morse em áudio"""
        morse_code = self.decoder.detect_morse(self.morse_audio_path)
        
        self.assertIsInstance(morse_code, str)
        self.assertEqual(morse_code.strip(), "... --- ...")
        
    def test_frequency_analysis(self):
        """Testa análise de frequências"""
        frequencies = self.decoder.analyze_frequencies(self.freq_audio_path)
        
        self.assertIsInstance(frequencies, list)
        self.assertGreater(len(frequencies), 0)
        
        # Verificar se as frequências esperadas estão presentes
        expected_freqs = [440, 880, 1760]
        for freq in expected_freqs:
            found = False
            for detected_freq in frequencies:
                if abs(detected_freq - freq) < 10:  # tolerância de 10 Hz
                    found = True
                    break
            self.assertTrue(found, f"Frequência {freq}Hz não detectada")
            
    def test_pattern_detection(self):
        """Testa detecção de padrões temporais"""
        patterns = self.decoder.detect_patterns(self.morse_audio_path)
        
        self.assertIsInstance(patterns, list)
        self.assertGreater(len(patterns), 0)
        
    def test_invalid_audio(self):
        """Testa tratamento de arquivos de áudio inválidos"""
        invalid_path = os.path.join(self.test_dir, "invalid.wav")
        
        # Criar arquivo inválido
        with open(invalid_path, 'wb') as f:
            f.write(b'Invalid audio data')
            
        with self.assertRaises(ValueError):
            self.decoder.generate_spectrogram(invalid_path)
            
        with self.assertRaises(ValueError):
            self.decoder.detect_morse(invalid_path)
            
        with self.assertRaises(ValueError):
            self.decoder.analyze_frequencies(invalid_path)
            
    def test_noise_handling(self):
        """Testa tratamento de ruído"""
        # Criar áudio com ruído
        sample_rate = 44100
        duration = 1.0
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Sinal + ruído
        signal = np.sin(2*np.pi*440*t) + np.random.normal(0, 0.1, len(t))
        noisy_path = os.path.join(self.test_dir, "noisy.wav")
        self.decoder.save_wave(signal, sample_rate, noisy_path)
        
        # Verificar se ainda detecta a frequência principal
        frequencies = self.decoder.analyze_frequencies(noisy_path)
        found_440 = False
        for freq in frequencies:
            if abs(freq - 440) < 10:
                found_440 = True
                break
        self.assertTrue(found_440)

if __name__ == '__main__':
    unittest.main()
