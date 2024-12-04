"""
Configurações globais para o EoF Enigma Decoder.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any

# Diretórios do projeto
PROJECT_ROOT = Path(__file__).parent.parent
RESOURCES_DIR = PROJECT_ROOT / "resources"
LOGS_DIR = PROJECT_ROOT / "logs"
KNOWN_PATTERNS_DIR = RESOURCES_DIR / "known_patterns"

# Criar diretórios se não existirem
for directory in [RESOURCES_DIR, LOGS_DIR, KNOWN_PATTERNS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configurações de logging
LOG_FILE = LOGS_DIR / "decoder.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

# Configurações da interface
UI_CONFIG = {
    'theme': {
        'background': '#000000',      # Preto
        'foreground': '#00ff00',      # Verde
        'button_bg': '#000000',       # Preto
        'button_fg': '#00ff00',       # Verde
        'entry_bg': '#000000',        # Preto
        'entry_fg': '#00ff00',        # Verde
        'text_bg': '#000000',         # Preto
        'text_fg': '#00ff00',         # Verde
        'label_bg': '#000000',        # Preto
        'label_fg': '#00ff00',        # Verde
        'tab_bg': '#000000',          # Preto
        'tab_fg': '#00ff00',          # Verde
        'tab_selected': '#000000',    # Preto
        'scrollbar_bg': '#000000',    # Preto
        'scrollbar_fg': '#00ff00',    # Verde
        'button_active': '#000000',   # Preto
        'button_hover': '#000000',    # Preto
        'highlight_bg': '#000000',    # Preto
        'highlight_fg': '#00ff00',    # Verde
        'font': ('Courier', 10),      # Fonte estilo terminal
        'title_font': ('Courier', 12, 'bold')
    },
    
    'window': {
        'title': 'EoF Enigma Decoder',
        'geometry': '800x600',
        'min_size': (800, 600)
    },
    
    'tabs': {
        'names': ['Labyrinth Decoder', 'Text Decoder', 'Image Decoder', 'Audio Decoder'],
        'padding': 10
    }
}

# Configurações dos decodificadores
DECODER_CONFIG = {
    "labyrinth": {
        "known_keywords": [
            "KREV",      # Sangue
            "SMRT",      # Morte
            "ZNALOST",   # Conhecimento
            "ENERGIE",   # Energia
            "STRACH"     # Medo
        ],
        "max_depth": 10,
        "timeout": 30  # segundos
    },
    "image": {
        "min_pattern_size": 10,
        "max_pattern_size": 100,
        "color_threshold": 0.1,
        "edge_threshold": 100,
        "qr_timeout": 5  # segundos
    },
    "text": {
        "min_pattern_length": 3,
        "max_pattern_length": 50,
        "default_caesar_shift": 3,
        "default_vigenere_key": "STRACH"
    },
    "audio": {
        "sample_rate": 44100,
        "morse_threshold": 0.1,
        "min_silence_len": 100,  # ms
        "min_frequency": 20,     # Hz
        "max_frequency": 20000   # Hz
    }
}

# Configurações de segurança
SECURITY_CONFIG = {
    "max_file_size": 100 * 1024 * 1024,  # 100MB
    "allowed_image_extensions": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    "allowed_audio_extensions": [".wav", ".mp3", ".ogg", ".flac"],
    "max_text_length": 1000000,  # caracteres
    "max_processing_time": 300   # segundos
}

def get_config() -> Dict[str, Any]:
    """Retorna todas as configurações em um único dicionário."""
    return {
        "project_root": str(PROJECT_ROOT),
        "resources_dir": str(RESOURCES_DIR),
        "logs_dir": str(LOGS_DIR),
        "known_patterns_dir": str(KNOWN_PATTERNS_DIR),
        "log_file": str(LOG_FILE),
        "log_format": LOG_FORMAT,
        "log_level": LOG_LEVEL,
        "ui": UI_CONFIG,
        "decoders": DECODER_CONFIG,
        "security": SECURITY_CONFIG
    }

def setup_logging():
    """Configura o sistema de logging."""
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

def validate_config():
    """Valida as configurações e cria diretórios necessários."""
    # Verificar e criar diretórios
    for directory in [RESOURCES_DIR, LOGS_DIR, KNOWN_PATTERNS_DIR]:
        if not directory.exists():
            directory.mkdir(parents=True)
    
    # Verificar permissões de escrita
    try:
        test_file = LOGS_DIR / "test.tmp"
        test_file.touch()
        test_file.unlink()
    except Exception as e:
        raise PermissionError(f"Erro de permissão no diretório de logs: {e}")
    
    # Validar configurações específicas
    if DECODER_CONFIG["labyrinth"]["max_depth"] < 1:
        raise ValueError("max_depth deve ser maior que 0")
    
    if DECODER_CONFIG["audio"]["sample_rate"] not in [44100, 48000, 96000]:
        raise ValueError("sample_rate inválido")
    
    if SECURITY_CONFIG["max_file_size"] > 1024 * 1024 * 1024:  # 1GB
        raise ValueError("max_file_size muito grande")

# Inicialização
if __name__ == "__main__":
    setup_logging()
    validate_config()
