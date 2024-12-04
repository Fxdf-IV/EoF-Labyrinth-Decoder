import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.decoders.audio_decoder import AudioDecoder
import numpy as np
from scipy.io import wavfile

def create_test_audio():
    """Cria um arquivo de áudio de teste com código Morse"""
    # Configurações
    sample_rate = 44100
    duration = 3  # segundos
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Criar sinal de teste (1000Hz)
    frequency = 1000
    signal = np.sin(2 * np.pi * frequency * t)
    
    # Adicionar código Morse (SOS = ... --- ...)
    morse_signal = np.zeros_like(t)
    
    # Função para adicionar um pulso
    def add_pulse(start, duration):
        mask = (t >= start) & (t < start + duration)
        morse_signal[mask] = 1
    
    # Adicionar ... (S)
    add_pulse(0.2, 0.1)  # dot
    add_pulse(0.4, 0.1)  # dot
    add_pulse(0.6, 0.1)  # dot
    
    # Adicionar --- (O)
    add_pulse(1.0, 0.3)  # dash
    add_pulse(1.4, 0.3)  # dash
    add_pulse(1.8, 0.3)  # dash
    
    # Adicionar ... (S)
    add_pulse(2.2, 0.1)  # dot
    add_pulse(2.4, 0.1)  # dot
    add_pulse(2.6, 0.1)  # dot
    
    # Combinar sinais
    final_signal = signal * morse_signal
    
    # Normalizar
    final_signal = final_signal / np.max(np.abs(final_signal))
    
    # Salvar arquivo
    output_file = "test_morse_sos.wav"
    wavfile.write(output_file, sample_rate, final_signal.astype(np.float32))
    return output_file

def test_audio_decoder():
    """Testa as funcionalidades do AudioDecoder"""
    print("Iniciando teste do AudioDecoder...")
    
    # Criar instância do decoder
    decoder = AudioDecoder()
    
    # Criar arquivo de teste
    test_file = create_test_audio()
    print(f"\nArquivo de teste criado: {test_file}")
    
    try:
        # Analisar áudio
        print("\nAnalisando áudio...")
        results = decoder.analyze_audio(test_file)
        
        # Mostrar resultados
        print("\nResultados da análise:")
        for key, value in results.items():
            print(f"{key}: {value}")
        
    except Exception as e:
        print(f"Erro durante o teste: {str(e)}")
    finally:
        # Limpar arquivo de teste
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"\nArquivo de teste removido: {test_file}")

if __name__ == "__main__":
    test_audio_decoder()
