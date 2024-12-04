"""
Decodificador do labirinto
"""

import logging
from typing import Dict, Any

class LabyrinthDecoder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Dicionário com as dicas do labirinto
        self.hints = {
            "Crânio de Corvo": {
                "computer_hint": "simples como ler sigilos",
                "technical_hint": "Observe os sigilos e as inscrições que os cercam. A sequência repetitiva pode conter a chave para decifrar o significado central. Leia cuidadosamente os detalhes destacados. USE O ALFABETO."
            },
            "Monóculo Quebrado": {
                "computer_hint": "7 elas são",
                "technical_hint": "Os valores hexadecimais correspondem a algo visível em uma sequência específica. Analise as cores e relacione-as com os padrões exibidos."
            },
            "Garrafa Aqua Amassada": {
                "computer_hint": "toc toc.",
                "technical_hint": "Preste atenção nos sons emitidos. Sequências repetitivas podem formar um padrão significativo."
            },
            "Disco DEMO": {
                "computer_hint": "Siga o padrão",
                "technical_hint": "Formas geométricas podem indicar caminhos ocultos. Examine atentamente os padrões nos círculos."
            },
            "Pote de Vidro com Algo Suspeito Dentro": {
                "computer_hint": "Tátil",
                "technical_hint": "Examine o conteúdo com cuidado. O alinhamento de pequenos detalhes pode conter uma sequência importante."
            },
            "Bola Mágica 8": {
                "computer_hint": "a hora mais importante.",
                "technical_hint": "O tempo e os números podem revelar algo. Observe atentamente os detalhes no momento certo."
            },
            "Vaquinha": {
                "computer_hint": "zero dimensões.",
                "technical_hint": "Reduza a intensidade da luz ao observar. Formas ocultas podem emergir de detalhes aparentemente simples."
            },
            "Brinquedo Cachorro-bola": {
                "computer_hint": "mínimo",
                "technical_hint": "Movimentos calculados podem ser a chave. Reduza o esforço ao mínimo para revelar o significado oculto."
            },
            "Filtro dos Sonhos": {
                "computer_hint": " _ ▭ x",
                "technical_hint": "Nem tudo está em primeiro plano. Experimente diferentes interações para trazer algo à tona."
            },
            "Boné de Sapo": {
                "computer_hint": "Trace o caminho.",
                "technical_hint": "Siga as direções indicadas por sinais. Cada movimento pode desbloquear algo novo."
            },
            "Relógio de Gatinho": {
                "computer_hint": "como falar com um avião.",
                "technical_hint": "Pistas visuais podem estar conectadas. Interprete sinais gráficos com base em suas posições relativas."
            },
            "Mantega": {
                "computer_hint": "Porco.",
                "technical_hint": "Uma sequência não-linear pode fazer sentido. Reorganize os elementos com lógica."
            },
            "Moeda": {
                "computer_hint": "observe o ruído",
                "technical_hint": "Sinais audíveis ou visíveis podem ser transformados. Concentre-se em padrões discretos."
            },
            "Baú": {
                "computer_hint": "Tabula Recta",
                "technical_hint": "Métodos tradicionais podem ajudar. Descubra como diferentes elementos se interligam."
            },
            "Miniatura de Fusca Azul": {
                "computer_hint": "Ouro.",
                "technical_hint": "Pistas históricas ou culturais podem ser úteis. Explore a ligação entre referências e significados ocultos."
            },
            "PenDrive Amassado": {
                "computer_hint": "conecta-as.",
                "technical_hint": "Partes separadas podem se unir. Conecte as informações dispersas para formar algo coeso."
            },
            "Anel de Corvo": {
                "computer_hint": "1507580",
                "technical_hint": "A busca por pistas pode levá-lo além do jogo. Investigue todas as possibilidades ao seu redor."
            },
            "Bracelete Dourado": {
                "computer_hint": "leia as fórmulas.",
                "technical_hint": "As formas das fórmulas podem esconder algo essencial. Examine cada elemento para encontrar conexões inesperadas."
            },
            "Fita K7": {
                "computer_hint": "2 etapas.",
                "technical_hint": "Camadas de áudio podem conter segredos. Ajuste o ritmo ou explore outras formas de interpretação para decifrá-las."
            },
            "D20": {
                "computer_hint": "Menu.",
                "technical_hint": "Padrões numéricos e conexões entre eles podem revelar algo único. Procure pelo inesperado em objetos geométricos."
            }
        }

    def get_hint(self, item_name: str) -> Dict[str, str]:
        """
        Retorna as dicas para um item específico
        """
        try:
            if item_name in self.hints:
                return self.hints[item_name]
            else:
                return {
                    "computer_hint": "Item não encontrado",
                    "technical_hint": "Item não encontrado no banco de dados"
                }
        except Exception as e:
            self.logger.error(f"Erro ao buscar dica: {str(e)}")
            return {
                "computer_hint": "Erro ao buscar dica",
                "technical_hint": "Ocorreu um erro ao buscar a dica"
            }

    def list_items(self) -> list:
        """
        Retorna a lista de todos os itens disponíveis
        """
        return list(self.hints.keys())
