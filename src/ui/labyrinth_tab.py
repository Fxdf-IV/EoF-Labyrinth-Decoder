"""
Aba do decodificador do labirinto
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..decoders.labyrinth_decoder import LabyrinthDecoder
import os

class LabyrinthTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.decoder = LabyrinthDecoder()
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instruções
        instructions = """
INSTRUÇÕES DE USO:

1. Clique em "Selecionar Pasta do Labirinto" e navegue até:
   [Pasta do Jogo]/Labyrinthus

2. Selecione a pasta Labyrinthus e clique em OK

3. Clique em "Decodificar" para:
   - Analisar todos os caminhos do labirinto
   - Identificar itens e suas localizações
   - Mostrar dicas do computador
   - Fornecer dicas técnicas para ajudar na solução

4. Dicas:
   - Certifique-se de selecionar a pasta correta (Labyrinthus)
   - O processo pode demorar alguns segundos
   - Os resultados mostrarão todos os itens encontrados
"""
        
        instructions_label = ttk.Label(
            main_frame, 
            text=instructions,
            foreground='#00ff00',
            background='black',
            justify=tk.LEFT,
            font=('Consolas', 10)
        )
        instructions_label.pack(pady=10, padx=20, anchor='w')

        # Frame para botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Campo do caminho selecionado
        self.path_label = ttk.Label(
            button_frame,
            text="Nenhuma pasta selecionada",
            foreground='#00ff00',
            background='black',
            font=('Consolas', 10)
        )
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botão de seleção de pasta
        select_button = ttk.Button(
            button_frame,
            text="Selecionar Pasta do Labirinto",
            command=self.select_folder
        )
        select_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Botão de decodificar
        self.decode_button = ttk.Button(
            button_frame,
            text="Decodificar",
            command=self.decode_path,
            state='disabled'
        )
        self.decode_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Área de resultados com scroll
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar estilo da scrollbar
        style = ttk.Style()
        style.configure("Custom.Vertical.TScrollbar",
                      background="black",
                      troughcolor="black",
                      arrowcolor="#00ff00")
        style.map("Custom.Vertical.TScrollbar",
                 background=[('active', '#003300')],
                 arrowcolor=[('active', '#00ff00')])
        scrollbar.configure(style="Custom.Vertical.TScrollbar")
        
        # Text widget para resultados
        self.result_text = tk.Text(
            result_frame, 
            wrap=tk.WORD,
            bg='black',
            fg='#00ff00',
            font=('Consolas', 10),
            width=80,
            height=20
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar scroll
        scrollbar.config(command=self.result_text.yview)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # Bind do mousewheel
        def on_mousewheel(event):
            self.result_text.yview_scroll(int(-1*(event.delta/120)), "units")
        self.result_text.bind('<MouseWheel>', on_mousewheel)

    def format_result(self, results):
        """Formata os resultados da decodificação"""
        text = ""
        for i, result in enumerate(results, 1):
            text += f"\nItem {i}: {result['name']}\n\n"
            text += f"Caminho: {result['path']}\n"
            text += f"Sequência: {result['sequence']}\n"
            text += f"Arquivos: {result['files']}\n\n"
            text += f"Dica exibida no computador: {result['computer_hint']}\n\n"
            text += "Dica Técnica:\n"
            text += f"{result['technical_hint']}\n"
            text += "\n" + "="*80 + "\n"  # Separador
        return text

    def select_folder(self):
        """Abre diálogo para selecionar a pasta do labirinto"""
        folder = filedialog.askdirectory(
            title="Selecione a pasta do Labirinto",
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
        
        try:
            # Decodifica o labirinto
            results = self.decoder.decode_labyrinth(self.selected_path)
            
            # Formata e mostra os resultados
            formatted_text = self.format_result(results)
            self.result_text.insert(tk.END, formatted_text)
            
        except Exception as e:
            self.result_text.insert(tk.END, f"Erro ao decodificar o labirinto: {str(e)}")
