# EoF Labyrinth Decoder

Esta é uma ferramenta especialmente desenvolvida para o jogo [Enigma of Fear (Enigma do Medo)](https://store.steampowered.com/app/1779190/Enigma_of_Fear/) disponível na Steam.

## Sobre o Jogo

Enigma of Fear é um jogo de terror psicológico em primeira pessoa que mistura elementos de puzzle e exploração. Na história do Samuel, você precisa desvendar a criptografia dos itens explorando o labirinto de pastas do jogo.

## Sobre esta Ferramenta

O EoF Labyrinth Decoder é uma ferramenta que ajuda a explorar todos os caminhos possíveis dentro do labirinto do jogo, localizando arquivos importantes e excluindo caminhos que levam a sustos ("uh-oh"). 

### Características:
- Interface gráfica intuitiva
- Exploração automática de todos os caminhos possíveis
- Exclusão de caminhos que levam a sustos
- Barra de progresso em tempo real
- Exibição clara dos caminhos encontrados

## Como Usar

1. Baixe o instalador na seção [Releases](../../releases)
2. Execute o instalador
3. Abra o programa
4. Clique em "Procurar" e selecione a pasta "Labyrinthus" do jogo
   - Geralmente localizada em: `C:\Program Files (x86)\Steam\steamapps\common\Enigma of Fear\Labyrinthus`
5. Clique em "Iniciar Exploração" e aguarde o processo terminar
6. Os caminhos válidos serão exibidos na tela

## Instalação Manual (Para Desenvolvedores)

Se você preferir executar o código fonte:

1. Clone este repositório
```bash
git clone https://github.com/seu-usuario/eof-labyrinth-decoder.git
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Execute o programa
```bash
python maze_solver.py
```

## Requisitos
- Windows 7 ou superior
- [Enigma of Fear](https://store.steampowered.com/app/1779190/Enigma_of_Fear/) instalado
- 5MB de espaço em disco para o programa
