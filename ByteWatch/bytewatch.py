import psutil
from GPUtil import getGPUs
from tkinter import Tk, RIGHT, BOTH, X, Button, ttk

class SysInfo(ttk.Frame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.night_mode = False
        self.update_info()

    def initUI(self):
        self.master.title("System Info")
        self.pack(fill=BOTH, expand=True)

        self.style = ttk.Style()
        self.style.configure("BW.TFrame", background="white")

        self.create_frame("VRAM: ", "vram_label")
        self.create_frame("RAM: ", "ram_label")

        night_mode_frame = ttk.Frame(self, style="BW.TFrame")
        night_mode_frame.pack(fill=X)

        self.night_mode_btn = Button(night_mode_frame, text="Night Mode", command=self.toggle_night_mode)
        self.night_mode_btn.pack(side=RIGHT, padx=5, pady=5)

    def create_frame(self, text, label_name):
        frame = ttk.Frame(self, style="BW.TFrame")
        frame.pack(fill=X)
        label = ttk.Label(frame, text=text, justify=RIGHT)
        label.pack(side=RIGHT, padx=5, pady=5)
        setattr(self, label_name, label)

    def toggle_night_mode(self):
        colors = ("black", "white") if self.night_mode else ("white", "black")
        self.style.configure("BW.TFrame", background=colors[0])
        self.vram_label.config(background=colors[0], foreground=colors[1])
        self.ram_label.config(background=colors[0], foreground=colors[1])
        self.night_mode_btn.config(text="Day Mode" if self.night_mode else "Night Mode")
        self.night_mode = not self.night_mode

    def update_info(self):
        self.update_VRAM()
        self.update_RAM()
        self.after(1000, self.update_info)

    def update_VRAM(self):
        try:
            gpu = getGPUs()[0]
            vram_perc = round(gpu.memoryUsed / gpu.memoryTotal * 100, 2)
            self.vram_label.config(text=f"VRAM: {vram_perc}%")
        except IndexError:
            self.vram_label.config(text="VRAM: Not available")

    def update_RAM(self):
        ram = psutil.virtual_memory()
        ram_perc = round(ram.used / ram.total * 100, 2)
        self.ram_label.config(text=f"RAM: {ram_perc}%")

def main():
    root = Tk()
    root.geometry("200x100+1000+10")
    root.attributes('-topmost', True)
    app = SysInfo()
    root.mainloop()

if __name__ == '__main__':
    main()
