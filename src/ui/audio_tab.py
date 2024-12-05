"""
Aba do decodificador de áudio
"""

import tkinter as tk
from tkinter import ttk, filedialog
import pygame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import soundfile as sf
import numpy as np

from src.config import UI_CONFIG
from src.decoders.audio_decoder import AudioDecoder

class AudioDecoderTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.decoder = AudioDecoder()
        
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
        """Configura a interface da aba"""
        # Frame de instruções
        instructions = ttk.Label(self,
            text="Decodificador de Áudio\n\n" +
                 "Funcionalidades:\n" +
                 "- Análise de espectrograma\n" +
                 "- Análise de frequências\n" +
                 "- Análise de amplitude",
            justify=tk.LEFT,
            style='TLabel')
        instructions.pack(pady=10, padx=10, anchor=tk.W)
        
        # Frame de controles
        controls = ttk.Frame(self)
        controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(controls,
            text="Carregar Áudio",
            command=self.load_audio,
            style='TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls,
            text="Reproduzir Áudio",
            command=self.play_audio,
            style='TButton').pack(side=tk.LEFT, padx=5)
        
        # Botão para pausar/retomar áudio
        self.play_pause_button = ttk.Button(controls,
            text="Pausar",
            command=self.toggle_play_pause,
            style='TButton')
        self.play_pause_button.pack(side=tk.LEFT, padx=5)
        
        # Frame para visualização
        self.audio_frame = ttk.Frame(self)
        self.audio_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Área de resultados
        text_frame = ttk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, style="Custom.Vertical.TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto para resultados
        self.result_text = tk.Text(text_frame,
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
        
    def load_audio(self):
        """Carrega e analisa um arquivo de áudio"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Áudio",
            filetypes=[
                ("Arquivos de áudio", "*.wav *.mp3 *.ogg *.flac"),
                ("Todos os arquivos", "*.*")
            ])

        if file_path:
            try:
                # Limpar visualização anterior
                for widget in self.audio_frame.winfo_children():
                    widget.destroy()

                # Processar o áudio
                self.file_path = file_path  # Armazena o caminho do arquivo para reprodução
                audio_data, sample_rate = sf.read(file_path)
                if len(audio_data.shape) > 1:
                    audio_data = np.mean(audio_data, axis=1)

                # Plotar espectro de frequências completo
                self.plot_fixed_spectrum(audio_data)

                # Mostrar resultados
                results = self.decoder.analyze_audio(file_path)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Resultados da análise de áudio:\n\n")
                for key, value in results.items():
                    self.result_text.insert(tk.END, f"{key}: {value}\n")

            except Exception as e:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Erro ao processar áudio: {str(e)}")

    def plot_fixed_spectrum(self, audio_data):
        """Plota o espectro de frequências fixo"""
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='black')
        ax = fig.add_subplot(111, facecolor='black')
        ax.plot(audio_data, color='#00ff00')
        ax.set_title('Espectro de Frequências', color='#00ff00')
        ax.set_xlabel('Tempo', color='#00ff00')
        ax.set_ylabel('Amplitude', color='#00ff00')
        ax.tick_params(axis='x', colors='#00ff00')
        ax.tick_params(axis='y', colors='#00ff00')

        # Adicionar gráfico ao frame
        canvas = FigureCanvasTkAgg(fig, master=self.audio_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def play_audio(self):
        """Reproduz o áudio carregado sem atualizar o espectro"""
        if hasattr(self, 'file_path'):
            pygame.mixer.init()
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.play()

    def toggle_play_pause(self):
        """Alterna entre pausar e retomar a reprodução do áudio"""
        if pygame.mixer.music.get_busy():
            if self.play_pause_button.config('text')[-1] == 'Pausar':
                pygame.mixer.music.pause()
                self.play_pause_button.config(text='Retomar')
            else:
                pygame.mixer.music.unpause()
                self.play_pause_button.config(text='Pausar')

    def plot_frequencies(self, frequencies):
        """Plota o espectro de frequências estático"""
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='black')
        ax = fig.add_subplot(111, facecolor='black')
        ax.bar(range(len(frequencies)), frequencies, color='#00ff00')
        ax.set_title('Espectro de Frequências', color='#00ff00')
        ax.set_xlabel('Frequência (Hz)', color='#00ff00')
        ax.set_ylabel('Magnitude', color='#00ff00')
        ax.tick_params(axis='x', colors='#00ff00')
        ax.tick_params(axis='y', colors='#00ff00')

        # Limpar gráficos anteriores
        for widget in self.audio_frame.winfo_children():
            widget.destroy()

        # Adicionar gráfico ao frame
        canvas = FigureCanvasTkAgg(fig, master=self.audio_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_spectrum(self):
        """Atualiza o espectro de frequências durante a reprodução do áudio"""
        if not hasattr(self, 'file_path'):
            return

        # Carregar áudio
        audio_data, sample_rate = sf.read(self.file_path)

        # Converter para mono se estéreo
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        # Atualizar gráfico
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='black')
        ax = fig.add_subplot(111, facecolor='black')
        ax.plot(audio_data[:int(sample_rate * 0.1)], color='#00ff00')  # Mostrar apenas uma parte do áudio
        ax.set_xlim(0, int(sample_rate * 0.1))  # Manter o limite fixo
        ax.set_ylim(-1, 1)  # Normalizar amplitude
        ax.set_title('Espectro de Frequências', color='#00ff00')
        ax.set_xlabel('Tempo', color='#00ff00')
        ax.set_ylabel('Amplitude', color='#00ff00')
        ax.tick_params(axis='x', colors='#00ff00')
        ax.tick_params(axis='y', colors='#00ff00')

        # Limpar gráficos anteriores
        for widget in self.audio_frame.winfo_children():
            widget.pack_forget()

        # Adicionar gráfico ao frame
        canvas = FigureCanvasTkAgg(fig, master=self.audio_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Atualizar a cada 100 ms
        self.after(100, self.update_spectrum)

        # Smooth out the transitions
        self.audio_frame.update_idletasks()
        self.audio_frame.update()
