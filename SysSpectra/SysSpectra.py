import psutil
from GPUtil import getGPUs
from tkinter import Tk, RIGHT, BOTH, X, Button, ttk

REFRESH_RATE = 1000

class SysInfo(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style = ttk.Style()
        self.night_mode = False
        self.initUI()
        self.update_info()

    def initUI(self):
        self.master.title("System Info")
        self.pack(fill=BOTH, expand=True)

        self.initFrames()
        self.initLabels()
        self.initButtons()

    def initFrames(self):
        self.frame1 = ttk.Frame(self, style="BW.TFrame")
        self.frame1.pack(fill=X)

        self.frame2 = ttk.Frame(self, style="BW.TFrame")
        self.frame2.pack(fill=X)

        self.frame3 = ttk.Frame(self, style="BW.TFrame")
        self.frame3.pack(fill=X)

        self.frame4 = ttk.Frame(self, style="BW.TFrame")
        self.frame4.pack(fill=X)

        self.night_mode_frame = ttk.Frame(self, style="BW.TFrame")
        self.night_mode_frame.pack(fill=X)

    def initLabels(self):
        self.vram_label = ttk.Label(self.frame1, text="VRAM: ", justify=RIGHT)
        self.vram_label.pack(side=RIGHT, padx=5, pady=5)

        self.gpu_util_label = ttk.Label(self.frame2, text="GPU Util: ", justify=RIGHT)
        self.gpu_util_label.pack(side=RIGHT, padx=5, pady=5)

        self.ram_label = ttk.Label(self.frame3, text="RAM: ", justify=RIGHT)
        self.ram_label.pack(side=RIGHT, padx=5, pady=5)

        self.cpu_util_label = ttk.Label(self.frame4, text="CPU Util: ", justify=RIGHT)
        self.cpu_util_label.pack(side=RIGHT, padx=5, pady=5)

    def initButtons(self):
        self.night_mode_btn = Button(self.night_mode_frame, text="Night Mode", command=self.toggle_night_mode)
        self.night_mode_btn.pack(side=RIGHT, padx=5, pady=5)

    def toggle_night_mode(self):
        if self.night_mode:
            self.set_theme("white", "black", "Night Mode")
        else:
            self.set_theme("black", "white", "Day Mode")
        self.night_mode = not self.night_mode

    def set_theme(self, bg_color, fg_color, btn_text):
        self.style.configure("BW.TFrame", background=bg_color)
        self.vram_label.config(background=bg_color, foreground=fg_color)
        self.ram_label.config(background=bg_color, foreground=fg_color)
        self.cpu_util_label.config(background=bg_color, foreground=fg_color)
        self.gpu_util_label.config(background=bg_color, foreground=fg_color)
        self.night_mode_btn.config(text=btn_text)

    def update_info(self):
        try:
            GPUs = getGPUs()
            gpu = GPUs[0]
            vram_perc = round(gpu.memoryUsed / gpu.memoryTotal * 100, 2)
            gpu_util = round(gpu.load * 100, 2)
            self.vram_label.config(text=f"VRAM: {vram_perc}%")
            self.gpu_util_label.config(text=f"GPU Util: {gpu_util}%")
        except IndexError:
            self.vram_label.config(text="VRAM: GPU not found")
            self.gpu_util_label.config(text="GPU Util: GPU not found")
        except Exception as e:
            self.vram_label.config(text=f"VRAM: error {str(e)}")
            self.gpu_util_label.config(text=f"GPU Util: error {str(e)}")

        ram = psutil.virtual_memory()
        ram_perc = round(ram.used / ram.total * 100, 2)
        self.ram_label.config(text=f"RAM: {ram_perc}%")

        cpu_util = round(psutil.cpu_percent(interval=1), 2)
        self.cpu_util_label.config(text=f"CPU Util: {cpu_util}%")

        self.after(REFRESH_RATE, self.update_info)

def main():
    root = Tk()
    root.geometry("300x150+1000+10")
    app = SysInfo()
    root.mainloop()

if __name__ == '__main__':
    main()
