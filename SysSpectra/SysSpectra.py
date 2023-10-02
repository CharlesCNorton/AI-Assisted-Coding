# Import necessary libraries:
# psutil: for system utilities like CPU and RAM usage.
# GPUtil: for GPU usage and related info.
# tkinter: for creating the GUI.
import psutil
from GPUtil import getGPUs
from tkinter import Tk, RIGHT, BOTH, X, Button, Frame, Label

# Set refresh rate constant for how frequently the tool updates system stats.
REFRESH_RATE = 1000

class SysInfo(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Toggle flag for night mode.
        self.night_mode = False
        
        # Define the themes for day and night mode.
        self.themes = {
            "day": {
                "bg": "white",
                "fg": "black",
                "btn_text": "Night Mode"
            },
            "night": {
                "bg": "black",
                "fg": "white",
                "btn_text": "Day Mode"
            }
        }
        
        # Initialize the GUI.
        self.initUI()
        
        # Update system info.
        self.update_info()
        
        # Set the default theme to day mode.
        self.set_theme("day")

    def initUI(self):
        # Set title for the main window.
        self.master.title("System Info")
        
        # Pack the main frame.
        self.pack(fill=BOTH, expand=True)

        # Initialize all the subframes.
        self.initFrames()
        
        # Initialize labels.
        self.initLabels()
        
        # Initialize buttons.
        self.initButtons()

    def initFrames(self):
        # Define frames to hold various system info components.
        self.frame1 = Frame(self)
        self.frame1.pack(fill=X, padx=10, pady=5)

        # ...repeat for other frames.
        self.frame2 = Frame(self)
        self.frame2.pack(fill=X, padx=10, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(fill=X, padx=10, pady=5)

        self.frame4 = Frame(self)
        self.frame4.pack(fill=X, padx=10, pady=5)

        # Frame for the night mode toggle button.
        self.night_mode_frame = Frame(self)
        self.night_mode_frame.pack(fill=X, pady=10)

    def initLabels(self):
        # Label to display VRAM usage.
        self.vram_label = Label(self.frame1, justify=RIGHT, text="VRAM:")
        self.vram_label.pack(side=RIGHT, padx=5)

        # ...repeat for other labels.
        self.gpu_util_label = Label(self.frame2, justify=RIGHT, text="GPU Util:")
        self.gpu_util_label.pack(side=RIGHT, padx=5)

        self.ram_label = Label(self.frame3, justify=RIGHT, text="RAM:")
        self.ram_label.pack(side=RIGHT, padx=5)

        self.cpu_util_label = Label(self.frame4, justify=RIGHT, text="CPU Util:")
        self.cpu_util_label.pack(side=RIGHT, padx=5)

    def initButtons(self):
        # Button to toggle night mode on and off.
        self.night_mode_btn = Button(self.night_mode_frame, command=self.toggle_night_mode)
        self.night_mode_btn.pack(side=RIGHT, padx=5)

    def toggle_night_mode(self):
        # Determine which theme to switch to based on current theme.
        theme = "night" if not self.night_mode else "day"
        self.set_theme(theme)
        self.night_mode = not self.night_mode

    def set_theme(self, theme_name):
        # Fetch the theme details.
        theme = self.themes[theme_name]
        bg_color = theme["bg"]
        fg_color = theme["fg"]
        btn_text = theme["btn_text"]

        # Apply the theme to various components.
        self.master.config(bg=bg_color)
        for frame in [self, self.frame1, self.frame2, self.frame3, self.frame4, self.night_mode_frame]:
            frame.config(bg=bg_color)

        for label in [self.vram_label, self.gpu_util_label, self.ram_label, self.cpu_util_label]:
            label.config(bg=bg_color, fg=fg_color)

        self.night_mode_btn.config(text=btn_text, bg=bg_color, fg=fg_color)

    def update_info(self):
        # Fetch and display GPU info.
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
            self.vram_label.config(text=f"Error: {str(e)}")
            self.gpu_util_label.config(text=f"Error: {str(e)}")

        # Fetch and display RAM info.
        ram = psutil.virtual_memory()
        ram_perc = round(ram.used / ram.total * 100, 2)
        self.ram_label.config(text=f"RAM: {ram_perc}%")

        # Fetch and display CPU usage.
        cpu_util = round(psutil.cpu_percent(interval=0), 2)
        self.cpu_util_label.config(text=f"CPU Util: {cpu_util}%")

        # Call update_info again after the REFRESH_RATE duration.
        self.after(REFRESH_RATE, self.update_info)

def main():
    # Initialize the main window.
    root = Tk()
    app = SysInfo()
    root.update()

    # Center the application on the screen.
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    # Make sure the application stays on top.
    root.attributes('-topmost', True)
    
    # Run the mainloop for the GUI.
    root.mainloop()

if __name__ == '__main__':
    main()