import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from threading import Thread

class MazeSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EoF Labyrinth Decoder")
        self.root.geometry("600x400")
        
        # Criar frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Campo de caminho
        self.path_var = tk.StringVar()
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(path_frame, text="Caminho para Labyrinthus:").pack(side=tk.LEFT)
        ttk.Entry(path_frame, textvariable=self.path_var, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(path_frame, text="Procurar", command=self.browse_path).pack(side=tk.LEFT)
        
        # Área de log
        self.log_area = scrolledtext.ScrolledText(main_frame, height=15, width=70)
        self.log_area.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, mode='determinate', variable=self.progress_var)
        self.progress.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Botão de iniciar
        self.start_button = ttk.Button(main_frame, text="Iniciar Exploração", command=self.start_exploration)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Configurar expansão da janela
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def browse_path(self):
        path = filedialog.askdirectory(title="Selecione a pasta Labyrinthus")
        if path:
            if "Labyrinthus" in path:
                self.path_var.set(path)
            else:
                messagebox.showwarning("Aviso", "Por favor, selecione a pasta Labyrinthus!")

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
    
    def start_exploration(self):
        path = self.path_var.get()
        if not path:
            messagebox.showwarning("Aviso", "Por favor, selecione um caminho válido!")
            return
        if "Labyrinthus" not in path:
            messagebox.showwarning("Aviso", "Por favor, selecione a pasta Labyrinthus!")
            return

        self.log_area.delete(1.0, tk.END)
        self.start_button.state(['disabled'])
        self.progress_var.set(0)
        self.progress.configure(mode='determinate')
        
        Thread(target=self.run_exploration, daemon=True).start()
    
    def run_exploration(self):
        base_path = self.path_var.get()
        
        def custom_print(message):
            self.root.after(0, self.log, message)

        def update_progress(value):
            self.root.after(0, self.progress_var.set, value)
        
        try:
            results = explore_maze(base_path, print_func=custom_print, progress_callback=update_progress)
            if results:
                custom_print("\nCaminhos encontrados:")
                for i, result in enumerate(results, 1):
                    relative_path = os.path.relpath(result['full_path'], base_path)
                    custom_print(f"\n{i}. {relative_path}")
            else:
                custom_print("\nNenhum caminho válido encontrado.")
        except Exception as e:
            custom_print(f"\nErro durante a exploração: {str(e)}")
        
        self.root.after(0, self.finish_exploration)
    
    def finish_exploration(self):
        self.progress.stop()
        self.start_button.state(['!disabled'])

def explore_maze(base_path, current_path=None, visited_paths=None, depth=0, max_depth=10, print_func=print, progress_callback=None):
    if current_path is None:
        current_path = []
    if visited_paths is None:
        visited_paths = set()
        
    if not os.path.exists(base_path):
        print_func(f"Erro: O diretório '{base_path}' não existe!")
        return []

    current_path_str = '/'.join(current_path)
    
    if current_path_str in visited_paths or depth > max_depth:
        return []
    
    visited_paths.add(current_path_str)
    full_path = os.path.join(base_path, *current_path)
    
    valid_paths = []
    try:
        contents = os.listdir(full_path)
        total_items = len(contents)
        
        for i, item in enumerate(contents):
            if progress_callback:
                progress_callback((i / total_items) * 100)
                
            item_path = os.path.join(full_path, item)
            if not os.path.isdir(item_path) and "uh-oh" not in item.lower():
                valid_paths.append({
                    'path': '/'.join(current_path),
                    'file': item,
                    'full_path': item_path
                })

            if os.path.isdir(item_path):
                new_path = current_path + [item]
                sub_paths = explore_maze(base_path, new_path, visited_paths, depth + 1, max_depth, print_func, progress_callback)
                valid_paths.extend(sub_paths)
                
    except PermissionError:
        print_func(f"Erro de permissão ao acessar: {full_path}")
    except Exception as e:
        print_func(f"Erro ao explorar {full_path}: {e}")
    
    if progress_callback:
        progress_callback(100)
    
    return valid_paths

def main():
    root = tk.Tk()
    app = MazeSolverGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
