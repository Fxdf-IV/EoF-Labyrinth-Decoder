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
                "sequence": "Sangue, Medo, Medo, Medo",
                "files": "Cornix",
                "computer_hint": "simples como ler sigilos",
                "technical_hint": "Observe os sigilos e as inscrições que os cercam. A sequência repetitiva pode conter a chave para decifrar o significado central. Leia cuidadosamente os detalhes destacados. USE O ALFABETO."
            },
            {
                "name": "Monóculo Quebrado",
                "path_suffix": "Smrt/Krev/Znalost/Znalost",
                "sequence": "Morte, Sangue, Conhecimento, Conhecimento",
                "files": "Newton, Visio",
                "computer_hint": "7 elas são",
                "technical_hint": "Os valores hexadecimais correspondem a algo visível em uma sequência específica. Analise as cores e relacione-as com os padrões exibidos."
            },
            {
                "name": "Garrafa Aqua Amassada",
                "path_suffix": "Strach/Krev/Krev/Smrt",
                "sequence": "Medo, Sangue, Sangue, Morte",
                "files": "Aqua",
                "computer_hint": "toc toc.",
                "technical_hint": "Preste atenção nos sons emitidos. Sequências repetitivas podem formar um padrão significativo."
            },
            {
                "name": "Disco DEMO",
                "path_suffix": "Smrt/Energie/Energie/Energie",
                "sequence": "Morte, Energia, Energia, Energia",
                "files": "Demo_disc",
                "computer_hint": "Siga o padrão",
                "technical_hint": "Formas geométricas podem indicar caminhos ocultos. Examine atentamente os padrões nos círculos."
            },
            {
                "name": "Pote de Vidro com Algo Suspeito Dentro",
                "path_suffix": "Znalost/Energie/Energie/Znalost",
                "sequence": "Conhecimento, Energia, Energia, Conhecimento",
                "files": "Jar_content",
                "computer_hint": "Tátil",
                "technical_hint": "Examine o conteúdo com cuidado. O alinhamento de pequenos detalhes pode conter uma sequência importante."
            },
            {
                "name": "Bola Mágica 8",
                "path_suffix": "Krev/Znalost/Krev/Krev",
                "sequence": "Sangue, Conhecimento, Sangue, Sangue",
                "files": "Magic_8",
                "computer_hint": "a hora mais importante.",
                "technical_hint": "O tempo e os números podem revelar algo. Observe atentamente os detalhes no momento certo."
            },
            {
                "name": "Vaquinha",
                "path_suffix": "Znalost/Strach/Smrt/Smrt",
                "sequence": "Conhecimento, Medo, Morte, Morte",
                "files": "Cow",
                "computer_hint": "zero dimensões.",
                "technical_hint": "Reduza a intensidade da luz ao observar. Formas ocultas podem emergir de detalhes aparentemente simples."
            },
            {
                "name": "Brinquedo Cachorro-bola",
                "path_suffix": "Energie/Znalost/Smrt/Krev",
                "sequence": "Energia, Conhecimento, Morte, Sangue",
                "files": "Dog_ball",
                "computer_hint": "mínimo",
                "technical_hint": "Movimentos calculados podem ser a chave. Reduza o esforço ao mínimo para revelar o significado oculto."
            },
            {
                "name": "Filtro dos Sonhos",
                "path_suffix": "Krev/Smrt/Energie/Energie",
                "sequence": "Sangue, Morte, Energia, Energia",
                "files": "Dreamcatcher",
                "computer_hint": " _ ▭ x",
                "technical_hint": "Nem tudo está em primeiro plano. Experimente diferentes interações para trazer algo à tona."
            },
            {
                "name": "Boné de Sapo",
                "path_suffix": "Znalost/Strach/Strach/Krev",
                "sequence": "Conhecimento, Medo, Medo, Sangue",
                "files": "Frog_cap",
                "computer_hint": "Trace o caminho.",
                "technical_hint": "Siga as direções indicadas por sinais. Cada movimento pode desbloquear algo novo."
            },
            {
                "name": "Relógio de Gatinho",
                "path_suffix": "Krev/Smrt/Strach/Smrt",
                "sequence": "Sangue, Morte, Medo, Morte",
                "files": "Cat_clock",
                "computer_hint": "como falar com um avião.",
                "technical_hint": "Pistas visuais podem estar conectadas. Interprete sinais gráficos com base em suas posições relativas."
            },
            {
                "name": "Mantega",
                "path_suffix": "Znalost/Krev/Strach/Krev",
                "sequence": "Conhecimento, Sangue, Medo, Sangue",
                "files": "Butter",
                "computer_hint": "Porco.",
                "technical_hint": "Uma sequência não-linear pode fazer sentido. Reorganize os elementos com lógica."
            },
            {
                "name": "Moeda",
                "path_suffix": "Znalost/Znalost/Energie/Smrt",
                "sequence": "Conhecimento, Conhecimento, Energia, Morte",
                "files": "Coin",
                "computer_hint": "observe o ruído",
                "technical_hint": "Sinais audíveis ou visíveis podem ser transformados. Concentre-se em padrões discretos."
            },
            {
                "name": "Baú",
                "path_suffix": "Krev/Znalost/Smrt/Smrt",
                "sequence": "Sangue, Conhecimento, Morte, Morte",
                "files": "Chest",
                "computer_hint": "Tabula Recta",
                "technical_hint": "Métodos tradicionais podem ajudar. Descubra como diferentes elementos se interligam."
            },
            {
                "name": "Miniatura de Fusca Azul",
                "path_suffix": "Smrt/Znalost/Smrt/Smrt",
                "sequence": "Morte, Conhecimento, Morte, Morte",
                "files": "Blue_beetle",
                "computer_hint": "Ouro.",
                "technical_hint": "Pistas históricas ou culturais podem ser úteis. Explore a ligação entre referências e significados ocultos."
            },
            {
                "name": "PenDrive Amassado",
                "path_suffix": "Znalost/Smrt/Energie/Strach",
                "sequence": "Conhecimento, Morte, Energia, Medo",
                "files": "Pendrive",
                "computer_hint": "conecta-as.",
                "technical_hint": "Partes separadas podem se unir. Conecte as informações dispersas para formar algo coeso."
            },
            {
                "name": "Anel de Corvo",
                "path_suffix": "Krev/Znalost/Energie/Energie",
                "sequence": "Sangue, Conhecimento, Energia, Energia",
                "files": "Crow_ring",
                "computer_hint": "1507580",
                "technical_hint": "A busca por pistas pode levá-lo além do jogo. Investigue todas as possibilidades ao seu redor."
            },
            {
                "name": "Fita K7",
                "path_suffix": "Znalost/Smrt/Strach/Strach",
                "sequence": "Conhecimento, Morte, Medo, Medo",
                "files": "K7",
                "computer_hint": "2 etapas.",
                "technical_hint": "Camadas de áudio podem conter segredos. Ajuste o ritmo ou explore outras formas de interpretação para decifrá-las."
            },
            {
                "name": "Bracelete Dourado",
                "path_suffix": "Smrt/Energie/Strach/Krev",
                "sequence": "Morte, Energia, Medo, Sangue",
                "files": "Golden_bracelet",
                "computer_hint": "leia as fórmulas.",
                "technical_hint": "As formas das fórmulas podem esconder algo essencial. Examine cada elemento para encontrar conexões inesperadas."
            },
            {
                "name": "D20",
                "path_suffix": "Znalost/Krev/Strach/Krev",
                "sequence": "Conhecimento, Sangue, Medo, Sangue",
                "files": "D20",
                "computer_hint": "Menu.",
                "technical_hint": "O caminho é a resposta",
                "image_path": os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "resources", "images", "sigilo_d20.jpg")
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
            
            # Se o item tem uma imagem, adiciona o caminho da imagem
            if "image_path" in item:
                result["image_path"] = item["image_path"]
            
            results.append({
                "name": result["name"],
                "path": result["path"],
                "sequence": result["sequence"],
                "files": result["files"],
                "computer_hint": result["computer_hint"],
                "technical_hint": result["technical_hint"],
                "image_path": result.get("image_path", None)
            })
        
        return results
