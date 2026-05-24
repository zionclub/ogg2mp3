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
        self.root.title("Ogg2Mp3 Converter (Native)")
        self.root.geometry("800x600")
        
        self.input_files = []
        self.output_dir = tk.StringVar(value="Not selected")
        self.sort_option = tk.StringVar(value="name")
        
        self.setup_ui()

    def setup_ui(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top Panels (Selection)
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # Left: Select Files
        left_selection = ttk.Frame(top_frame)
        left_selection.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        btn_select_files = ttk.Button(left_selection, text="Select .ogg Files", command=self.select_files)
        btn_select_files.pack(side=tk.TOP, anchor=tk.NW)

        # Right: Select Output
        right_selection = ttk.Frame(top_frame)
        right_selection.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        
        btn_select_output = ttk.Button(right_selection, text="Select Output Directory", command=self.select_output)
        btn_select_output.pack(side=tk.TOP, anchor=tk.NE)
        
        lbl_output = ttk.Label(right_selection, textvariable=self.output_dir, wraplength=350, foreground="gray")
        lbl_output.pack(side=tk.TOP, anchor=tk.E, pady=(5, 0))

        # Central Panel (Single List)
        lists_frame = ttk.Frame(main_frame)
        lists_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(lists_frame, text="Selected Files (Conversion Order)").pack(anchor=tk.W)
        
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
        sort_frame = ttk.LabelFrame(bottom_frame, text="Sort by:", padding="5")
        sort_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(sort_frame, text="Name", variable=self.sort_option, value="name", command=self.update_lists).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(sort_frame, text="Date", variable=self.sort_option, value="date", command=self.update_lists).pack(side=tk.LEFT, padx=5)

        # Progress
        progress_frame = ttk.Frame(bottom_frame)
        progress_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)
        
        self.status_var = tk.StringVar(value="Waiting for files...")
        self.lbl_status = ttk.Label(progress_frame, textvariable=self.status_var)
        self.lbl_status.pack(anchor=tk.W)

        self.log_var = tk.StringVar(value="")
        self.lbl_log = ttk.Label(progress_frame, textvariable=self.log_var, font=("Consolas", 8), foreground="gray")
        self.lbl_log.pack(anchor=tk.W)

        # Convert Button
        self.btn_convert = ttk.Button(bottom_frame, text="Convert", command=self.start_conversion)
        self.btn_convert.pack(side=tk.RIGHT, padx=(10, 0))

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select .ogg files",
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
        directory = filedialog.askdirectory(title="Select output directory")
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
        
        self.status_var.set(f"{num_files} files ready for conversion.")

    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("Warning", "No files selected.")
            return
        
        if self.output_dir.get() == "Not selected":
            messagebox.showwarning("Warning", "Please select an output directory.")
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

            self.status_var.set(f"Converting {i} of {num_files}: {file_info['name']}...")
            self.log_var.set(f"From: {input_path}\nTo: {output_path}")
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
                print(f"Error converting {file_info['name']}: {e}")

        self.status_var.set("Conversion completed!")
        self.progress_var.set(100)
        self.btn_convert.config(state=tk.NORMAL)
        messagebox.showinfo("Success", "All files were converted successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = OggToMp3Converter(root)
    root.mainloop()
