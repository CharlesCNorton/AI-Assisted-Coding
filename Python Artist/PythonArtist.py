# PythonArtist was created with GPT-4 on June 15, 2023.
# This program is a simple paint application created using the tkinter library in Python. It allows users to draw on a canvas using various tools such as a brush, line,
# rectangle, and eraser. Users can also choose the brush color and size, clear the canvas, undo previous actions, save the drawing as an image, and load an image to edit.

import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import ImageDraw, Image, ImageTk

class PaintApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Paint")
        self.current_tool = tk.StringVar(value="brush")
        self.brush_color = tk.StringVar(value="black")
        self.brush_size = tk.IntVar(value=5)
        self.lastx = self.lasty = self.startx = self.starty = None
        self.image = Image.new("RGB", (400, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.undo_stack = []
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.create_canvas()
        self.create_tool_buttons()
        self.create_size_buttons()
        self.create_bottom_buttons()
        self.create_message()

    def create_canvas(self):
        """Create and configure the canvas."""
        self.canvas_frame = tk.Frame(self.root, bd=2, bg="black")
        self.canvas_frame.pack(padx=10, pady=10)
        self.canvas = tk.Canvas(self.canvas_frame, width=400, height=400, bg="white")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.reset_coords)
        self.canvas.bind("<ButtonRelease-1>", self.draw_shape)

    def create_tool_buttons(self):
        """Create and configure tool selection buttons."""
        self.tool_frame = tk.Frame(self.root)
        self.tool_frame.pack(side=tk.TOP)
        tools = ["brush", "line", "rectangle", "eraser"]
        for tool in tools:
            b = tk.Radiobutton(self.tool_frame, text=tool.capitalize(), variable=self.current_tool, value=tool)
            b.pack(side=tk.LEFT)
        self.color_button = tk.Button(self.tool_frame, text="Choose Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

    def create_size_buttons(self):
        """Create and configure brush size buttons."""
        self.size_frame = tk.Frame(self.root)
        self.size_frame.pack(side=tk.TOP)
        sizes = [1, 3, 5, 7, 9]
        for size in sizes:
            b = tk.Radiobutton(self.size_frame, text=str(size), variable=self.brush_size, value=size)
            b.pack(side=tk.LEFT)

    def create_bottom_buttons(self):
        """Create and configure bottom utility buttons."""
        self.clear_button = tk.Button(self.root, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(side=tk.BOTTOM)
        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.BOTTOM)
        self.save_button = tk.Button(self.root, text="Save Image", command=self.save)
        self.save_button.pack(side=tk.BOTTOM)
        self.load_button = tk.Button(self.root, text="Load Image", command=self.load)
        self.load_button.pack(side=tk.BOTTOM)

    def create_message(self):
        """Create and configure the message label."""
        self.message = tk.Label(self.root, text="Press and Drag the mouse to draw")
        self.message.pack(side=tk.BOTTOM)

    def paint(self, event):
        x, y = event.x, event.y
        if self.lastx is not None and self.lasty is not None:
            if self.current_tool.get() == "brush":
                self.draw.line((self.lastx, self.lasty, x, y), fill=self.brush_color.get(), width=self.brush_size.get())
                self.canvas.create_line(self.lastx, self.lasty, x, y, fill=self.brush_color.get(), width=self.brush_size.get())
            elif self.current_tool.get() == "line":
                self.canvas.delete("temp_line")
                self.canvas.create_line(self.startx, self.starty, x, y, tags="temp_line", fill=self.brush_color.get(), width=self.brush_size.get())
            elif self.current_tool.get() == "eraser":
                self.draw.line((self.lastx, self.lasty, x, y), fill="white", width=self.brush_size.get())
                self.canvas.create_line(self.lastx, self.lasty, x, y, fill="white", width=self.brush_size.get())
        self.lastx, self.lasty = x, y

    def reset_coords(self, event):
        self.startx, self.starty = self.lastx, self.lasty = event.x, event.y

    def draw_shape(self, event):
        x, y = event.x, event.y
        if self.current_tool.get() == "line":
            self.canvas.delete("temp_line")
            self.draw.line((self.startx, self.starty, x, y), fill=self.brush_color.get(), width=self.brush_size.get())
            self.canvas.create_line(self.startx, self.starty, x, y, fill=self.brush_color.get(), width=self.brush_size.get())
        elif self.current_tool.get() == "rectangle":
            self.draw.rectangle((self.startx, self.starty, x, y), outline=self.brush_color.get(), width=self.brush_size.get())
            self.canvas.create_rectangle(self.startx, self.starty, x, y, outline=self.brush_color.get(), width=self.brush_size.get())

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle((0, 0, self.image.width, self.image.height), fill="white")

    def undo(self):
        if len(self.undo_stack) > 0:
            img = self.undo_stack.pop()
            self.image.paste(img)
            self.canvas.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor=tk.NW)

    def save(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png")
        if filename:
            self.image.save(filename)

    def load(self):
        filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filename:
            self.clear_canvas()
            self.image = Image.open(filename)
            self.draw = ImageDraw.Draw(self.image)
            self.canvas.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor=tk.NW)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.brush_color.set(color)

if __name__ == "__main__":
    PaintApp()