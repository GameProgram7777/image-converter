import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")
        self.root.geometry("500x350")

        # Variables
        self.input_paths = []
        self.target_format = tk.StringVar(value="png")
        self.output_dir = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Input Section
        input_frame = ttk.LabelFrame(self.root, text="Input", padding=(10, 5))
        input_frame.pack(fill="x", padx=10, pady=5)

        self.btn_select_files = ttk.Button(input_frame, text="Select Files", command=self.select_files)
        self.btn_select_files.pack(side="left", padx=5, pady=5)

        self.btn_select_dir = ttk.Button(input_frame, text="Select Directory", command=self.select_directory)
        self.btn_select_dir.pack(side="left", padx=5, pady=5)

        self.lbl_input_status = ttk.Label(input_frame, text="No files selected.")
        self.lbl_input_status.pack(side="left", padx=10, pady=5)

        # Output Directory Section
        output_dir_frame = ttk.LabelFrame(self.root, text="Output Directory", padding=(10, 5))
        output_dir_frame.pack(fill="x", padx=10, pady=5)

        self.ent_output_dir = ttk.Entry(output_dir_frame, textvariable=self.output_dir, state="readonly")
        self.ent_output_dir.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.btn_output_dir = ttk.Button(output_dir_frame, text="Browse...", command=self.select_output_dir)
        self.btn_output_dir.pack(side="right", padx=5, pady=5)

        # Target Format Section
        format_frame = ttk.LabelFrame(self.root, text="Target Format", padding=(10, 5))
        format_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(format_frame, text="Format:").pack(side="left", padx=5, pady=5)

        # Adding a combobox with some common formats, but allow custom entry
        self.cb_format = ttk.Combobox(format_frame, textvariable=self.target_format,
                                      values=["png", "jpg", "jpeg", "webp", "gif", "bmp", "tiff", "ico"])
        self.cb_format.pack(side="left", padx=5, pady=5)

        # Convert Section
        convert_frame = ttk.Frame(self.root, padding=(10, 5))
        convert_frame.pack(fill="x", padx=10, pady=10)

        self.btn_convert = ttk.Button(convert_frame, text="Convert Images", command=self.convert_images)
        self.btn_convert.pack(fill="x", pady=5)

        # Progress/Status Section
        self.lbl_status = ttk.Label(self.root, text="Ready.")
        self.lbl_status.pack(pady=5)

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=(("All Files", "*.*"), ("JPEG", "*.jpg;*.jpeg"), ("PNG", "*.png"), ("WebP", "*.webp"))
        )
        if files:
            self.input_paths = list(files)
            self.lbl_input_status.config(text=f"{len(self.input_paths)} file(s) selected.")

            # If output dir is not set, set it to the directory of the first selected file
            if not self.output_dir.get():
                self.output_dir.set(os.path.dirname(self.input_paths[0]))

    def select_directory(self):
        directory = filedialog.askdirectory(title="Select Directory with Images")
        if directory:
            # Gather all files in the directory
            self.input_paths = []
            valid_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff', '.ico'}
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    _, ext = os.path.splitext(filename)
                    if ext.lower() in valid_extensions:
                        self.input_paths.append(filepath)

            if self.input_paths:
                self.lbl_input_status.config(text=f"{len(self.input_paths)} file(s) found in directory.")
                if not self.output_dir.get():
                    self.output_dir.set(directory)
            else:
                self.lbl_input_status.config(text="No files found in directory.")

    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)

    def convert_images(self):
        if not self.input_paths:
            messagebox.showwarning("Warning", "Please select input files or a directory.")
            return

        out_dir = self.output_dir.get()
        if not out_dir:
            messagebox.showwarning("Warning", "Please select an output directory.")
            return

        target_ext = self.target_format.get().strip().lower()
        if not target_ext:
            messagebox.showwarning("Warning", "Please specify a target format.")
            return

        # Ensure target format starts with a dot for extension logic
        if target_ext.startswith("."):
            target_ext = target_ext[1:]

        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create output directory:\n{e}")
                return

        self.btn_convert.config(state="disabled")
        self.lbl_status.config(text="Converting...")

        # Run conversion in a separate thread to keep UI responsive
        import threading
        def conversion_thread():
            success_count = 0
            fail_count = 0

            for idx, path in enumerate(self.input_paths):
                try:
                    # Open image
                    img = Image.open(path)

                    # Handling modes for formats that don't support alpha (like JPEG)
                    if target_ext in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')

                    filename = os.path.basename(path)
                    name, _ = os.path.splitext(filename)

                    # Construct output path
                    out_path = os.path.join(out_dir, f"{name}.{target_ext}")

                    # Save
                    img.save(out_path)
                    success_count += 1
                except Exception as e:
                    print(f"Failed to convert {path}: {e}")
                    fail_count += 1

                # Update status safely from thread
                if idx % 10 == 0:
                    self.root.after(0, lambda i=idx: self.lbl_status.config(text=f"Processed {i + 1} of {len(self.input_paths)}"))

            self.root.after(0, lambda: self.conversion_finished(success_count, fail_count))

        threading.Thread(target=conversion_thread, daemon=True).start()

    def conversion_finished(self, success_count, fail_count):
        self.btn_convert.config(state="normal")
        if fail_count == 0:
            msg = f"Successfully converted {success_count} image(s)."
            self.lbl_status.config(text="Done.")
            messagebox.showinfo("Success", msg)
        else:
            msg = f"Converted {success_count} image(s). Failed {fail_count} image(s)."
            self.lbl_status.config(text="Done with errors.")
            messagebox.showwarning("Completed with Errors", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
