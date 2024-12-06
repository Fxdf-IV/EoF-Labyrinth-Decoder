"""
Aba do decodificador do labirinto
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from decoders.labyrinth_decoder import LabyrinthDecoder

class LabyrinthTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.decoder = LabyrinthDecoder()
        
        # Configurar estilo global das scrollbars
        style = ttk.Style()
        style.configure("Custom.Vertical.TScrollbar",
                      background="black",
                      troughcolor="black",
                      arrowcolor="#00ff00")
        style.map("Custom.Vertical.TScrollbar",
                 background=[('active', '#003300')],
                 arrowcolor=[('active', '#00ff00')])
        
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
        
        # Área de resultados com scrollbar
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(result_frame, style="Custom.Vertical.TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto para resultados
        self.result_text = tk.Text(result_frame, 
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            background='black',
            foreground='#00ff00',
            insertbackground='#00ff00',
            selectbackground='#003300',
            selectforeground='#00ff00',
            height=20)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.result_text.yview)
        
        # Bind do mousewheel
        def on_mousewheel(event):
            self.result_text.yview_scroll(int(-1*(event.delta/120)), "units")
        self.result_text.bind('<MouseWheel>', on_mousewheel)

    def format_result(self, results):
        """Formata os resultados da decodificação"""
        text = ""
        for i, result in enumerate(results, 1):
            text += f"\nItem {i}: {result['name']}\n\n"
            
            # Se for o D20, tenta mostrar a imagem no caminho
            if result['name'] == "D20":
                if result.get('image_path'):
                    try:
                        # Insere o início do texto
                        self.result_text.insert(tk.END, text + "Caminho: ")
                        text = ""  # Limpa o texto para continuar depois
                        
                        # Carrega e redimensiona a imagem mantendo a proporção
                        image = Image.open(result['image_path'])
                        # Pega as dimensões originais
                        width, height = image.size
                        # Calcula a proporção
                        aspect_ratio = width / height
                        # Define a altura desejada
                        target_height = 50  # pixels
                        # Calcula a largura proporcional
                        target_width = int(target_height * aspect_ratio)
                        # Redimensiona mantendo a proporção
                        image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                        
                        # Converte a imagem para PhotoImage
                        photo = ImageTk.PhotoImage(image)
                        
                        # Guarda referência da imagem para não ser coletada pelo garbage collector
                        if not hasattr(self, 'images'):
                            self.images = []
                        self.images.append(photo)
                        
                        # Insere a imagem
                        self.result_text.image_create(tk.END, image=photo)
                        text += "\n"  # Quebra de linha após a imagem
                    except Exception as e:
                        text += f"Caminho: Erro ao carregar imagem: {str(e)}\n"
                else:
                    text += f"Caminho: {result['path']}\n"
            else:
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
            self.results = self.decoder.decode_labyrinth(self.selected_path)
            
            # Inicia a animação de digitação
            self.current_item = 0
            self.current_char = 0
            self.type_next_character()
            
        except Exception as e:
            self.result_text.insert(tk.END, f"Erro ao decodificar o labirinto: {str(e)}")

    def type_next_character(self):
        """Digita o próximo caractere com efeito de digitação"""
        if self.current_item >= len(self.results):
            return
            
        result = self.results[self.current_item]
        
        # Formata o texto do item atual
        if self.current_char == 0:
            self.current_text = f"\nItem {self.current_item + 1}: {result['name']}\n\n"
            if result['name'] == "D20":
                self.current_text += "Caminho: "
                # Após inserir o texto inicial, insere a imagem
                self.result_text.insert(tk.END, self.current_text)
                self.current_text = ""
                try:
                    # Carrega e redimensiona a imagem mantendo a proporção
                    image = Image.open(result['image_path'])
                    width, height = image.size
                    aspect_ratio = width / height
                    target_height = 50
                    target_width = int(target_height * aspect_ratio)
                    image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    if not hasattr(self, 'images'):
                        self.images = []
                    self.images.append(photo)
                    self.result_text.image_create(tk.END, image=photo)
                    self.current_text = "\n"
                except Exception as e:
                    self.current_text += f"Erro ao carregar imagem: {str(e)}\n"
            else:
                self.current_text += f"Caminho: {result['path']}\n"
            self.current_text += f"Sequência: {result['sequence']}\n"
            self.current_text += f"Arquivos: {result['files']}\n\n"
            self.current_text += f"Dica exibida no computador: {result['computer_hint']}\n\n"
            self.current_text += "Dica Técnica:\n"
            self.current_text += f"{result['technical_hint']}\n"
            self.current_text += "\n" + "="*80 + "\n"
        
        # Insere o próximo caractere
        if self.current_char < len(self.current_text):
            self.result_text.insert(tk.END, self.current_text[self.current_char])
            self.current_char += 1
            self.result_text.see(tk.END)  # Rola automaticamente para o final
            # Velocidade de digitação - 5x mais rápido (2ms entre caracteres)
            self.after(2, self.type_next_character)
        else:
            # Passa para o próximo item
            self.current_item += 1
            self.current_char = 0
            if self.current_item < len(self.results):
                self.after(10, self.type_next_character)  # Pausa entre itens também 5x mais rápida
