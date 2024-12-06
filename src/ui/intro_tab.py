"""
Aba inicial com informações sobre o labirinto
"""

import tkinter as tk
from tkinter import ttk
import os
import sys
from PIL import Image, ImageTk
from pathlib import Path

def get_asset_path():
    """Retorna o caminho correto para a pasta assets, seja em desenvolvimento ou no executável"""
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como executável
        base_path = Path(sys._MEIPASS)
        return base_path / "assets"
    else:
        # Se estiver em desenvolvimento
        return Path(__file__).parent.parent / "assets"

class IntroTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.assets_path = get_asset_path()
        
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
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(main_frame, background='black', highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview, style="Custom.Vertical.TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configura o canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame interno para o conteúdo
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
        # Bind do mousewheel diretamente no canvas e no frame principal
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        main_frame.bind("<MouseWheel>", _on_mousewheel)
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        self.inner_frame.bind("<MouseWheel>", _on_mousewheel)
        
        # Atualiza a região de scroll quando o conteúdo muda
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
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
            img_path = self.assets_path / "images" / "itens.jpg"
            img_itens = Image.open(str(img_path))
            img_itens = ImageTk.PhotoImage(img_itens)
            itens_label = ttk.Label(self.inner_frame, image=img_itens)
            itens_label.image = img_itens
            itens_label.pack(pady=10)
        except Exception as e:
            error_label = ttk.Label(self.inner_frame,
                text=f"Erro ao carregar imagem dos itens: {str(e)}",
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
            img_path = self.assets_path / "images" / "alfabeto.jpg"
            img_alfabeto = Image.open(str(img_path))
            img_alfabeto = ImageTk.PhotoImage(img_alfabeto)
            alfabeto_label = ttk.Label(self.inner_frame, image=img_alfabeto)
            alfabeto_label.image = img_alfabeto
            alfabeto_label.pack(pady=10)
        except Exception as e:
            error_label = ttk.Label(self.inner_frame,
                text=f"Erro ao carregar imagem do alfabeto: {str(e)}",
                foreground='red')
            error_label.pack(pady=5)
