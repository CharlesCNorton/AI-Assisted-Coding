import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import ImageDraw, Image, ImageTk

class PaintApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Paint")
        self.current_tool = tk.StringVar(value="brush")
        self.brush_color = tk.StringVar(value="black")
        self.brush_size = tk.IntVar(value=5)
        self.fill_type = tk.StringVar(value="solid")  # New variable for fill type
        self.lastx = self.lasty = self.startx = self.starty = None
        self.image = Image.new("RGB", (400, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.undo_stack = []
        self.redo_stack = []
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.create_canvas()
        self.create_tool_buttons()
        self.create_size_buttons()
        self.create_bottom_buttons()
        self.create_message()

    def create_canvas(self):
        self.canvas_frame = tk.Frame(self.root, bd=2, bg="black")
        self.canvas_frame.pack(padx=10, pady=10)
        self.canvas = tk.Canvas(self.canvas_frame, width=400, height=400, bg="white")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.reset_coords)
        self.canvas.bind("<ButtonRelease-1>", self.draw_shape)

    def create_tool_buttons(self):
        self.tool_frame = tk.Frame(self.root)
        self.tool_frame.pack(side=tk.TOP)
        tools = ["brush", "line", "rectangle", "eraser"]
        for tool in tools:
            b = tk.Radiobutton(self.tool_frame, text=tool.capitalize(), variable=self.current_tool, value=tool)
            b.pack(side=tk.LEFT)
        self.color_button = tk.Button(self.tool_frame, text="Choose Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

    def create_size_buttons(self):
        self.size_frame = tk.Frame(self.root)
        self.size_frame.pack(side=tk.TOP)
        sizes = [1, 3, 5, 7, 9]
        for size in sizes:
            b = tk.Radiobutton(self.size_frame, text=str(size), variable=self.brush_size, value=size)
            b.pack(side=tk.LEFT)

    def create_bottom_buttons(self):
        self.clear_button = tk.Button(self.root, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(side=tk.BOTTOM)
        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.BOTTOM)
        self.redo_button = tk.Button(self.root, text="Redo", command=self.redo)
        self.redo_button.pack(side=tk.BOTTOM)
        self.save_button = tk.Button(self.root, text="Save Image", command=self.save)
        self.save_button.pack(side=tk.BOTTOM)
        self.load_button = tk.Button(self.root, text="Load Image", command=self.load)
        self.load_button.pack(side=tk.BOTTOM)

        # Fill Type Buttons
        self.fill_type_frame = tk.Frame(self.root)
        self.fill_type_frame.pack(side=tk.TOP)
        fill_types = ["solid", "gradient", "pattern"]
        for fill_type in fill_types:
            b = tk.Radiobutton(self.fill_type_frame, text=fill_type.capitalize(), variable=self.fill_type, value=fill_type)
            b.pack(side=tk.LEFT)

    def create_message(self):
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
        self.save_state_for_undo()

    def reset_coords(self, event):
        self.startx, self.starty = self.lastx, self.lasty = event.x, event.y

    def draw_shape(self, event):
        x, y = event.x, event.y
        if self.current_tool.get() == "rectangle":
            if self.fill_type.get() == "gradient":
                fill_image = self.linear_gradient("red", "blue", abs(x - self.startx), abs(y - self.starty))
                self.draw.rectangle((self.startx, self.starty, x, y), fill=fill_image)
            elif self.fill_type.get() == "pattern":
                pattern_image = self.create_pattern_image()  # Placeholder for pattern image
                fill_image = self.create_pattern_fill(pattern_image, abs(x - self.startx), abs(y - self.starty))
                self.draw.rectangle((self.startx, self.starty, x, y), fill=fill_image)
            else:
                self.draw.rectangle((self.startx, self.starty, x, y), outline=self.brush_color.get(), width=self.brush_size.get())

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle((0, 0, self.image.width, self.image.height), fill="white")
        self.save_state_for_undo()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.undo_stack.pop())
            self.update_canvas_image(self.undo_stack[-1] if self.undo_stack else Image.new("RGB", (400, 400), "white"))

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.update_canvas_image(self.undo_stack[-1])

    def update_canvas_image(self, image):
        self.image = image
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor=tk.NW)

    def save_state_for_undo(self):
        self.undo_stack.append(self.image.copy())
        self.redo_stack.clear()

    def save(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".png")
            if filename:
                self.image.save(filename)
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def load(self):
        try:
            filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if filename:
                self.clear_canvas()
                self.image = Image.open(filename)
                self.draw = ImageDraw.Draw(self.image)
                self.update_canvas_image(self.image)
        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.brush_color.set(color)

    def linear_gradient(self, start_color, end_color, width, height):
        base = Image.new('RGB', (width, height), start_color)
        top = Image.new('RGB', (width, height), end_color)
        mask = Image.new('L', (width, height))
        mask_data = []
        for y in range(height):
            mask_data.extend([int(255 * (y / height))] * width)
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base

    def create_pattern_fill(self, pattern_image, width, height):
        pattern_width, pattern_height = pattern_image.size
        base = Image.new('RGB', (width, height), "white")
        for i in range(0, width, pattern_width):
            for j in range(0, height, pattern_height):
                base.paste(pattern_image, (i, j))
        return base

    def create_pattern_image(self):
        return Image.new('RGB', (10, 10), "black")

if __name__ == "__main__":
    PaintApp()