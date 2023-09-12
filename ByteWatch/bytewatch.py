import psutil
from GPUtil import getGPUs
from tkinter import Tk, RIGHT, BOTH, X, Button, ttk

class SystemMetrics:
    @staticmethod
    def get_RAM_usage():
        ram = psutil.virtual_memory()
        return round(ram.used / ram.total * 100, 2)

    @staticmethod
    def get_VRAM_usage():
        try:
            gpu = getGPUs()[0]
            return round(gpu.memoryUsed / gpu.memoryTotal * 100, 2)
        except (IndexError, Exception):
            return None

class SysInfo(ttk.Frame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.night_mode = False
        self.metrics = {"VRAM": None, "RAM": SystemMetrics.get_RAM_usage}
        self.labels = {}
        self.update_info()

    def initUI(self):
        self.master.title("System Info")
        self.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.style = ttk.Style()
        self.style.configure("BW.TFrame", background="white")

        for metric, _ in self.metrics.items():
            self.labels[metric] = self.create_label(f"{metric}: ", metric.lower())

        night_mode_frame = ttk.Frame(self, style="BW.TFrame")
        night_mode_frame.pack(fill=X)
        self.night_mode_btn = Button(night_mode_frame, text="Night Mode", command=self.toggle_night_mode)
        self.night_mode_btn.pack(side=RIGHT, padx=5, pady=5)

    def create_label(self, text, label_name):
        frame = ttk.Frame(self, style="BW.TFrame")
        frame.pack(fill=X)
        label = ttk.Label(frame, text=text, justify=RIGHT)
        label.pack(side=RIGHT, padx=5, pady=5)
        return label

    def get_colors(self):
        return ("black", "white") if self.night_mode else ("white", "black")

    def toggle_night_mode(self):
        bg, fg = self.get_colors()
        self.style.configure("BW.TFrame", background=bg)
        for label in self.labels.values():
            label.config(background=bg, foreground=fg)
        self.night_mode_btn.config(text="Day Mode" if self.night_mode else "Night Mode")
        self.night_mode = not self.night_mode

    def update_info(self):
        for metric, func in self.metrics.items():
            value = func() if func else None
            self.labels[metric].config(text=f"{metric}: {value if value is not None else 'Not available'}%")
        self.after(1000, self.update_info)

def main():
    root = Tk()
    root.geometry("230x120+1000+10")
    root.attributes('-topmost', True)
    app = SysInfo()
    root.mainloop()

if __name__ == '__main__':
    main()