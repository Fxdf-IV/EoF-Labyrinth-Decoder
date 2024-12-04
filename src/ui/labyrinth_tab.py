"""
Aba do decodificador do labirinto
"""

import tkinter as tk
from tkinter import ttk, filedialog
from ..decoders.labyrinth_decoder import LabyrinthDecoder

class LabyrinthTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.decoder = LabyrinthDecoder()
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instruções
        instructions = """
INSTRUÇÕES DE USO:

1. Clique em "Selecionar Pasta do Labirinto" e navegue até:
   [Pasta do Jogo]/Labyrinthus

2. Selecione a pasta Labyrinthus e clique em OK

3. O decodificador irá:
   - Analisar todos os caminhos do labirinto
   - Identificar itens e suas localizações
   - Mostrar dicas do computador
   - Fornecer dicas técnicas para ajudar na solução

4. Dicas:
   - Certifique-se de selecionar a pasta correta (Labyrinthus)
   - O processo pode demorar alguns segundos
   - Os resultados mostrarão todos os itens encontrados
"""
        
        instructions_label = ttk.Label(main_frame, 
                                     text=instructions,
                                     foreground='#00ff00',
                                     justify=tk.LEFT,
                                     font=('Consolas', 10))
        instructions_label.pack(pady=10, padx=20, anchor='w')

        # Frame para botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Campo do caminho selecionado
        self.path_label = ttk.Label(button_frame,
                                  text="Nenhuma pasta selecionada",
                                  foreground='#00ff00',
                                  font=('Consolas', 10))
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botão de seleção de pasta
        select_button = ttk.Button(button_frame,
                                 text="Selecionar Pasta do Labirinto",
                                 command=self.select_folder)
        select_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Botão de decodificar
        self.decode_button = ttk.Button(button_frame,
                                      text="Decodificar",
                                      command=self.decode_path,
                                      state='disabled')
        self.decode_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Área de resultados com scroll
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget para resultados
        self.result_text = tk.Text(result_frame, 
                                 wrap=tk.WORD, 
                                 width=50, 
                                 height=20,
                                 background='black',
                                 foreground='#00ff00',
                                 font=('Consolas', 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Configura scrollbar
        scrollbar.config(command=self.result_text.yview)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
    def select_folder(self):
        """Abre diálogo para selecionar a pasta do labirinto"""
        folder = filedialog.askdirectory(
            title="Selecione a pasta Labyrinthus",
            initialdir="C:/Program Files (x86)/Steam/steamapps/common/Enigma of Fear"
        )
        if folder:
            if folder.endswith("Labyrinthus"):
                self.selected_path = folder
                self.path_label.config(text=folder)
                self.decode_button.config(state='normal')
            else:
                self.result_text.delete('1.0', tk.END)
                self.result_text.insert('1.0', "ERRO: Por favor, selecione a pasta 'Labyrinthus' dentro da pasta do jogo.")
                self.decode_button.config(state='disabled')
                
    def decode_path(self):
        """Decodifica todos os caminhos do labirinto"""
        if not hasattr(self, 'selected_path'):
            return
            
        # Limpa resultados anteriores
        self.result_text.delete('1.0', tk.END)
        
        # Lista todos os caminhos conhecidos
        all_results = []
        
        # Decodifica todos os caminhos de uma vez
        result = self.decoder.decode_path("")  # Passa string vazia para retornar todos os itens
        
        # Mostra resultados
        if result and "Nenhum item encontrado" not in result:
            self.result_text.insert('1.0', result)
        else:
            self.result_text.insert('1.0', "Nenhum item encontrado nos caminhos do labirinto.")
