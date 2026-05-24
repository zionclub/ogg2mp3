import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import soundfile as sf
import lameenc
import numpy as np

class OggToMp3Converter:
    """
    A GUI application to convert OGG (Opus) files to MP3 using native Python libraries.
    This approach bypasses FFmpeg's metadata issues with WhatsApp voice notes.
    """
    def __init__(self, root):
        self.root = root
        self.lang = tk.StringVar(value="en")
        
        # Translation dictionary
        self.translations = {
            "en": {
                "title": "Ogg2Mp3 Converter (Native)",
                "select_files": "Select .ogg Files",
                "select_output": "Select Output Directory",
                "not_selected": "Not selected",
                "list_label": "Selected Files (Conversion Order)",
                "sort_label": "Sort by:",
                "sort_name": "Name",
                "sort_date": "Date",
                "status_waiting": "Waiting for files...",
                "status_ready": "{num} files ready for conversion.",
                "status_converting": "Converting {i} of {total}: {name}...",
                "status_done": "Conversion completed!",
                "log_from": "From: ",
                "log_to": "To: ",
                "btn_convert": "Convert",
                "warn_title": "Warning",
                "warn_no_files": "No files selected.",
                "warn_no_output": "Please select an output directory.",
                "success_title": "Success",
                "success_msg": "All files were converted successfully.",
                "error_msg": "Error converting {name}: {err}"
            },
            "pt": {
                "title": "Conversor OGG para MP3 (Nativo)",
                "select_files": "Selecionar Arquivos .ogg",
                "select_output": "Selecionar Diretório de Saída",
                "not_selected": "Não selecionado",
                "list_label": "Arquivos Selecionados (Ordem de Conversão)",
                "sort_label": "Ordenar por:",
                "sort_name": "Nome",
                "sort_date": "Data",
                "status_waiting": "Aguardando arquivos...",
                "status_ready": "{num} arquivos prontos para conversão.",
                "status_converting": "Convertendo {i} de {total}: {name}...",
                "status_done": "Conversão concluída!",
                "log_from": "De: ",
                "log_to": "Para: ",
                "btn_convert": "Converter",
                "warn_title": "Aviso",
                "warn_no_files": "Nenhum arquivo selecionado.",
                "warn_no_output": "Por favor, selecione um diretório de saída.",
                "success_title": "Sucesso",
                "success_msg": "Todos os arquivos foram convertidos com sucesso.",
                "error_msg": "Erro ao converter {name}: {err}"
            }
        }

        self.input_files = []
        self.output_dir = tk.StringVar(value=self.get_text("not_selected"))
        self.sort_option = tk.StringVar(value="name")
        self.status_var = tk.StringVar(value=self.get_text("status_waiting"))
        self.log_var = tk.StringVar(value="")
        
        self.setup_ui()
        self.update_ui_texts()

    def get_text(self, key, **kwargs):
        """Helper to get translated text."""
        text = self.translations[self.lang.get()].get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text

    def change_language(self):
        """Callback for language selector."""
        self.update_ui_texts()
        if self.input_files:
            self.update_lists()
        else:
            self.status_var.set(self.get_text("status_waiting"))

    def update_ui_texts(self):
        """Updates all static and dynamic UI labels based on current language."""
        self.root.title(self.get_text("title"))
        self.btn_select_files.config(text=self.get_text("select_files"))
        self.btn_select_output.config(text=self.get_text("select_output"))
        self.lbl_list_title.config(text=self.get_text("list_label"))
        self.sort_frame.config(text=self.get_text("sort_label"))
        self.radio_name.config(text=self.get_text("sort_name"))
        self.radio_date.config(text=self.get_text("sort_date"))
        self.btn_convert.config(text=self.get_text("btn_convert"))
        
        if self.output_dir.get() in ["Not selected", "Não selecionado"]:
            self.output_dir.set(self.get_text("not_selected"))

    def setup_ui(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top Panels (Selection)
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Language Selector (Mini-selector)
        lang_frame = ttk.Frame(top_frame)
        lang_frame.pack(side=tk.TOP, anchor=tk.E)
        ttk.Label(lang_frame, text="Lang:").pack(side=tk.LEFT)
        ttk.Radiobutton(lang_frame, text="EN", variable=self.lang, value="en", command=self.change_language).pack(side=tk.LEFT)
        ttk.Radiobutton(lang_frame, text="PT", variable=self.lang, value="pt", command=self.change_language).pack(side=tk.LEFT)

        # Left: Select Files
        left_selection = ttk.Frame(top_frame)
        left_selection.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        self.btn_select_files = ttk.Button(left_selection, text="", command=self.select_files)
        self.btn_select_files.pack(side=tk.TOP, anchor=tk.NW)

        # Right: Select Output
        right_selection = ttk.Frame(top_frame)
        right_selection.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        
        self.btn_select_output = ttk.Button(right_selection, text="", command=self.select_output)
        self.btn_select_output.pack(side=tk.TOP, anchor=tk.NE)
        
        lbl_output = ttk.Label(right_selection, textvariable=self.output_dir, wraplength=350, foreground="gray")
        lbl_output.pack(side=tk.TOP, anchor=tk.E, pady=(5, 0))

        # Central Panel (Single List)
        lists_frame = ttk.Frame(main_frame)
        lists_frame.pack(fill=tk.BOTH, expand=True)

        self.lbl_list_title = ttk.Label(lists_frame, text="")
        self.lbl_list_title.pack(anchor=tk.W)
        
        # Scrollbars for the list
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

        # Bottom Panel (Controls and Progress)
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))

        # Sorting
        self.sort_frame = ttk.LabelFrame(bottom_frame, text="", padding="5")
        self.sort_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        self.radio_name = ttk.Radiobutton(self.sort_frame, text="", variable=self.sort_option, value="name", command=self.update_lists)
        self.radio_name.pack(side=tk.LEFT, padx=5)
        self.radio_date = ttk.Radiobutton(self.sort_frame, text="", variable=self.sort_option, value="date", command=self.update_lists)
        self.radio_date.pack(side=tk.LEFT, padx=5)

        # Progress
        progress_frame = ttk.Frame(bottom_frame)
        progress_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)
        
        self.lbl_status = ttk.Label(progress_frame, textvariable=self.status_var)
        self.lbl_status.pack(anchor=tk.W)

        self.lbl_log = ttk.Label(progress_frame, textvariable=self.log_var, font=("Consolas", 8), foreground="gray")
        self.lbl_log.pack(anchor=tk.W)

        # Convert Button
        self.btn_convert = ttk.Button(bottom_frame, text="", command=self.start_conversion)
        self.btn_convert.pack(side=tk.RIGHT, padx=(10, 0))

    def select_files(self):
        files = filedialog.askopenfilenames(
            title=self.get_text("select_files"),
            filetypes=[("OGG Files", "*.ogg")]
        )
        if files:
            self.input_files = []
            for f in files:
                self.input_files.append({
                    'path': f,
                    'name': os.path.basename(f),
                    'mtime': os.path.getmtime(f)
                })
            self.update_lists()

    def select_output(self):
        directory = filedialog.askdirectory(title=self.get_text("select_output"))
        if directory:
            self.output_dir.set(directory)

    def update_lists(self):
        """Sorts the list and updates the interface."""
        if not self.input_files:
            return

        # Sorting logic
        if self.sort_option.get() == "name":
            self.input_files.sort(key=lambda x: x['name'].lower())
        else:
            self.input_files.sort(key=lambda x: x['mtime'])

        # Update Listbox
        self.listbox_input.delete(0, tk.END)
        num_files = len(self.input_files)
        digits = len(str(num_files))
        
        for i, f in enumerate(self.input_files, 1):
            # Format: 01: C:\path\file.ogg
            self.listbox_input.insert(tk.END, f"{i:0{digits}d}: {f['path']}")
        
        self.status_var.set(self.get_text("status_ready", num=num_files))

    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning(self.get_text("warn_title"), self.get_text("warn_no_files"))
            return
        
        if self.output_dir.get() == self.get_text("not_selected"):
            messagebox.showwarning(self.get_text("warn_title"), self.get_text("warn_no_output"))
            return

        self.btn_convert.config(state=tk.DISABLED)
        
        # Start conversion in a background thread to keep UI responsive
        thread = threading.Thread(target=self.convert_process)
        thread.daemon = True
        thread.start()

    def convert_process(self):
        """Core conversion loop using soundfile and lameenc."""
        num_files = len(self.input_files)
        digits = len(str(num_files))
        out_dir = self.output_dir.get()

        for i, file_info in enumerate(self.input_files, 1):
            input_path = file_info['path']
            output_filename = f"{i:0{digits}d}.mp3"
            output_path = os.path.join(out_dir, output_filename)

            self.status_var.set(self.get_text("status_converting", i=i, total=num_files, name=file_info['name']))
            self.log_var.set(f"{self.get_text('log_from')}{input_path}\n{self.get_text('log_to')}{output_path}")
            self.progress_var.set((i / num_files) * 100)
            
            try:
                # 1. Read OGG file using soundfile (ignores broken granule metadata)
                data, samplerate = sf.read(input_path)
                
                # Identify channels
                if data.ndim == 1:
                    channels = 1
                else:
                    channels = data.shape[1]

                # Convert Float (-1.0 to 1.0) to Int16 (PCM)
                # lameenc requires raw PCM bytes
                pcm_data = np.clip(data * 32767, -32768, 32767).astype(np.int16).tobytes()

                # 2. Configure native LAME encoder
                encoder = lameenc.Encoder()
                encoder.set_bit_rate(192) 
                encoder.set_in_sample_rate(samplerate)
                encoder.set_channels(channels)
                encoder.set_quality(2) # High quality
                
                # 3. Encode and save the final file
                mp3_data = encoder.encode(pcm_data)
                mp3_data += encoder.flush()
                
                with open(output_path, 'wb') as f:
                    f.write(mp3_data)
                    
            except Exception as e:
                print(self.get_text("error_msg", name=file_info['name'], err=str(e)))

        self.status_var.set(self.get_text("status_done"))
        self.progress_var.set(100)
        self.btn_convert.config(state=tk.NORMAL)
        messagebox.showinfo(self.get_text("success_title"), self.get_text("success_msg"))

if __name__ == "__main__":
    root = tk.Tk()
    app = OggToMp3Converter(root)
    root.mainloop()
