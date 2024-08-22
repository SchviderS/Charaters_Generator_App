import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os
import time
import warnings

class FontImageGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Font Image Generator")

        self.style = ttk.Style()
        self.style.configure("TLabel", padding=6)
        self.style.configure("TButton", padding=6)
        self.style.configure("TCheckbutton", padding=6)

        self.root.geometry("600x550")  # Set the initial size of the window
        
        self.font_label = tk.Label(root, text="Select fonts:")
        self.font_label.pack()

        self.font_button = tk.Button(root, text="Browse", command=self.browse_fonts)
        self.font_button.pack(padx=10, pady=(0, 10))

        self.size_label = tk.Label(root, text="Select image size:")
        self.size_label.pack()

        self.image_size_var = tk.StringVar()
        self.image_size_var.set("48x48")  # Default value
        self.image_size_menu = tk.OptionMenu(root, self.image_size_var, "48x48", "56x56", "64x64")
        self.image_size_menu.pack(padx=10, pady=(0, 10))

        self.font_size_label = tk.Label(root, text="Select font sizes:")
        self.font_size_label.pack()

        self.small_var = tk.IntVar()
        self.medium_var = tk.IntVar()
        self.large_var = tk.IntVar()

        self.small_checkbox = tk.Checkbutton(root, text="Small", variable=self.small_var)
        self.small_checkbox.pack()

        self.medium_checkbox = tk.Checkbutton(root, text="Medium", variable=self.medium_var)
        self.medium_checkbox.pack()

        self.large_checkbox = tk.Checkbutton(root, text="Large", variable=self.large_var)
        self.large_checkbox.pack(padx=10, pady=(0, 10))

        self.capitals_var = tk.IntVar()
        self.small_var = tk.IntVar()
        self.numbers_var = tk.IntVar()

        self.case_label = tk.Label(root, text="Select letter case:")
        self.case_label.pack()

        self.capitals_checkbox = tk.Checkbutton(root, text="Capital Letters", variable=self.capitals_var)
        self.capitals_checkbox.pack()

        self.small_checkbox = tk.Checkbutton(root, text="Small Letters", variable=self.small_var)
        self.small_checkbox.pack()

        self.numbers_checkbox = tk.Checkbutton(root, text="Numbers", variable=self.numbers_var)
        self.numbers_checkbox.pack()

        self.error_label = ttk.Label(root, text="", foreground="red")
        self.error_label.pack()

        self.output_label = tk.Label(root, text="Select an output directory:")
        self.output_label.pack()

        self.output_button = tk.Button(root, text="Browse", command=self.browse_output)
        self.output_button.pack(padx=10, pady=(0, 10))

        self.generate_button = ttk.Button(root, text="Generate Images", command=self.generate_images)
        self.generate_button.pack(fill="both", padx=10, pady=(0, 10))

        self.selected_fonts = []
        self.selected_font_sizes = []
        self.output_directory = None

        self.error_label = ttk.Label(root, text="", foreground="red")
        self.error_label.pack()

        self.name_label = ttk.Label(root, text="Created by Rumit Pathare", foreground="gray")
        self.name_label.pack()

    def display_error(self, error_message):
        self.error_label.config(text=error_message)

    def browse_fonts(self):
        font_paths = filedialog.askopenfilenames(filetypes=[("Font files", "*.ttf")])
        if font_paths:
            self.selected_fonts = font_paths
            font_names = [os.path.basename(path) for path in font_paths]
            self.font_label.config(text=f"Selected fonts: {', '.join(font_names)}")

    def browse_output(self):
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.output_directory = output_dir
            self.output_label.config(text=f"Selected output directory: {self.output_directory}")

    def generate_images(self):
        self.error_label.config(text="")  # Clear previous error messages

        if not (self.selected_fonts and self.output_directory):
            self.display_error("Please select fonts and output directory.")
            return

        selected_image_size = self.image_size_var.get().split("x")
        image_width = int(selected_image_size[0])
        image_height = int(selected_image_size[1])

        selected_characters = ""
        if self.capitals_var.get():
            selected_characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.small_var.get():
            selected_characters += "abcdefghijklmnopqrstuvwxyz"
        if self.numbers_var.get():
            selected_characters += "0123456789"

        dataset_dir = Path(self.output_directory) / "Dataset"
        dataset_dir.mkdir(parents=True, exist_ok=True)

        if not (self.small_var.get() or self.medium_var.get() or self.large_var.get()):
            self.display_error("Please select at least one font size.")
            return

        self.selected_font_sizes = []
        if self.small_var.get():
            self.selected_font_sizes.append(image_width - 16)
        if self.medium_var.get():
            self.selected_font_sizes.append(image_width - 8)
        if self.large_var.get():
            self.selected_font_sizes.append(image_width)

        for font_path in self.selected_fonts:
            font_name = os.path.basename(font_path).split(".")[0]

            for font_size in self.selected_font_sizes:
                font = ImageFont.truetype(font_path, font_size)
                font_size_text = str(font_size)

                for letter in selected_characters:
                    image = Image.new("L", (image_width, image_height), "white")
                    draw = ImageDraw.Draw(image)

                    text = letter
                    text_width = draw.textlength(text, font)
                    text_height = font_size
                    x = (image_width - text_width) // 2
                    y = (image_height - text_height) // 2

                    draw.text((x, y), text, font=font, fill="black")

                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    category_name = "CapitalLetters" if letter.isupper() else "SmallLetters"
                    if letter.isdigit():
                        category_name = "Numbers"
                    output_dir = dataset_dir / category_name / letter
                    output_dir.mkdir(parents=True, exist_ok=True)
                    image.save(output_dir / f"{letter}_{font_name}_{font_size_text}_{timestamp}.png")

                    print(f"Generated image for letter {letter} using font {font_name}, font size {font_size}, and timestamp {timestamp}")


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    root = tk.Tk()
    app = FontImageGeneratorApp(root)
    root.minsize(600, 550)
    root.mainloop()
