# EoF Enigma Decoder

Pensei como o Samuel resolveria esse problema, e então decidi agir como ele, desenvolvendo este programa para isso! 
O EoF Labyrinth Decoder é um decodificador multi-modal para o jogo Enigma of Fear, capaz de processar e decodificar os puzzles de itens amaldiçoados em que o Samuel está encarregado de resolver.

## Características

- Interface gráfica com tema Matrix (Para dar um charme estilo Samuel Hacker)
- Suporte para múltiplos tipos de decodificação:
  - Labirinto de pastas
  - Imagens
  - Textos
  - Áudios
- Análise de padrões
- Sistema de logging detalhado
- Testes unitários abrangentes

![Aba Informações](resources/README/aba_info.jpg)

## Decodificadores

### Labirinto
- Exploração automática de caminhos de pastas
- Validação de sequências de palavras-chave
- Dicas técnicas para ajudar na solução

![Aba Labirinto](resources/README/aba_labirinto.jpg)

### Imagem
- Detecção de QR codes e códigos de barras (INOPERANTE)
- OCR para texto em imagens
- Análise de padrões visuais
- Detecção de sigilos e símbolos
- Análise de cores e padrões

![Aba Imagem](resources/README/aba_image.jpg)

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

![Aba Texto](resources/README/aba_texto.jpg)

### Áudio
- Análise espectral
- Análise de frequências
- Análise de amplitude

![Aba Áudio](resources/README/aba_audio.jpg)

## Requisitos

- Python 3.13+
- Bibliotecas: tkinter, pygame, matplotlib, soundfile, numpy, scipy, Pillow

## Download e Uso

1. Na página do projeto no GitHub:
   - Clique na seção "Releases" no lado direito
   - Ou [clique aqui](../../releases) para ir direto
2. Em "Assets" da release mais recente:
   - Clique em `EoFLabyrinthDecoder.exe` para baixar
   - Se o Chrome bloquear o download:
     - Clique nos 3 pontos ao lado do aviso
     - Selecione "Manter assim mesmo"
     - Se aparecer outro aviso, clique em "Mostrar mais" e depois "Manter mesmo assim"
3. Depois de baixar:
   - Não precisa instalar
   - Você pode mover o arquivo para qualquer pasta
   - Ao tentar executar, o Windows Defender pode mostrar um aviso
   - Clique em "Mais informações" e depois em "Executar assim mesmo"

> **Nota sobre segurança**: O aplicativo é marcado como não seguro porque é um executável não assinado digitalmente (certificados digitais são caros). O código fonte está disponível aqui no GitHub para verificação. O programa é 100% seguro e não faz nada além do que está documentado.

## Contribuição

Sinta-se à vontade para contribuir com melhorias, correções de bugs ou novas funcionalidades. Para isso, faça um fork do repositório, crie uma branch com suas alterações e envie um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.

## Observações

- Este projeto foi desenvolvido com o intuito de auxiliar o jogador a ter uma experiência mais facil para resolver os puzzles de itens amaldiçoados no jogo Enigma of Fear. O objetivo principal é tornar o jogo mais interessante e divertido para todos os jogadores, independentemente de suas habilidades de programação ou conhecimentos de informática ou prática em resolver ARGS.

- Muitas das funcioanlidades mais complexas, como o uso de QR codes e código de barras não funcionam, pois seriam necessários recursos extras, que nesse caso não foram implementados. Já que o foco do projeto é tornar o jogo mais divertido, espero isso nao seria um problema para o jogador.
