import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import soundfile as sf
import lameenc
import numpy as np
from datetime import datetime

class OggToMp3Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor OGG para MP3 (Native)")
        self.root.geometry("800x600")
        
        self.input_files = []
        self.output_dir = tk.StringVar(value="Não selecionado")
        self.sort_option = tk.StringVar(value="name")
        
        self.setup_ui()

    def setup_ui(self):
        # Frame Principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Painéis Superior (Seleção)
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # Esquerda: Selecionar Arquivos
        left_selection = ttk.Frame(top_frame)
        left_selection.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        btn_select_files = ttk.Button(left_selection, text="Selecionar Arquivos .ogg", command=self.select_files)
        btn_select_files.pack(side=tk.TOP, anchor=tk.NW)

        # Direita: Selecionar Saída
        right_selection = ttk.Frame(top_frame)
        right_selection.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        
        btn_select_output = ttk.Button(right_selection, text="Selecionar Diretório de Saída", command=self.select_output)
        btn_select_output.pack(side=tk.TOP, anchor=tk.NE)
        
        lbl_output = ttk.Label(right_selection, textvariable=self.output_dir, wraplength=350, foreground="gray")
        lbl_output.pack(side=tk.TOP, anchor=tk.E, pady=(5, 0))

        # Painel Central (Lista Única)
        lists_frame = ttk.Frame(main_frame)
        lists_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(lists_frame, text="Arquivos Selecionados (Ordem de Conversão)").pack(anchor=tk.W)
        
        # Scrollbar para a lista
        scrollbar_y = ttk.Scrollbar(lists_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(lists_frame, orient=tk.HORIZONTAL)
        
        self.listbox_input = tk.Listbox(
            lists_frame, 
            selectmode=tk.EXTENDED, 
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        scrollbar_y.config(command=self.listbox_input.yview)
        scrollbar_x.config(command=self.listbox_input.xview)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox_input.pack(fill=tk.BOTH, expand=True)

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

        self.log_var = tk.StringVar(value="")
        self.lbl_log = ttk.Label(progress_frame, textvariable=self.log_var, font=("Consolas", 8), foreground="gray")
        self.lbl_log.pack(anchor=tk.W)

        # Botão Converter
        self.btn_convert = ttk.Button(bottom_frame, text="Converter", command=self.start_conversion)
        self.btn_convert.pack(side=tk.RIGHT, padx=(10, 0))

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Selecione arquivos .ogg",
            filetypes=[("Arquivos OGG", "*.ogg")]
        )
        if files:
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
        """Ordena a lista e atualiza a interface."""
        if not self.input_files:
            return

        # Ordenação
        if self.sort_option.get() == "name":
            self.input_files.sort(key=lambda x: x['name'].lower())
        else:
            self.input_files.sort(key=lambda x: x['mtime'])

        # Atualiza Listbox
        self.listbox_input.delete(0, tk.END)
        num_files = len(self.input_files)
        digits = len(str(num_files))
        
        for i, f in enumerate(self.input_files, 1):
            # Formato: 01: C:\diretorio\arquivo.ogg
            self.listbox_input.insert(tk.END, f"{i:0{digits}d}: {f['path']}")
        
        self.status_var.set(f"{num_files} arquivos prontos para conversão.")

    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")
            return
        
        if self.output_dir.get() == "Não selecionado":
            messagebox.showwarning("Aviso", "Selecione um diretório de saída.")
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
            self.log_var.set(f"De: {input_path}\nPara: {output_path}")
            self.progress_var.set((i / num_files) * 100)
            
            try:
                # 1. Lê o arquivo OGG usando soundfile (mais robusto com Opus/WhatsApp)
                data, samplerate = sf.read(input_path)
                
                # Identifica canais
                if data.ndim == 1:
                    channels = 1
                else:
                    channels = data.shape[1]

                # Converte Float (-1.0 a 1.0) para Int16 (PCM)
                # O lameenc exige dados em bytes PCM
                pcm_data = np.clip(data * 32767, -32768, 32767).astype(np.int16).tobytes()

                # 2. Configura o encoder LAME nativo
                encoder = lameenc.Encoder()
                encoder.set_bit_rate(192) 
                encoder.set_in_sample_rate(samplerate)
                encoder.set_channels(channels)
                encoder.set_quality(2) # Alta qualidade
                
                # 3. Codifica e salva o arquivo final
                mp3_data = encoder.encode(pcm_data)
                mp3_data += encoder.flush()
                
                with open(output_path, 'wb') as f:
                    f.write(mp3_data)
                    
            except Exception as e:
                print(f"Erro ao converter {file_info['name']}: {e}")

        self.status_var.set("Conversão concluída!")
        self.progress_var.set(100)
        self.btn_convert.config(state=tk.NORMAL)
        messagebox.showinfo("Sucesso", "Todos os arquivos foram convertidos com sucesso.")

if __name__ == "__main__":
    root = tk.Tk()
    app = OggToMp3Converter(root)
    root.mainloop()
