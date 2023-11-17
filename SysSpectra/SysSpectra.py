import logging
import psutil
from GPUtil import getGPUs
from tkinter import Tk, RIGHT, BOTH, X, Button, Frame, Label

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REFRESH_RATE = 2000

class SysInfo(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.night_mode = False
        self.themes = {
            "day": {"bg": "white", "fg": "black", "btn_text": "Night Mode"},
            "night": {"bg": "black", "fg": "white", "btn_text": "Day Mode"}
        }
        self.initUI()
        self.set_theme("day")
        self.update_info()

    def initUI(self):
        self.master.title("System Info")
        self.pack(fill=BOTH, expand=True)
        self.initFrames()
        self.initLabels()
        self.initButtons()

    def initFrames(self):
        self.frame1 = Frame(self)
        self.frame1.pack(fill=X, padx=10, pady=5)
        self.frame2 = Frame(self)
        self.frame2.pack(fill=X, padx=10, pady=5)
        self.frame3 = Frame(self)
        self.frame3.pack(fill=X, padx=10, pady=5)
        self.frame4 = Frame(self)
        self.frame4.pack(fill=X, padx=10, pady=5)
        self.night_mode_frame = Frame(self)
        self.night_mode_frame.pack(fill=X, pady=10)

    def initLabels(self):
        self.vram_label = Label(self.frame1, justify=RIGHT, text="VRAM:")
        self.vram_label.pack(side=RIGHT, padx=5)
        self.gpu_util_label = Label(self.frame2, justify=RIGHT, text="GPU Util:")
        self.gpu_util_label.pack(side=RIGHT, padx=5)
        self.ram_label = Label(self.frame3, justify=RIGHT, text="RAM:")
        self.ram_label.pack(side=RIGHT, padx=5)
        self.cpu_util_label = Label(self.frame4, justify=RIGHT, text="CPU Util:")
        self.cpu_util_label.pack(side=RIGHT, padx=5)

    def initButtons(self):
        self.night_mode_btn = Button(self.night_mode_frame, command=self.toggle_night_mode)
        self.night_mode_btn.pack(side=RIGHT, padx=5)

    def toggle_night_mode(self):
        self.night_mode = not self.night_mode
        theme = "night" if self.night_mode else "day"
        self.set_theme(theme)

    def set_theme(self, theme_name):
        theme = self.themes[theme_name]
        bg_color = theme["bg"]
        fg_color = theme["fg"]
        btn_text = theme["btn_text"]
        self.master.config(bg=bg_color)
        for frame in [self, self.frame1, self.frame2, self.frame3, self.frame4, self.night_mode_frame]:
            frame.config(bg=bg_color)
        for label in [self.vram_label, self.gpu_util_label, self.ram_label, self.cpu_util_label]:
            label.config(bg=bg_color, fg=fg_color)
        self.night_mode_btn.config(text=btn_text, bg=bg_color, fg=fg_color)

    def update_info(self):
        self.update_cpu_info()
        self.update_ram_info()
        self.update_gpu_info()
        self.after(REFRESH_RATE, self.update_info)

    def update_gpu_info(self):
        try:
            GPUs = getGPUs()
            if GPUs:
                gpu = GPUs[0]
                vram_perc = round(gpu.memoryUsed / gpu.memoryTotal * 100, 2)
                gpu_util = round(gpu.load * 100, 2)
                self.vram_label.config(text=f"VRAM: {vram_perc}%")
                self.gpu_util_label.config(text=f"GPU Util: {gpu_util}%")
        except Exception as e:
            logging.error(f"Failed to retrieve GPU information: {e}")
            self.vram_label.config(text="VRAM: N/A")
            self.gpu_util_label.config(text="GPU Util: N/A")

    def update_ram_info(self):
        try:
            ram = psutil.virtual_memory()
            ram_perc = round(ram.used / ram.total * 100, 2)
            self.ram_label.config(text=f"RAM: {ram_perc}%")
        except Exception as e:
            logging.error(f"Failed to retrieve RAM information: {e}")
            self.ram_label.config(text="RAM: N/A")

    def update_cpu_info(self):
        try:
            cpu_util = round(psutil.cpu_percent(interval=None), 2)
            self.cpu_util_label.config(text=f"CPU Util: {cpu_util}%")
        except Exception as e:
            logging.error(f"Failed to retrieve CPU utilization: {e}")
            self.cpu_util_label.config(text="CPU Util: N/A")

def main():
    root = Tk()
    root.geometry("250x200+300+300")
    app = SysInfo(master=root)
    root.mainloop()

if __name__ == '__main__':
    main()