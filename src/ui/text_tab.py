"""
Aba do decodificador de texto
"""

import tkinter as tk
from tkinter import ttk
from ..decoders.text_decoder import TextDecoder

class TextTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.decoder = TextDecoder()
        self.decode_type = tk.StringVar(value="braille")
        
        # Configurar estilo global das scrollbars
        style = ttk.Style()
        style.configure("Custom.Vertical.TScrollbar",
                      background="black",
                      troughcolor="black",
                      arrowcolor="#00ff00")
        style.map("Custom.Vertical.TScrollbar",
                 background=[('active', '#003300')],
                 arrowcolor=[('active', '#00ff00')])
        
        self.create_widgets()
        self.current_text = ""
        
        # Dicionário para mapear posições dos caracteres Braille clicáveis
        self.braille_positions = {}
        
        # Bind global do mousewheel para toda a janela
        self.bind_all('<MouseWheel>', self.on_mousewheel)
        
    def on_mousewheel(self, event):
        """Trata o scroll do mouse em todas as áreas de texto"""
        # Encontra o widget sob o mouse
        x, y = self.winfo_pointerxy()
        target = self.winfo_containing(x, y)
        
        # Se o target for o próprio canvas ou o frame das instruções
        if target == self.instructions or target in self.instructions.winfo_children():
            self.instructions.yview_scroll(int(-1*(event.delta/120)), "units")
        # Para outros widgets Text
        elif isinstance(target, tk.Text):
            target.yview_scroll(int(-1*(event.delta/120)), "units")
        # Para widgets dentro de frames
        else:
            # Procura pelo widget pai até encontrar um Text ou o root
            while target and not isinstance(target, tk.Text):
                if hasattr(target, 'winfo_children'):
                    for child in target.winfo_children():
                        if isinstance(child, tk.Text):
                            child.yview_scroll(int(-1*(event.delta/120)), "units")
                            return
                target = target.master
            
    def create_widgets(self):
        # Frame principal com scrollbar
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas e Scrollbar
        self.canvas = tk.Canvas(main_frame, bg='black', highlightthickness=0)
        self.main_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.main_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_scrollbar.configure(style="Custom.Vertical.TScrollbar")

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.configure(yscrollcommand=self.main_scrollbar.set)

        # Frame para conteúdo
        self.canvas_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor=tk.NW)
        
        # Frame para os radio buttons
        radio_frame = ttk.Frame(self.canvas_frame)
        radio_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Estilo para os radio buttons
        style = ttk.Style()
        style.configure('Custom.TRadiobutton',
                      background='black',
                      foreground='#00ff00',
                      selectcolor='black',
                      indicatorcolor='#00ff00')
        style.map('Custom.TRadiobutton',
                 background=[('active', '#003300'), ('selected', '#003300')],
                 foreground=[('active', '#00ff00'), ('selected', '#00ff00')])
        
        # Radio buttons
        decoders = [
            ("Braille", "braille"),
            ("ASCII", "ascii"),
            ("Base64", "base64"),
            ("Morse", "morse"),
            ("Cifra de César", "caesar"),
            ("Atbash", "atbash"),
            ("Vigenère", "vigenere"),
            ("Binário", "binary"),
            ("Hexadecimal", "hex"),
            ("ROT13", "rot13")
        ]
        
        for text, value in decoders:
            ttk.Radiobutton(radio_frame, 
                          text=text, 
                          variable=self.decode_type, 
                          value=value,
                          style='Custom.TRadiobutton',
                          command=self.update_instructions).pack(side=tk.LEFT, padx=10)

        # Área de instruções com texto clicável
        self.instructions_frame = ttk.Frame(self.canvas_frame)
        self.instructions_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        self.instructions = tk.Text(self.instructions_frame, 
                                  bg='black', 
                                  fg='#00ff00',
                                  font=('Courier', 12),
                                  wrap=tk.WORD,
                                  height=20,
                                  width=50)
        self.instructions.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.instructions.tag_configure('clickable', foreground='#00ff00', underline=True, font=('Courier', 14, 'bold'))
        self.instructions.tag_bind('clickable', '<Button-1>', self.copy_braille)

        def _on_mousewheel(event):
            self.instructions.yview_scroll(int(-1*(event.delta/120)), "units")

        # Bind do mousewheel no frame e no text widget
        self.instructions_frame.bind_all('<MouseWheel>', _on_mousewheel)

        # Configurar scrollbar preta para as instruções
        self.instructions_scrollbar = ttk.Scrollbar(self.instructions_frame, orient=tk.VERTICAL, command=self.instructions.yview)
        self.instructions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.instructions.configure(yscrollcommand=self.instructions_scrollbar.set)
        self.instructions_scrollbar.configure(style="Custom.Vertical.TScrollbar")
        
        # Frame para entrada e saída
        io_frame = ttk.Frame(self.canvas_frame)
        io_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Coluna da esquerda (entrada)
        input_frame = ttk.Frame(io_frame)
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        input_label = ttk.Label(input_frame,
                              text="Texto para decodificar:",
                              foreground='#00ff00',
                              background='black',
                              font=('Consolas', 10))
        input_label.pack(anchor=tk.W)
        
        self.input_text = tk.Text(input_frame,
                                height=10,  
                                width=40,
                                bg='black',
                                fg='#00ff00',
                                insertbackground='#00ff00',
                                font=('Consolas', 12))  
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar preta para entrada
        self.input_scrollbar = ttk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.input_text.yview)
        self.input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_text.configure(yscrollcommand=self.input_scrollbar.set)
        self.input_scrollbar.configure(style="Custom.Vertical.TScrollbar")
        
        # Botão decodificar
        decode_button = ttk.Button(io_frame,
                                 text="Decodificar",
                                 command=self.decode_text,
                                 style='Custom.TButton')
        decode_button.pack(side=tk.LEFT, padx=10)
        
        # Coluna da direita (saída)
        output_frame = ttk.Frame(io_frame)
        output_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        output_label = ttk.Label(output_frame,
                               text="Resultado:",
                               foreground='#00ff00',
                               background='black',
                               font=('Consolas', 10))
        output_label.pack(anchor=tk.W)
        
        self.output_text = tk.Text(output_frame,
                                 height=10,  
                                 width=40,
                                 bg='black',
                                 fg='#00ff00',
                                 font=('Consolas', 12))  
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar preta para saída
        self.output_scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.configure(yscrollcommand=self.output_scrollbar.set)
        self.output_scrollbar.configure(style="Custom.Vertical.TScrollbar")
        
        # Configura o scroll do canvas
        def configure_scroll(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas_frame.bind('<Configure>', configure_scroll)
        
    def copy_braille(self, event):
        """Copia o caractere Braille clicado para a área de entrada"""
        clicked_index = self.instructions.index(f"@{event.x},{event.y}")
        start = self.instructions.index(f"{clicked_index} linestart")
        line_content = self.instructions.get(start, f"{start} lineend")
        
        # Encontra o caractere Braille clicado
        pos = int(float(clicked_index.split('.')[1]))
        if pos < len(line_content):
            char = line_content[pos]
            if '⠀' <= char <= '⣿':  # Verifica se é um caractere Braille
                current_text = self.input_text.get("1.0", tk.END).strip()
                if current_text:
                    self.input_text.insert(tk.END, char)
                else:
                    self.input_text.insert("1.0", char)
                
    def update_instructions(self):
        """Atualiza as instruções baseado no tipo de decodificação selecionado"""
        self.instructions.delete("1.0", tk.END)
        if self.decode_type.get() == "braille":
            base_instructions = """INSTRUÇÕES PARA DECODIFICAÇÃO BRAILLE:

1. Clique nos caracteres Braille abaixo para adicioná-los ao texto
2. Clique em "Decodificar"

Exemplo: ⠨⠨⠓⠑⠇⠇⠕ (decodifica para "HELLO")

ALFABETO BRAILLE DE REFERÊNCIA:
Maiúsculo: """
            self.instructions.insert(tk.END, base_instructions)
            self.instructions.insert(tk.END, "⠨⠨", "clickable")
            self.instructions.insert(tk.END, "\n\n")
            
            # Letras com mais espaçamento
            letters = [
                ('a', '⠁'), ('b', '⠃'), ('c', '⠉'), ('d', '⠙'), ('e', '⠑'),
                ('f', '⠋'), ('g', '⠛'), ('h', '⠓'), ('i', '⠊'), ('j', '⠚'),
                ('k', '⠅'), ('l', '⠇'), ('m', '⠍'), ('n', '⠝'), ('o', '⠕'),
                ('p', '⠏'), ('q', '⠟'), ('r', '⠗'), ('s', '⠎'), ('t', '⠞'),
                ('u', '⠥'), ('v', '⠧'), ('w', '⠺'), ('x', '⠭'), ('y', '⠽'),
                ('z', '⠵')
            ]
            
            for i, (letter, braille) in enumerate(letters):
                if i % 5 == 0 and i > 0:
                    self.instructions.insert(tk.END, "\n")
                self.instructions.insert(tk.END, f"{braille}", "clickable")
                self.instructions.insert(tk.END, f" = {letter}        ")  
            
            # Números com mais espaçamento
            self.instructions.insert(tk.END, "\n\nNÚMEROS:\nPrefixo: ")
            self.instructions.insert(tk.END, "⠼", "clickable")
            self.instructions.insert(tk.END, "\n")
            
            numbers = [
                ('0', '⠚'), ('1', '⠁'), ('2', '⠃'), ('3', '⠉'), ('4', '⠙'),
                ('5', '⠑'), ('6', '⠋'), ('7', '⠛'), ('8', '⠓'), ('9', '⠊')
            ]
            
            for i, (number, braille) in enumerate(numbers):
                if i % 5 == 0 and i > 0:
                    self.instructions.insert(tk.END, "\n")
                self.instructions.insert(tk.END, f"{braille}", "clickable")
                self.instructions.insert(tk.END, f" = {number}        ")  
            
            # Pontuação com mais espaçamento
            self.instructions.insert(tk.END, "\n\nPONTUAÇÃO:\n")
            punctuation = [
                (',', '⠂'), ("'", '⠄'), ('.', '⠲'), ('!', '⠖'),
                ('?', '⠢'), ('-', '⠱')
            ]
            
            for i, (punct, braille) in enumerate(punctuation):
                if i % 3 == 0 and i > 0:
                    self.instructions.insert(tk.END, "\n")
                self.instructions.insert(tk.END, f"{braille}", "clickable")
                self.instructions.insert(tk.END, f" = {punct}        ")  
        
        elif self.decode_type.get() == "ascii":
            instructions = """INSTRUÇÕES PARA DECODIFICAÇÃO ASCII:

1. Cole o texto em ASCII para decodificar
2. Clique em "Decodificar"

Exemplo: 72 69 76 76 79 (decodifica para "HELLO")

Dica: Cada número representa um caractere na tabela ASCII."""
            
            self.instructions.insert(tk.END, instructions)
            
        elif self.decode_type.get() == "base64":
            instructions = """INSTRUÇÕES PARA DECODIFICAÇÃO BASE64:

1. Cole o texto em Base64 para decodificar
2. Clique em "Decodificar"

Exemplo: SGVsbG8= (decodifica para "Hello")

Dica: O texto em Base64 geralmente termina com = ou =="""
            
            self.instructions.insert(tk.END, instructions)
            
        elif self.decode_type.get() == "morse":
            instructions = """INSTRUÇÕES PARA DECODIFICAÇÃO MORSE:

1. Cole o texto em código Morse (use . para ponto e - para traço)
2. Separe as letras com espaço e as palavras com /
3. Clique em "Decodificar"

Exemplo: .... . .-.. .-.. --- / .-- --- .-. .-.. -.. (decodifica para "HELLOWORLD")

ALFABETO MORSE:
A = .-      B = -...    C = -.-.    D = -..     E = .
F = ..-.    G = --.     H = ....    I = ..      J = .---
K = -.-     L = .-..    M = --      N = -.      O = ---
P = .--.    Q = --.-    R = .-.     S = ...     T = -
U = ..-     V = ...-    W = .--     X = -..-    Y = -.--
Z = --..

NÚMEROS:
1 = .----   2 = ..---   3 = ...--   4 = ....-   5 = .....
6 = -....   7 = --...   8 = ---..   9 = ----.   0 = -----"""
            
            self.instructions.insert(tk.END, instructions)
            
        elif self.decode_type.get() == "caesar":
            instructions = """INSTRUÇÕES PARA DECODIFICAÇÃO CIFRA DE CÉSAR:

1. Cole o texto cifrado
2. Digite o deslocamento (1-25) no início do texto, seguido de :
3. Clique em "Decodificar"

Exemplo: 3:KHOOR (decodifica para "HELLO")

Dica: Se não souber o deslocamento, tente números diferentes ou deixe em branco para ver todas as possibilidades."""
            
            self.instructions.insert(tk.END, instructions)
            
        elif self.decode_type.get() == "atbash":
            instructions = """INSTRUÇÕES PARA DECODIFICAÇÃO ATBASH:

1. Cole o texto cifrado
2. Clique em "Decodificar"

A cifra Atbash substitui cada letra pela letra oposta no alfabeto:
A↔Z, B↔Y, C↔X, D↔W, E↔V, F↔U, G↔T, H↔S, I↔R, J↔Q,
K↔P, L↔O, M↔N, N↔M, O↔L, P↔K, Q↔J, R↔I, S↔H, T↔G,
U↔F, V↔E, W↔D, X↔C, Y↔B, Z↔A

Exemplo: SVOOL (decodifica para "HELLO")"""
            
            self.instructions.insert(tk.END, instructions)
            
        elif self.decode_type.get() == "vigenere":
            instructions = """INSTRUÇÕES PARA DECODIFICAÇÃO VIGENÈRE:

1. Cole o texto cifrado
2. Digite a chave no início do texto, seguida de :
3. Clique em "Decodificar"

Exemplo: KEY:RIJVS (com chave "KEY" decodifica para "HELLO")

Dica: A chave é repetida para cobrir todo o texto. Se não souber a chave,
tente palavras relacionadas ao contexto ou ao jogo."""
            
            self.instructions.insert(tk.END, instructions)
            
        elif self.decode_type.get() == "binary":
            instructions = """INSTRUÇÕES PARA DECODIFICAÇÃO BINÁRIA:

1. Cole o texto em binário (8 bits por caractere)
2. Os grupos podem ser separados por espaços
3. Clique em "Decodificar"

Exemplo: 01001000 01100101 01101100 01101100 01101111
(decodifica para "Hello")"""
            
            self.instructions.insert(tk.END, instructions)
            
        elif self.decode_type.get() == "hex":
            instructions = """INSTRUÇÕES PARA DECODIFICAÇÃO HEXADECIMAL:

1. Cole o texto em hexadecimal
2. Pode usar ou não 0x no início e espaços entre os bytes
3. Clique em "Decodificar"

Exemplos: 
48656C6C6F
0x48 0x65 0x6C 0x6C 0x6F
(ambos decodificam para "Hello")"""
            
            self.instructions.insert(tk.END, instructions)
            
        else:  # rot13
            instructions = """INSTRUÇÕES PARA DECODIFICAÇÃO ROT13:

1. Cole o texto cifrado
2. Clique em "Decodificar"

ROT13 desloca cada letra 13 posições no alfabeto:
A↔N, B↔O, C↔P, D↔Q, E↔R, F↔S, G↔T, H↔U, I↔V, J↔W,
K↔X, L↔Y, M↔Z, N↔A, O↔B, P↔C, Q↔D, R↔E, S↔F, T↔G,
U↔H, V↔I, W↔J, X↔K, Y↔L, Z↔M

Exemplo: URYYB (decodifica para "HELLO")"""
            
            self.instructions.insert(tk.END, instructions)
            
    def decode_text(self):
        """Decodifica o texto baseado no tipo selecionado"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        
        if not input_text:
            return
            
        # Limpa o campo de saída
        self.output_text.delete("1.0", tk.END)
        
        # Decodifica baseado no tipo selecionado
        decode_type = self.decode_type.get()
        
        try:
            if decode_type == "braille":
                result = self.decoder.decode_braille(input_text)
            elif decode_type == "ascii":
                result = self.decoder.decode_ascii(input_text)
            elif decode_type == "base64":
                result = self.decoder.decode_base64(input_text)
            elif decode_type == "morse":
                result = self.decoder.decode_morse(input_text)
            elif decode_type == "caesar":
                result = self.decoder.decode_caesar(input_text)
            elif decode_type == "atbash":
                result = self.decoder.decode_atbash(input_text)
            elif decode_type == "vigenere":
                result = self.decoder.decode_vigenere(input_text)
            elif decode_type == "binary":
                result = self.decoder.decode_binary(input_text)
            elif decode_type == "hex":
                result = self.decoder.decode_hex(input_text)
            else:  # rot13
                result = self.decoder.decode_rot13(input_text)
                
            # Mostra o resultado
            self.output_text.insert("1.0", result)
            
        except Exception as e:
            self.output_text.insert("1.0", f"Erro: {str(e)}")
