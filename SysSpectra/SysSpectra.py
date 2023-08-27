import psutil
from GPUtil import getGPUs
from tkinter import Tk, RIGHT, BOTH, X, Button, ttk

class SysInfo(ttk.Frame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.style = ttk.Style()
        self.style.configure("BW.TFrame", background="white")

    def initUI(self):
        self.master.title("System Info")
        self.pack(fill=BOTH, expand=True)

        frame1 = ttk.Frame(self, style="BW.TFrame")
        frame1.pack(fill=X)
        vram_label = ttk.Label(frame1, text="VRAM: ", justify=RIGHT)
        vram_label.pack(side=RIGHT, padx=5, pady=5)

        frame2 = ttk.Frame(self, style="BW.TFrame")
        frame2.pack(fill=X)
        ram_label = ttk.Label(frame2, text="RAM: ", justify=RIGHT)
        ram_label.pack(side=RIGHT, padx=5, pady=5)

        self.night_mode = False
        self.vram_label = vram_label
        self.ram_label = ram_label
        night_mode_frame = ttk.Frame(self, style="BW.TFrame")
        night_mode_frame.pack(fill=X)

        self.night_mode_btn = Button(night_mode_frame, text="Night Mode", command=self.toggle_night_mode)
        self.night_mode_btn.pack(side=RIGHT, padx=5, pady=5)
        self.update_info()

    def toggle_night_mode(self):
        if self.night_mode:
            self.style.configure("BW.TFrame", background="white")
            self.vram_label.config(background="white", foreground="black")
            self.ram_label.config(background="white", foreground="black")
            self.night_mode_btn.config(text="Night Mode")
        else:
            self.style.configure("BW.TFrame", background="black")
            self.vram_label.config(background="black", foreground="white")
            self.ram_label.config(background="black", foreground="white")
            self.night_mode_btn.config(text="Day Mode")
        self.night_mode = not self.night_mode

    def update_info(self):
        try:
            GPUs = getGPUs()
            gpu = GPUs[0]
            vram_perc = round(gpu.memoryUsed / gpu.memoryTotal * 100, 2)
            self.vram_label.config(text=f"VRAM: {vram_perc}%")
        except Exception as e:
            self.vram_label.config(text=f"VRAM: error {str(e)}")

        ram = psutil.virtual_memory()
        ram_perc = round(ram.used / ram.total * 100, 2)
        self.ram_label.config(text=f"RAM: {ram_perc}%")
        self.after(1000, self.update_info)

def main():
    root = Tk()
    root.geometry("200x100+1000+10")
    app = SysInfo()
    root.mainloop()

if __name__ == '__main__':
    main()
