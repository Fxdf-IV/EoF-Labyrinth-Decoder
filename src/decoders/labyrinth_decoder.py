"""
Decodificador do labirinto
"""

import os

class LabyrinthDecoder:
    def __init__(self):
        self.items = [
            {
                "name": "Crânio de Corvo",
                "path_suffix": "Krev/Strach/Strach/Strach",
                "sequence": "Este caminho contém uma sequência importante. Relacionado a sangue. Envolve medo.",
                "files": "Cornix",
                "computer_hint": "Percorra o labirinto",
                "technical_hint": "Observe os sigilos e as inscrições que os cercam. A sequência repetitiva pode conter a chave para decifrar o significado central. Leia cuidadosamente os detalhes destacados. USE O ALFABETO"
            },
            {
                "name": "Monóculo Quebrado",
                "path_suffix": "Smrt/Krev/Znalost/Znalost",
                "sequence": "Este caminho contém uma sequência importante. Relacionado a sangue. Tem conexão com morte. Requer conhecimento.",
                "files": "Newton, Visio",
                "computer_hint": "7 elas são",
                "technical_hint": "Os valores hexadecimais correspondem a algo visível em uma sequência específica. Analise as cores e relacione-as com os padrões exibidos."
            },
            {
                "name": "Garrafa Aqua Amassada",
                "path_suffix": "Strach/Krev/Krev/Smrt",
                "sequence": "Este caminho contém uma sequência importante. Relacionado a energia e medo.",
                "files": "Aqua",
                "computer_hint": "Siga o fluxo da água",
                "technical_hint": "Examine os padrões de fluxo e as marcações nas paredes. A direção e intensidade podem indicar um caminho específico."
            },
            {
                "name": "Disco DEMO",
                "path_suffix": "Smrt/Energie/Energie/Energie",
                "sequence": "Conhecimento leva à energia e morte.",
                "files": "Demo_disc",
                "computer_hint": "A música guia o caminho",
                "technical_hint": "As frequências sonoras podem revelar padrões ocultos. Preste atenção às variações rítmicas."
            },
            {
                "name": "Pote de Vidro com Algo Suspeito Dentro",
                "path_suffix": "Znalost/Energie/Energie/Znalost",
                "sequence": "Medo se transforma em sangue e energia.",
                "files": "Jar_content",
                "computer_hint": "O conteúdo revela segredos",
                "technical_hint": "Analise a composição e as reações químicas. Os elementos podem formar um padrão significativo."
            },
            {
                "name": "Bola Mágica 8",
                "path_suffix": "Krev/Znalost/Krev/Krev",
                "sequence": "Conhecimento da morte traz medo.",
                "files": "Magic_8",
                "computer_hint": "A resposta está nas estrelas",
                "technical_hint": "Os padrões astrológicos e números podem conter mensagens codificadas."
            },
            {
                "name": "Vaquinha",
                "path_suffix": "Znalost/Strach/Smrt/Smrt",
                "sequence": "Sangue alimenta energia e conhecimento.",
                "files": "Cow",
                "computer_hint": "Siga os rastros",
                "technical_hint": "As pegadas e marcas no chão formam um padrão específico. Observe a direção e profundidade."
            },
            {
                "name": "Brinquedo Cachorro-bola",
                "path_suffix": "Energie/Znalost/Smrt/Krev",
                "sequence": "Medo da morte leva ao sangue.",
                "files": "Dog_ball",
                "computer_hint": "Brinque com as sombras",
                "technical_hint": "As sombras projetadas podem revelar símbolos ocultos. Observe em diferentes ângulos."
            },
            {
                "name": "Filtro dos Sonhos",
                "path_suffix": "Krev/Smrt/Energie/Energie",
                "sequence": "Energia do conhecimento gera medo.",
                "files": "Dreamcatcher",
                "computer_hint": "Os sonhos mostram o caminho",
                "technical_hint": "Os padrões da teia contêm uma sequência específica. Analise a geometria e símbolos."
            },
            {
                "name": "Boné de Sapo",
                "path_suffix": "Znalost/Strach/Strach/Krev",
                "sequence": "Morte e medo geram energia.",
                "files": "Frog_cap",
                "computer_hint": "Pule entre os portais",
                "technical_hint": "A sequência de saltos forma um padrão. Observe os pontos de aterrissagem."
            },
            {
                "name": "Relógio de Gatinho",
                "path_suffix": "Krev/Smrt/Strach/Smrt",
                "sequence": "Conhecimento do sangue leva à morte.",
                "files": "Cat_clock",
                "computer_hint": "O tempo não para",
                "technical_hint": "Os números e posições dos ponteiros formam uma sequência. Analise os intervalos."
            },
            {
                "name": "Mantega",
                "path_suffix": "Znalost/Krev/Strach/Krev",
                "sequence": "Sangue da morte gera energia.",
                "files": "Butter",
                "computer_hint": "Derreta os símbolos",
                "technical_hint": "O padrão de derretimento revela mensagens ocultas. Observe a ordem e direção."
            },
            {
                "name": "Moeda",
                "path_suffix": "Znalost/Znalost/Energie/Smrt",
                "sequence": "Energia do sangue traz conhecimento.",
                "files": "Coin",
                "computer_hint": "Duas faces da verdade",
                "technical_hint": "As inscrições em ambos os lados formam um código. Compare e combine os símbolos."
            },
            {
                "name": "Baú",
                "path_suffix": "Krev/Znalost/Smrt/Smrt",
                "sequence": "Medo do conhecimento leva à morte.",
                "files": "Chest",
                "computer_hint": "O tesouro está protegido",
                "technical_hint": "A sequência de travas forma um padrão específico. Analise a ordem de desbloqueio."
            },
            {
                "name": "Miniatura de Fusca Azul",
                "path_suffix": "Smrt/Znalost/Smrt/Smrt",
                "sequence": "Morte energizada pelo sangue.",
                "files": "Blue_beetle",
                "computer_hint": "Siga as rodas",
                "technical_hint": "As marcas das rodas formam um caminho específico. Observe a profundidade e direção."
            },
            {
                "name": "PenDrive Amassado",
                "path_suffix": "Znalost/Smrt/Energie/Strach",
                "sequence": "Conhecimento do medo leva ao sangue.",
                "files": "Pendrive",
                "computer_hint": "Os dados não mentem",
                "technical_hint": "Os arquivos corrompidos contêm padrões. Analise os bytes e sequências binárias."
            },
            {
                "name": "Anel de Corvo",
                "path_suffix": "Krev/Znalost/Energie/Energie",
                "sequence": "Sangue do conhecimento gera energia.",
                "files": "Crow_ring",
                "computer_hint": "O círculo se fecha",
                "technical_hint": "As inscrições no anel formam uma sequência circular. Observe o ponto de início."
            },
            {
                "name": "Bracelete Dourado",
                "path_suffix": "Smrt/Energie/Strach/Krev",
                "sequence": "Energia da morte traz medo.",
                "files": "Golden_bracelet",
                "computer_hint": "O brilho guia",
                "technical_hint": "Os padrões de reflexão formam símbolos específicos. Analise em diferentes intensidades de luz."
            },
            {
                "name": "Chave do Labirinto",
                "path_suffix": "Strach/Energie/Znalost",
                "sequence": "Medo da energia traz conhecimento.",
                "files": "Maze_key",
                "computer_hint": "A chave final",
                "technical_hint": "As ranhuras da chave formam um código específico. Compare com os padrões das fechaduras."
            },
            {
                "name": "Grimório",
                "path_suffix": "Znalost/Krev/Strach/Krev",
                "sequence": "Conhecimento do sangue traz medo.",
                "files": "Grimoire",
                "computer_hint": "As páginas sussurram",
                "technical_hint": "As páginas contêm padrões ocultos. Analise a ordem e símbolos em cada página."
            }
        ]

    def decode_labyrinth(self, base_path):
        """Decodifica o labirinto a partir do caminho base fornecido"""
        results = []
        
        for item in self.items:
            # Constrói o caminho completo usando apenas barras /
            full_path = os.path.join(base_path, item["path_suffix"]).replace("\\", "/")
            
            # Cria uma cópia do item e adiciona o caminho completo
            result = item.copy()
            result["path"] = full_path
            
            results.append({
                "name": result["name"],
                "path": result["path"],
                "sequence": result["sequence"],
                "files": result["files"],
                "computer_hint": result["computer_hint"],
                "technical_hint": result["technical_hint"]
            })
        
        return results
