"""
Aba inicial com informações sobre o labirinto
"""

import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

class IntroTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(main_frame, background='black', highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configura o canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame interno para o conteúdo
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
        # Título
        title = ttk.Label(self.inner_frame, 
            text="Guia do Labirinto",
            font=('Arial', 16, 'bold'),
            foreground='#00ff00')
        title.pack(pady=10)
        
        # Traduções
        translations = ttk.Label(self.inner_frame,
            text="""
            Traduções:
            
            Krev = Sangue
            Smrt = Morte
            Znalost = Conhecimento
            Energie = Energia
            Strach = Medo
            """,
            justify=tk.LEFT,
            foreground='#00ff00')
        translations.pack(pady=10, padx=20, anchor='w')

        # Título da imagem dos itens
        items_image_title = ttk.Label(self.inner_frame,
            text="Itens do Labirinto",
            font=('Arial', 12, 'bold'),
            foreground='#00ff00')
        items_image_title.pack(pady=(20,5))

        # Imagem dos itens
        try:
            img_itens = Image.open("src/assets/images/itens.jpg")
            img_itens = ImageTk.PhotoImage(img_itens)
            itens_label = ttk.Label(self.inner_frame, image=img_itens)
            itens_label.image = img_itens
            itens_label.pack(pady=10)
        except Exception as e:
            error_label = ttk.Label(self.inner_frame,
                text="Erro ao carregar imagem dos itens",
                foreground='red')
            error_label.pack(pady=5)
        
        # Itens e Localizações
        items = ttk.Label(self.inner_frame,
            text="""
            Itens e Localizações:

            Crânio de Corvo - Subsolo
            Monóculo Quebrado - Atrás da Mansão Strach
            Garrafa Aqua Amassada - Direita da área que leva ao Cemitério
            Disco DEMO - Caminho para o topo da Colina
            Pote de Vidro com Algo Suspeito Dentro - Banheiro ao lado dos dormitórios do Castelo
            Bola Mágica 8 - Primeira área do Cemitério, ao lado da barraca do Theo
            Vaquinha - Caminho para o Mausoléu, em frente ao campinho com a carta do Calisto para o Theo
            Brinquedo Cachorro-bola - Cavernas, embaixo da área 8
            Filtro dos Sonhos - Área externa do Castelo, à direita, ao lado de um Pilar de Lodo
            Boné de Sapo - Direita do motor perpétuo
            Relógio de Gatinho - Calabouços, na sala do Yuri
            Mantega - Cozinha do Castelo
            Moeda - Jardim do Cemitério, ao lado da barraca do Beto e do Theo
            Baú - Topo da área ao sair do Subsolo
            Miniatura de Fusca Azul - Topo à esquerda da área que leva ao Cemitério, dentro de um caminhão, ao lado de uma entrada para o Castelo
            PenDrive Amassado - Embaixo da entrada da Caverna
            Anel de Corvo - Primeira área do Cemitério, antes da ponte, à direita
            Bracelete Dourado - Calabouços, na mesa engrenagem
            """,
            justify=tk.LEFT,
            foreground='#00ff00')
        items.pack(pady=10, padx=20, anchor='w')

        # Título do alfabeto
        alphabet_title = ttk.Label(self.inner_frame,
            text="Alfabeto de sigilos decodificado",
            font=('Arial', 12, 'bold'),
            foreground='#00ff00')
        alphabet_title.pack(pady=(20,5))
        
        # Alfabeto
        try:
            img_alfabeto = Image.open("src/assets/images/alfabeto.jpg")
            img_alfabeto = ImageTk.PhotoImage(img_alfabeto)
            alfabeto_label = ttk.Label(self.inner_frame, image=img_alfabeto)
            alfabeto_label.image = img_alfabeto
            alfabeto_label.pack(pady=10)
        except Exception as e:
            error_label = ttk.Label(self.inner_frame,
                text="Erro ao carregar imagem do alfabeto",
                foreground='red')
            error_label.pack(pady=5)

        # Configurações de scroll
        self.inner_frame.bind('<Configure>', self._configure_scroll_region)
        self.canvas.bind('<Configure>', self._configure_canvas)
        
        # Bind do mousewheel
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _configure_scroll_region(self, event):
        """Configura a região de scroll do canvas"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _configure_canvas(self, event):
        """Ajusta o tamanho do frame interno ao redimensionar"""
        width = event.width - 4  # 4 pixels para margem
        self.canvas.itemconfig(self.canvas_frame, width=width)
        
    def _on_mousewheel(self, event):
        """Função para scroll do mouse"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
