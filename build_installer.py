import PyInstaller.__main__
import os

# Dependências
# build_exe_options = {
#     "packages": ["os", "tkinter"],
#     "excludes": [],
#     "include_files": ["README.md"]
# }

# Configuração do executável
PyInstaller.__main__.run([
    'maze_solver.py',
    '--name=EoFLabyrinthDecoder',
    '--onefile',
    '--windowed',
    '--clean',
    '--add-data=README.md;.',
    f'--icon={os.path.join(os.getcwd(), "icon.ico")}' if os.path.exists('icon.ico') else '',
])
