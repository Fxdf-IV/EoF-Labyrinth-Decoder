# EoF Labyrinth Decoder

Esta é uma ferramenta especialmente desenvolvida para o jogo [Enigma of Fear (Enigma do Medo)](https://store.steampowered.com/app/1779190/Enigma_of_Fear/) disponível na Steam.

## Sobre o Jogo

Enigma of Fear é um jogo de terror psicológico em primeira pessoa que mistura elementos de puzzle e exploração. Na história do Samuel, você precisa desvendar a criptografia dos itens explorando o labirinto de pastas do jogo.

## Sobre esta Ferramenta

Pensei como o Samuel resolveria esse problema, e então decidi agir como ele, desenvolvendo este script. O EoF Labyrinth Decoder é uma ferramenta que ajuda a explorar todos os caminhos possíveis dentro do labirinto do jogo, localizando arquivos importantes e excluindo caminhos que levam a sustos ("uh-oh"). 

### Características:
- Interface gráfica intuitiva
- Exploração automática de todos os caminhos possíveis
- Exclusão de caminhos que levam a sustos
- Barra de progresso em tempo real
- Exibição clara dos caminhos encontrados

## Instalação e Uso

### Para Usuários
1. Na página do projeto no GitHub:
   - Clique na seção "Releases" no lado direito
   - Ou [clique aqui](../../releases) para ir direto
2. Em "Assets" da release mais recente:
   - Clique em `EoFLabyrinthDecoder.exe` para baixar
3. Depois de baixar:
   - Não precisa instalar
   - Você pode mover o arquivo para qualquer pasta
   - Basta dar duplo clique para executar
4. Na primeira execução:
   - O Windows vai mostrar um aviso de segurança
   - É normal, pois o programa não tem certificado digital
   - Clique em "Mais informações"
   - Depois clique em "Executar assim mesmo"
   OBS: Juro que não estou te hackeando!

### Como Usar o Programa
1. Com o programa aberto:
   - Clique no botão "Procurar"
   - Navegue até a pasta do jogo Enigma of Fear
   - Selecione a pasta "Labyrinthus"
      - Geralmente em: `C:\Program Files (x86)\Steam\steamapps\common\Enigma of Fear\Labyrinthus`
2. Clique em "Iniciar Exploração"
3. Aguarde a análise completar:
   - A barra de progresso mostrará o andamento
   - Os caminhos seguros aparecerão na área de texto
   - Caminhos com "uh-oh" são automaticamente ignorados

### Para Desenvolvedores
Se você quer executar o código fonte:

1. Clone este repositório:
```bash
git clone https://github.com/Fxdf-IV/EoF-Labyrinth-Decoder.git
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o programa:
```bash
python maze_solver.py
```

## Requisitos
- Windows 7 ou superior
- [Enigma of Fear](https://store.steampowered.com/app/1779190/Enigma_of_Fear/) instalado

## Problemas Conhecidos
Se você encontrar algum problema, por favor entre em contato com o usuário Fxdf#2179 no Discord.

## Contribuindo
Contribuições são bem-vindas! Se você tem uma sugestão de melhoria:
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request
