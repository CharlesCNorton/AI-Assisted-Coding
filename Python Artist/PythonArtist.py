# The following program was created using GPT-4 on June 15, 2023.
# This program is a simple paint application created using the tkinter library in Python. It allows users to draw on a canvas using various tools such as a brush, line,
# rectangle, and eraser. Users can also choose the brush color and size, clear the canvas, undo previous actions, save the drawing as an image, and load an image to edit.

import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import ImageDraw, Image, ImageTk

def paint(event):
    global lastx, lasty, draw
    x, y = event.x, event.y
    if lastx is not None and lasty is not None:
        if current_tool.get() == "brush":
            draw.line((lastx, lasty, x, y), fill=brush_color.get(), width=brush_size.get())
            canvas.create_line(lastx, lasty, x, y, fill=brush_color.get(), width=brush_size.get())
        elif current_tool.get() == "line":
            canvas.delete("temp_line")
            canvas.create_line(startx, starty, x, y, tags="temp_line", fill=brush_color.get(), width=brush_size.get())
        elif current_tool.get() == "eraser":
            draw.line((lastx,lasty,x,y),fill="white",width=brush_size.get())
            canvas.create_line(lastx,lasty,x,y,fill="white",width=brush_size.get())
    lastx,lasty=x,y

def reset_coords(event):
    global startx,starty
    startx,starty=event.x,event.y

def draw_shape(event):
    global draw
    x,y=event.x,event.y
    if current_tool.get() == "line":
        canvas.delete("temp_line")
        draw.line((startx,starty,x,y),fill=brush_color.get(),width=brush_size.get())
        canvas.create_line(startx,starty,x,y,fill=brush_color.get(),width=brush_size.get())
    elif current_tool.get() == "rectangle":
        draw.rectangle((startx,starty,x,y),outline=brush_color.get(),width=brush_size.get())
        canvas.create_rectangle(startx,starty,x,y,outline=brush_color.get(),width=brush_size.get())

def clear_canvas():
    global draw
    canvas.delete("all")
    draw.rectangle((0,0,image.width,image.height),fill="white")

def undo():
    global undo_stack
    if len(undo_stack) > 0:
        img = undo_stack.pop()
        image.paste(img)
        canvas.image = ImageTk.PhotoImage(image)
        canvas.create_image(0,0,image=canvas.image,anchor=tk.NW)

def save():
    filename = filedialog.asksaveasfilename(defaultextension=".png")
    if filename:
        image.save(filename)

def load():
    global image,draw
    filename = filedialog.askopenfilename(filetypes=[("Image Files","*.png;*.jpg;*.jpeg")])
    if filename:
        clear_canvas()
        image = Image.open(filename)
        draw = ImageDraw.Draw(image)
        canvas.image = ImageTk.PhotoImage(image)
        canvas.create_image(0,0,image=canvas.image,anchor=tk.NW)

def choose_color():
    color = colorchooser.askcolor()[1]
    if color:
        brush_color.set(color)

root = tk.Tk()
root.title("Paint")

lastx,lasty=None,None
startx,starty=None,None

current_tool=tk.StringVar(value="brush")
brush_color=tk.StringVar(value="black")
brush_size=tk.IntVar(value=5)

canvas_frame=tk.Frame(root,bd=2,bg="black")
canvas_frame.pack(padx=10,pady=10)

canvas=tk.Canvas(canvas_frame,width=400,height=400,bg="white")
canvas.pack(expand=tk.YES,fill=tk.BOTH)
canvas.bind("<B1-Motion>",paint)
canvas.bind("<Button-1>",reset_coords)
canvas.bind("<ButtonRelease-1>",draw_shape)

image = Image.new("RGB",(400,400),"white")
draw = ImageDraw.Draw(image)
undo_stack=[]

tool_frame=tk.Frame(root)
tool_frame.pack(side=tk.TOP)

tools=["brush","line","rectangle","eraser"]
for tool in tools:
    b=tk.Radiobutton(tool_frame,text=tool.capitalize(),variable=current_tool,value=tool)
    b.pack(side=tk.LEFT)

color_button=tk.Button(tool_frame,text="Choose Color",command=choose_color)
color_button.pack(side=tk.LEFT)

size_frame=tk.Frame(root)
size_frame.pack(side=tk.TOP)

sizes=[1,3,5,7,9]
for size in sizes:
    b=tk.Radiobutton(size_frame,text=str(size),variable=brush_size,value=size)
    b.pack(side=tk.LEFT)

clear_button=tk.Button(root,text="Clear",command=clear_canvas)
clear_button.pack(side=tk.BOTTOM)

undo_button=tk.Button(root,text="Undo",command=undo)
undo_button.pack(side=tk.BOTTOM)

save_button=tk.Button(root,text="Save",command=save)
save_button.pack(side=tk.BOTTOM)

load_button=tk.Button(root,text="Load",command=load)
load_button.pack(side=tk.BOTTOM)

message=tk.Label(root,text="Press and Drag the mouse to draw")
message.pack(side=tk.BOTTOM)

root.mainloop()
