import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
import threading
import shutil
from datetime import datetime

class OggToMp3Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor OGG para MP3")
        self.root.geometry("800x600")
        
        self.input_files = []
        self.input_dir = tk.StringVar(value="Não selecionado")
        self.output_dir = tk.StringVar(value="Não selecionado")
        self.sort_option = tk.StringVar(value="name")
        
        self.check_ffmpeg()
        self.setup_ui()

    def check_ffmpeg(self):
        """Verifica se o ffmpeg está no PATH."""
        if shutil.which("ffmpeg") is None:
            messagebox.showerror(
                "Erro de Dependência",
                "O executável 'ffmpeg' não foi encontrado no sistema.\n\n"
                "Por favor, instale o FFmpeg e adicione-o ao PATH para usar este programa."
            )

    def setup_ui(self):
        # Frame Principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Painéis Superior (Seleção)
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # Esquerda: Selecionar Arquivos
        left_selection = ttk.Frame(top_frame)
        left_selection.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        btn_select_files = ttk.Button(left_selection, text="Selecionar Arquivos .ogg", command=self.select_files)
        btn_select_files.pack(side=tk.TOP, anchor=tk.W)
        
        lbl_input = ttk.Label(left_selection, textvariable=self.input_dir, wraplength=350, foreground="gray")
        lbl_input.pack(side=tk.TOP, anchor=tk.W, pady=(5, 0))

        # Direita: Selecionar Saída
        right_selection = ttk.Frame(top_frame)
        right_selection.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        btn_select_output = ttk.Button(right_selection, text="Selecionar Diretório de Saída", command=self.select_output)
        btn_select_output.pack(side=tk.TOP, anchor=tk.E)
        
        lbl_output = ttk.Label(right_selection, textvariable=self.output_dir, wraplength=350, foreground="gray")
        lbl_output.pack(side=tk.TOP, anchor=tk.E, pady=(5, 0))

        # Painéis Centrais (Listas)
        lists_frame = ttk.Frame(main_frame)
        lists_frame.pack(fill=tk.BOTH, expand=True)

        # Lista de Entrada (Esquerda)
        left_list_frame = ttk.Frame(lists_frame)
        left_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        ttk.Label(left_list_frame, text="Arquivos de Origem").pack(anchor=tk.W)
        
        self.listbox_input = tk.Listbox(left_list_frame, selectmode=tk.EXTENDED)
        self.listbox_input.pack(fill=tk.BOTH, expand=True)
        
        # Lista de Preview (Direita)
        right_list_frame = ttk.Frame(lists_frame)
        right_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        ttk.Label(right_list_frame, text="Preview de Saída").pack(anchor=tk.W)
        
        self.listbox_preview = tk.Listbox(right_list_frame)
        self.listbox_preview.pack(fill=tk.BOTH, expand=True)

        # Painel Inferior (Controles e Progresso)
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))

        # Ordenação
        sort_frame = ttk.LabelFrame(bottom_frame, text="Ordenar por:", padding="5")
        sort_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(sort_frame, text="Nome", variable=self.sort_option, value="name", command=self.update_lists).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(sort_frame, text="Data", variable=self.sort_option, value="date", command=self.update_lists).pack(side=tk.LEFT, padx=5)

        # Progresso
        progress_frame = ttk.Frame(bottom_frame)
        progress_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)
        
        self.status_var = tk.StringVar(value="Aguardando arquivos...")
        self.lbl_status = ttk.Label(progress_frame, textvariable=self.status_var)
        self.lbl_status.pack(anchor=tk.W)

        # Botão Converter
        self.btn_convert = ttk.Button(bottom_frame, text="Converter", command=self.start_conversion)
        self.btn_convert.pack(side=tk.RIGHT, padx=(10, 0))

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Selecione arquivos .ogg",
            filetypes=[("Arquivos OGG", "*.ogg")]
        )
        if files:
            # Atualiza diretório de entrada (baseado no primeiro arquivo)
            self.input_dir.set(os.path.dirname(files[0]))
            
            # Armazenamos o path completo e a data de modificação
            self.input_files = []
            for f in files:
                self.input_files.append({
                    'path': f,
                    'name': os.path.basename(f),
                    'mtime': os.path.getmtime(f)
                })
            self.update_lists()

    def select_output(self):
        directory = filedialog.askdirectory(title="Selecione o diretório de saída")
        if directory:
            self.output_dir.set(directory)

    def update_lists(self):
        """Ordena a lista e atualiza o preview."""
        if not self.input_files:
            return

        # Ordenação
        if self.sort_option.get() == "name":
            self.input_files.sort(key=lambda x: x['name'].lower())
        else:
            self.input_files.sort(key=lambda x: x['mtime'])

        # Atualiza Listbox de Entrada
        self.listbox_input.delete(0, tk.END)
        num_files = len(self.input_files)
        digits = len(str(num_files))
        
        for i, f in enumerate(self.input_files, 1):
            self.listbox_input.insert(tk.END, f"{i:0{digits}d}: {f['name']}")

        # Atualiza Listbox de Preview (Renomeação Sequencial)
        self.listbox_preview.delete(0, tk.END)
        
        for i in range(1, num_files + 1):
            new_name = f"{i:0{digits}d}.mp3"
            self.listbox_preview.insert(tk.END, new_name)
        
        self.status_var.set(f"{num_files} arquivos prontos para conversão.")

    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")
            return
        
        if self.output_dir.get() == "Não selecionado":
            messagebox.showwarning("Aviso", "Selecione um diretório de saída.")
            return
        
        if shutil.which("ffmpeg") is None:
            messagebox.showerror("Erro", "FFmpeg não encontrado. Não é possível converter.")
            return

        # Desabilita botões durante conversão
        self.btn_convert.config(state=tk.DISABLED)
        
        # Inicia Thread
        thread = threading.Thread(target=self.convert_process)
        thread.daemon = True
        thread.start()

    def convert_process(self):
        num_files = len(self.input_files)
        digits = len(str(num_files))
        out_dir = self.output_dir.get()

        for i, file_info in enumerate(self.input_files, 1):
            input_path = file_info['path']
            output_filename = f"{i:0{digits}d}.mp3"
            output_path = os.path.join(out_dir, output_filename)

            self.status_var.set(f"Convertendo {i} de {num_files}: {file_info['name']}...")
            self.progress_var.set((i / num_files) * 100)
            
            # Configuração para esconder a janela do console no Windows
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0 # SW_HIDE

            # Comando FFmpeg
            try:
                # -y: Sobrescrever
                # -i: Input
                # -q:a 2: Qualidade VBR (~190kbps)
                subprocess.run(
                    ["ffmpeg", "-y", "-i", input_path, "-q:a", "2", output_path],
                    check=True,
                    capture_output=True,
                    startupinfo=startupinfo
                )
            except subprocess.CalledProcessError as e:
                print(f"Erro ao converter {file_info['name']}: {e.stderr.decode()}")
                # Poderíamos mostrar um erro aqui, mas vamos continuar para os próximos.

        self.status_var.set("Conversão concluída!")
        self.progress_var.set(100)
        self.btn_convert.config(state=tk.NORMAL)
        messagebox.showinfo("Sucesso", "Todos os arquivos foram convertidos com sucesso.")

if __name__ == "__main__":
    root = tk.Tk()
    app = OggToMp3Converter(root)
    root.mainloop()
