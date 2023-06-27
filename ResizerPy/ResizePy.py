import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, UnidentifiedImageError

SUPPORTED_FORMATS = ["BMP", "DIB", "EPS", "GIF", "ICNS", "ICO", "IM", "JPEG", "JPG", "MSP", "PCX", "PNG", "PPM", "SGI", "SPIDER", "TGA", "TIFF", "WebP", "XBM"]

def resize_image(input_image_path, output_image_path, size, output_format):
    try:
        original_image = Image.open(input_image_path)
    except UnidentifiedImageError:
        raise Exception("The selected input file is not a valid image.")
    except FileNotFoundError:
        raise Exception("The selected input file does not exist.")
    except PermissionError:
        raise Exception("Permission denied when trying to open the input file.")
    except Exception as e:
        raise Exception("An unknown error occurred while opening the input image. Error: " + str(e))

    width, height = original_image.size

    if width > height:
        new_height = size
        new_width = int(new_height * width / height)
    else:
        new_width = size
        new_height = int(new_width * height / width)

    resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

    try:
        resized_image.save(output_image_path, output_format)
    except FileNotFoundError:
        raise Exception("The output directory does not exist.")
    except PermissionError:
        raise Exception("Permission denied when trying to save the output file.")
    except ValueError:
        raise Exception(f"The output format {output_format} is not supported. Please use a supported format.")
    except Exception as e:
        raise Exception("An unknown error occurred while saving the resized image. Error: " + str(e))

def validate_size(size):
    if size <= 0:
        raise Exception("Size must be a positive integer.")

def validate_format(input_path, format):
    if format == "":
        return os.path.splitext(input_path)[1].replace(".", "").upper()
    elif format.upper() not in SUPPORTED_FORMATS:
        raise Exception(f"Format must be one of the following: {', '.join(SUPPORTED_FORMATS)}")
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
        try:
            if not input_path.get():
                raise Exception("Please select an input image.")
            if not output_path.get():
                raise Exception("Please select an output directory.")
            if not size.get().isdigit():
                raise Exception("Please enter a positive integer for the size.")
            size_value = int(size.get())
            validate_size(size_value)
            output_format_value = validate_format(input_path.get(), output_format.get())
            output_image_path = os.path.join(output_path.get(), "resized." + output_format_value)
            if os.path.isfile(output_image_path):
                if not messagebox.askyesno("Overwrite Confirmation", "The output file already exists. Do you want to overwrite it?"):
                    return
            resize_image(input_path.get(), output_image_path, size_value, output_format_value)
            messagebox.showinfo("Success", "Image was successfully resized.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


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

    def display_help():
        messagebox.showinfo("Help", "1. Click 'Browse' next to 'Select Input Image' and choose an image file.\n2. Click 'Browse' next to 'Select Output Directory' and choose a directory.\n3. Enter the desired size for the smaller side of the image (in pixels).\n4. Enter the desired output format (JPEG, PNG, etc.).\n5. Click 'Resize'.")

    tk.Button(window, text="Help", command=display_help, font=small_font).grid(row=5, column=0, columnspan=3, pady=10)

    window.mainloop()

start_program()
