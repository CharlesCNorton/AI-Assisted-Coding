import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, UnidentifiedImageError, ExifTags
import threading

SUPPORTED_FORMATS = ["BMP", "DIB", "EPS", "GIF", "ICNS", "ICO", "IM", "JPEG", "JPG", "MSP", "PCX", "PNG", "PPM", "SGI", "SPIDER", "TGA", "TIFF", "WebP", "XBM"]

def resize_image(input_image_path, output_image_path, size, output_format, progress_bar):
    try:
        original_image = Image.open(input_image_path)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    if not original_image.format in SUPPORTED_FORMATS:
        messagebox.showerror("Error", f"Invalid file format. Supported formats are: {', '.join(SUPPORTED_FORMATS)}")
        return

    exif = original_image.info['exif'] if 'exif' in original_image.info else None

    width, height = original_image.size

    if width > height:
        new_height = size
        new_width = int(new_height * width / height)
    else:
        new_width = size
        new_height = int(new_width * height / width)

    resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

    try:
        if exif:
            resized_image.save(output_image_path, output_format, exif=exif)
        else:
            resized_image.save(output_image_path, output_format)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    progress_bar.stop()
    messagebox.showinfo("Success", "Image was successfully resized.")

def validate_size(size):
    if size <= 0:
        messagebox.showerror("Error", "Size must be a positive integer.")

def validate_format(input_path, format):
    if format == "":
        return os.path.splitext(input_path)[1].replace(".", "").upper()
    elif format.upper() not in SUPPORTED_FORMATS:
        messagebox.showerror("Error", f"Format must be one of the following: {', '.join(SUPPORTED_FORMATS)}")
    else:
        return format

def start_program():
    window = tk.Tk()
    window.title("Image Resizer")
    window.configure(bg='white')

    large_font = ('Verdana', 12)
    small_font = ('Verdana', 10)

    input_path = tk.StringVar()
    output_path = tk.StringVar()
    size = tk.StringVar()
    output_format = tk.StringVar()

    def browse_file(path_variable):
        path_variable.set(filedialog.askopenfilename())

    def browse_folder(path_variable):
        path_variable.set(filedialog.askdirectory())

    def resize():
        if not input_path.get():
            messagebox.showerror("Error", "Please select an input image.")
            return
        if not output_path.get():
            messagebox.showerror("Error", "Please select an output directory.")
            return
        if not size.get().isdigit():
            messagebox.showerror("Error", "Please enter a positive integer for the size.")
            return
        size_value = int(size.get())
        validate_size(size_value)
        output_format_value = validate_format(input_path.get(), output_format.get())
        output_image_path = os.path.join(output_path.get(), "resized." + output_format_value)
        if os.path.isfile(output_image_path):
            if not messagebox.askyesno("Overwrite Confirmation", "The output file already exists. Do you want to overwrite it?"):
                return
        progress_bar.start()
        threading.Thread(target=resize_image, args=(input_path.get(), output_image_path, size_value, output_format_value, progress_bar)).start()

    tk.Label(window, text="Select Input Image:", bg='white', font=large_font).grid(row=0, column=0, sticky='W', padx=10, pady=10)
    tk.Entry(window, textvariable=input_path, font=small_font).grid(row=0, column=1, padx=10)
    tk.Button(window, text="Browse", command=lambda: browse_file(input_path), font=small_font).grid(row=0, column=2, padx=10)

    tk.Label(window, text="Select Output Directory:", bg='white', font=large_font).grid(row=1, column=0, sticky='W', padx=10, pady=10)
    tk.Entry(window, textvariable=output_path, font=small_font).grid(row=1, column=1, padx=10)
    tk.Button(window, text="Browse", command=lambda: browse_folder(output_path), font=small_font).grid(row=1, column=2, padx=10)

    tk.Label(window, text="Enter Output Format (JPEG, PNG, etc.):", bg='white', font=large_font).grid(row=2, column=0, sticky='W', padx=10, pady=10)
    tk.Entry(window, textvariable=output_format, font=small_font).grid(row=2, column=1, padx=10)

    tk.Label(window, text="Enter the Size for the Smaller Side of the Image:", bg='white', font=large_font).grid(row=3, column=0, sticky='W', padx=10, pady=10)
    tk.Entry(window, textvariable=size, font=small_font).grid(row=3, column=1, padx=10)

    tk.Button(window, text="Resize", command=resize, font=small_font).grid(row=4, column=0, columnspan=3, pady=10)

    progress_bar = ttk.Progressbar(window, mode='indeterminate')
    progress_bar.grid(row=5, column=0, columnspan=3, sticky='EW')

    def display_help():
        messagebox.showinfo("Help", "1. Click 'Browse' next to 'Select Input Image' and choose an image file.\n2. Click 'Browse' next to 'Select Output Directory' and choose a directory.\n3. Enter the desired size for the smaller side of the image (in pixels).\n4. Enter the desired output format (JPEG, PNG, etc.).\n5. Click 'Resize'.")

    tk.Button(window, text="Help", command=display_help, font=small_font).grid(row=6, column=0, columnspan=3, pady=10)

    window.mainloop()

start_program()
