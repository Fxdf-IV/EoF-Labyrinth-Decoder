"""
Decodificador do labirinto
"""

class LabyrinthDecoder:
    def __init__(self):
        self.items = {
            "Crânio de Corvo": {
                "path": "Labyrinthus/Krev/Strach/Strach/Strach",
                "sequence": "Este caminho contém uma sequência importante. Relacionado a sangue. Envolve medo.",
                "files": "Cornix",
                "hint": "Percorra o labirinto",
                "tech_hint": "Observe os sigilos e as inscrições que os cercam. A sequência repetitiva pode conter a chave para decifrar o significado central. Leia cuidadosamente os detalhes destacados. USE O ALFABETO"
            },
            "Monóculo Quebrado": {
                "path": "Labyrinthus/Smrt/Krev/Znalost/Znalost",
                "sequence": "Este caminho contém uma sequência importante. Relacionado a sangue. Tem conexão com morte. Requer conhecimento.",
                "files": "Newton, Visio",
                "hint": "7 elas são",
                "tech_hint": "Os valores hexadecimais correspondem a algo visível em uma sequência específica. Analise as cores e relacione-as com os padrões exibidos."
            },
            "Garrafa Aqua Amassada": {
                "path": "Labyrinthus/Energie/Strach/Krev",
                "sequence": "Este caminho contém uma sequência importante. Relacionado a energia e medo.",
                "files": "Aqua",
                "hint": "Siga o fluxo da água",
                "tech_hint": "Examine os padrões de fluxo e as marcações nas paredes. A direção e intensidade podem indicar um caminho específico."
            },
            "Disco DEMO": {
                "path": "Labyrinthus/Znalost/Energie/Smrt",
                "sequence": "Conhecimento leva à energia e morte.",
                "files": "Demo_disc",
                "hint": "A música guia o caminho",
                "tech_hint": "As frequências sonoras podem revelar padrões ocultos. Preste atenção às variações rítmicas."
            },
            "Pote de Vidro com Algo Suspeito Dentro": {
                "path": "Labyrinthus/Strach/Krev/Energie",
                "sequence": "Medo se transforma em sangue e energia.",
                "files": "Jar_content",
                "hint": "O conteúdo revela segredos",
                "tech_hint": "Analise a composição e as reações químicas. Os elementos podem formar um padrão significativo."
            },
            "Bola Mágica 8": {
                "path": "Labyrinthus/Znalost/Smrt/Strach",
                "sequence": "Conhecimento da morte traz medo.",
                "files": "Magic_8",
                "hint": "A resposta está nas estrelas",
                "tech_hint": "Os padrões astrológicos e números podem conter mensagens codificadas."
            },
            "Vaquinha": {
                "path": "Labyrinthus/Krev/Energie/Znalost",
                "sequence": "Sangue alimenta energia e conhecimento.",
                "files": "Cow",
                "hint": "Siga os rastros",
                "tech_hint": "As pegadas e marcas no chão formam um padrão específico. Observe a direção e profundidade."
            },
            "Brinquedo Cachorro-bola": {
                "path": "Labyrinthus/Strach/Smrt/Krev",
                "sequence": "Medo da morte leva ao sangue.",
                "files": "Dog_ball",
                "hint": "Brinque com as sombras",
                "tech_hint": "As sombras projetadas podem revelar símbolos ocultos. Observe em diferentes ângulos."
            },
            "Filtro dos Sonhos": {
                "path": "Labyrinthus/Energie/Znalost/Strach",
                "sequence": "Energia do conhecimento gera medo.",
                "files": "Dreamcatcher",
                "hint": "Os sonhos mostram o caminho",
                "tech_hint": "Os padrões da teia contêm uma sequência específica. Analise a geometria e símbolos."
            },
            "Boné de Sapo": {
                "path": "Labyrinthus/Smrt/Strach/Energie",
                "sequence": "Morte e medo geram energia.",
                "files": "Frog_cap",
                "hint": "Pule entre os portais",
                "tech_hint": "A sequência de saltos forma um padrão. Observe os pontos de aterrissagem."
            },
            "Relógio de Gatinho": {
                "path": "Labyrinthus/Znalost/Krev/Smrt",
                "sequence": "Conhecimento do sangue leva à morte.",
                "files": "Cat_clock",
                "hint": "O tempo não para",
                "tech_hint": "Os números e posições dos ponteiros formam uma sequência. Analise os intervalos."
            },
            "Mantega": {
                "path": "Labyrinthus/Krev/Smrt/Energie",
                "sequence": "Sangue da morte gera energia.",
                "files": "Butter",
                "hint": "Derreta os símbolos",
                "tech_hint": "O padrão de derretimento revela mensagens ocultas. Observe a ordem e direção."
            },
            "Moeda": {
                "path": "Labyrinthus/Energie/Krev/Znalost",
                "sequence": "Energia do sangue traz conhecimento.",
                "files": "Coin",
                "hint": "Duas faces da verdade",
                "tech_hint": "As inscrições em ambos os lados formam um código. Compare e combine os símbolos."
            },
            "Baú": {
                "path": "Labyrinthus/Strach/Znalost/Smrt",
                "sequence": "Medo do conhecimento leva à morte.",
                "files": "Chest",
                "hint": "O tesouro está protegido",
                "tech_hint": "A sequência de travas forma um padrão específico. Analise a ordem de desbloqueio."
            },
            "Miniatura de Fusca Azul": {
                "path": "Labyrinthus/Smrt/Energie/Krev",
                "sequence": "Morte energizada pelo sangue.",
                "files": "Blue_beetle",
                "hint": "Siga as rodas",
                "tech_hint": "As marcas das rodas formam um caminho específico. Observe a profundidade e direção."
            },
            "PenDrive Amassado": {
                "path": "Labyrinthus/Znalost/Strach/Krev",
                "sequence": "Conhecimento do medo leva ao sangue.",
                "files": "Pendrive",
                "hint": "Os dados não mentem",
                "tech_hint": "Os arquivos corrompidos contêm padrões. Analise os bytes e sequências binárias."
            },
            "Anel de Corvo": {
                "path": "Labyrinthus/Krev/Znalost/Energie",
                "sequence": "Sangue do conhecimento gera energia.",
                "files": "Crow_ring",
                "hint": "O círculo se fecha",
                "tech_hint": "As inscrições no anel formam uma sequência circular. Observe o ponto de início."
            },
            "Bracelete Dourado": {
                "path": "Labyrinthus/Energie/Smrt/Strach",
                "sequence": "Energia da morte traz medo.",
                "files": "Golden_bracelet",
                "hint": "O brilho guia",
                "tech_hint": "Os padrões de reflexão formam símbolos específicos. Analise em diferentes intensidades de luz."
            },
            "Chave do Labirinto": {
                "path": "Labyrinthus/Strach/Energie/Znalost",
                "sequence": "Medo da energia traz conhecimento.",
                "files": "Maze_key",
                "hint": "A chave final",
                "tech_hint": "As ranhuras da chave formam um código específico. Compare com os padrões das fechaduras."
            },
            "Grimório": {
                "path": "Labyrinthus/Znalost/Krev/Strach",
                "sequence": "Conhecimento do sangue traz medo.",
                "files": "Grimoire",
                "hint": "As páginas sussurram",
                "tech_hint": "As páginas contêm padrões ocultos. Analise a ordem e símbolos em cada página."
            }
        }

        # Lista ordenada dos itens
        self.ordered_items = [
            "Crânio de Corvo",
            "Monóculo Quebrado",
            "Garrafa Aqua Amassada",
            "Disco DEMO",
            "Pote de Vidro com Algo Suspeito Dentro",
            "Bola Mágica 8",
            "Vaquinha",
            "Brinquedo Cachorro-bola",
            "Filtro dos Sonhos",
            "Boné de Sapo",
            "Relógio de Gatinho",
            "Mantega",
            "Moeda",
            "Baú",
            "Miniatura de Fusca Azul",
            "PenDrive Amassado",
            "Anel de Corvo",
            "Bracelete Dourado",
            "Chave do Labirinto",
            "Grimório"
        ]

    def decode_path(self, path):
        """Decodifica um caminho do labirinto"""
        results = []
        
        # Se não houver caminho, retorna todos os itens na ordem
        if not path:
            items_to_process = self.ordered_items
        else:
            # Se houver caminho, filtra os itens que contêm o caminho
            items_to_process = [
                item for item in self.ordered_items 
                if path.lower() in self.items[item]["path"].lower()
            ]
        
        # Processa os itens mantendo a ordem
        for i, item_name in enumerate(items_to_process, 1):
            item_data = self.items[item_name]
            result = f"""
Item {i}: {item_name}

Caminho: {item_data['path']}
Sequência: {item_data['sequence']}
Arquivos: {item_data['files']}

Dica exibida no computador: "{item_data['hint']}"

Dica Técnica:
{item_data['tech_hint']}

--------------------------------------------------
"""
            results.append(result)
        
        return "".join(results) if results else "Nenhum item encontrado para este caminho."
