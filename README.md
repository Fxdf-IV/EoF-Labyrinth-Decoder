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

![Aba Informações](resources/README/aba%20info.jpg)

## Decodificadores

### Labirinto
- Exploração automática de caminhos
- Validação de sequências de palavras-chave
- Mapeamento de caminhos conhecidos do jogo

![Aba Labirinto](resources/README/aba%20labirinto.jpg)

### Imagem
- Detecção de QR codes e códigos de barras
- OCR para texto em imagens
- Análise de padrões visuais
- Detecção de sigilos e símbolos
- Análise de cores e padrões

![Aba Imagem](resources/README/aba%20image.jpg)

### Texto
- Decodificação automática de:
  - Base64
  - Hexadecimal
  - Binário
  - Cifra de César
  - Cifra Atbash
  - Cifra de Vigenère
- Análise de padrões de texto
- Detecção de sequências repetidas

![Aba Informações](resources/README/aba%20info.jpg)

### Áudio
- Análise espectral
- Análise de frequências
- Análise de amplitude

![Aba Áudio](resources/README/aba%20audio.jpg)

## Requisitos

- Python 3.13+
- Bibliotecas: tkinter, pygame, matplotlib, soundfile, numpy, scipy, Pillow

## Instalação

1. Clone o repositório: `git clone <url-do-repositorio>`
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o aplicativo: `python main.py`

## Contribuição

Sinta-se à vontade para contribuir com melhorias, correções de bugs ou novas funcionalidades. Para isso, faça um fork do repositório, crie uma branch com suas alterações e envie um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.
