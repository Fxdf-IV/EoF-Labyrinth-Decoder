"""
Decodificador para analisar arquivos do labirinto
"""

import os
import logging
from typing import List, Dict, Optional

class LabyrinthDecoder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Mapeamento de itens e suas informações
        self.items_info = {
            'cranio_corvo': {
                'name': 'Crânio de Corvo',
                'sequence': ['KREV', 'STRACH', 'STRACH', 'STRACH'],
                'files': ['Cornix'],
                'computer_hint': 'Percorra o labirinto',
                'technical_hint': 'Observe os sigilos e as inscrições que os cercam. A sequência repetitiva pode conter a chave para decifrar o significado central. Leia cuidadosamente os detalhes destacados. USE O ALFABETO'
            },
            'monoculo': {
                'name': 'Monóculo Quebrado',
                'sequence': ['SMRT', 'KREV', 'ZNALOST', 'ZNALOST'],
                'files': ['Newton', 'Visio'],
                'computer_hint': '7 elas são',
                'technical_hint': 'Os valores hexadecimais correspondem a algo visível em uma sequência específica. Analise as cores e relacione-as com os padrões exibidos.'
            }
            # Outros itens serão adicionados conforme o guia
        }
        
    def explore_paths(self, base_path: str) -> Dict[str, List[str]]:
        """Explora os caminhos do labirinto e retorna os itens encontrados"""
        results = {
            'items': [],      # Lista de itens encontrados
            'paths': [],      # Caminhos completos
            'sequences': [],  # Sequências importantes
            'files': [],     # Arquivos encontrados
            'computer_hints': [], # Dicas do computador
            'technical_hints': [] # Dicas técnicas
        }
        
        try:
            item_count = 0
            for item_key, item_info in self.items_info.items():
                current_path = base_path
                valid_path = True
                sequence = item_info['sequence']
                
                # Segue a sequência de pastas
                for folder in sequence:
                    found = False
                    try:
                        for item in os.listdir(current_path):
                            item_path = os.path.join(current_path, item)
                            if os.path.isdir(item_path) and folder in item.upper():
                                current_path = item_path
                                found = True
                                break
                    except Exception as e:
                        self.logger.error(f"Erro ao listar diretório {current_path}: {str(e)}")
                        valid_path = False
                        break
                        
                    if not found:
                        valid_path = False
                        break
                
                if valid_path:
                    item_count += 1
                    # Adiciona informações do item
                    results['items'].append(f"Item {item_count}: {item_info['name']}")
                    results['paths'].append(f"Caminho: {current_path}")
                    
                    # Gera a sequência
                    sequence_hint = "Este caminho contém uma sequência importante."
                    if 'KREV' in sequence: sequence_hint += " Relacionado a sangue."
                    if 'SMRT' in sequence: sequence_hint += " Tem conexão com morte."
                    if 'STRACH' in sequence: sequence_hint += " Envolve medo."
                    if 'ZNALOST' in sequence: sequence_hint += " Requer conhecimento."
                    if 'ENERGIE' in sequence: sequence_hint += " Energia é importante."
                    results['sequences'].append(f"Sequência: {sequence_hint}")
                    
                    # Adiciona arquivos e dicas
                    results['files'].append(f"Arquivos: {', '.join(item_info['files'])}")
                    results['computer_hints'].append(f"Dica exibida no computador: \"{item_info['computer_hint']}\"")
                    results['technical_hints'].append(f"Dica Técnica:\n{item_info['technical_hint']}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Erro ao explorar diretório {base_path}: {str(e)}")
            return {k: [] for k in results.keys()}
