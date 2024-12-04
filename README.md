# EoF Enigma Decoder

Um decodificador multi-modal para o jogo Enigma of Fear, capaz de processar e decodificar diversos tipos de puzzles e mensagens ocultas.

## Características

- Interface gráfica com tema Matrix
- Suporte para múltiplos tipos de decodificação:
  - Labirinto
  - Imagem
  - Texto
  - Áudio
- Análise avançada de padrões
- Sistema de logging detalhado
- Testes unitários abrangentes

## Decodificadores

### Labirinto
- Exploração automática de caminhos
- Validação de sequências de palavras-chave
- Mapeamento de caminhos conhecidos do jogo

### Imagem
- Detecção de QR codes e códigos de barras
- OCR para texto em imagens
- Análise de padrões visuais
- Detecção de sigilos e símbolos
- Análise de cores e padrões

### Texto
- Decodificação automática de:
  - Base64
  - Hexadecimal
  - Binário
  - Código Morse
  - Cifra de César
  - Cifra Atbash
  - Cifra de Vigenère
- Análise de padrões de texto
- Detecção de sequências repetidas

### Áudio
- Detecção de código Morse em áudio
- Análise de tons DTMF
- Análise espectral
- Detecção de mensagens ocultas
- Análise de estrutura musical

## Requisitos

```
numpy>=1.21.0
pillow>=8.3.0
opencv-python>=4.5.0
matplotlib>=3.4.0
morse-translator>=1.1.0
pyzbar>=0.1.8
pydub>=0.25.1
scipy>=1.7.0
scikit-image>=0.18.0
python-dotenv>=0.19.0
qrcode>=7.3.0
python-barcode>=0.13.1
pytesseract>=0.3.8
librosa>=0.8.1
cryptography>=41.0.0
pyttsx3>=2.90
braille-translator>=0.1.0
```

## Instalação

1. Clone o repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute o programa:
   ```
   python src/main.py
   ```

## Testes

Execute os testes unitários:
```
python -m unittest tests/test_decoders.py
```

## Estrutura do Projeto

```
EoF Labyrinth Decoder/
├── src/
│   ├── ui/
│   │   ├── main_window.py
│   │   └── dialogs/
│   ├── decoders/
│   │   ├── labyrinth_decoder.py
│   │   ├── image_decoder.py
│   │   ├── text_decoder.py
│   │   └── audio_decoder.py
│   └── main.py
├── tests/
│   └── test_decoders.py
├── resources/
│   └── known_patterns/
├── logs/
├── requirements.txt
└── README.md
```

## Uso

1. Inicie o programa
2. Selecione a aba apropriada para o tipo de puzzle
3. Carregue o arquivo ou insira o texto/padrão
4. Use as ferramentas de análise e decodificação
5. Verifique os resultados e logs

## Contribuindo

1. Fork o projeto
2. Crie sua branch de feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.
