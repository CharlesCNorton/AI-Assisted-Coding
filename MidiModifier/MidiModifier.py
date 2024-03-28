import mido
from mido import MidiFile, MidiTrack
from tkinter import Tk, filedialog
from colorama import Fore, init

init(autoreset=True)


class MidiModifier:
    def __init__(self):
        self.input_file = ""
        self.output_file = ""

    def run(self):
        while True:
            self.display_menu()
            choice = input(Fore.LIGHTGREEN_EX + "Enter your choice (1-2): ")
            if choice == "1":
                self.handle_conversion()
            elif choice == "2":
                print(Fore.MAGENTA + "Exiting the program. Goodbye!")
                break
            else:
                print(Fore.RED + "Invalid choice. Please enter 1 or 2.")

    def display_menu(self):
        print(Fore.YELLOW + "\nMIDI Modifier")
        print(Fore.CYAN + "1. Convert a MIDI file")
        print(Fore.CYAN + "2. Exit")

    def handle_conversion(self):
        self.input_file = self.select_file("Select the input MIDI file", [("MIDI files", "*.mid *.midi")])
        if not self.input_file:
            print(Fore.RED + "No input file selected. Returning to the main menu.")
            return

        self.output_file = self.select_output_file("Save the output MIDI file as", [("MIDI files", "*.mid *.midi")])
        if not self.output_file:
            print(Fore.RED + "No output file selected. Returning to the main menu.")
            return

        self.convert_to_two_tracks()

    @staticmethod
    def select_file(title, filetypes):
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        root.destroy()
        return file_path

    @staticmethod
    def select_output_file(title, filetypes):
        root = Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(title=title, filetypes=filetypes, defaultextension=filetypes)
        root.destroy()
        return file_path

    def convert_to_two_tracks(self):
        try:
            original_midi = MidiFile(self.input_file)
            new_midi = MidiFile(ticks_per_beat=original_midi.ticks_per_beat)
            combined_track = MidiTrack()
            new_midi.tracks.append(combined_track)

            for track in original_midi.tracks:
                for msg in track:
                    if not msg.is_meta and msg.type not in ['track_name', 'instrument_name']:
                        combined_track.append(msg.copy())
                    elif msg.is_meta and combined_track not in new_midi.tracks:
                        combined_track.append(msg.copy())

            new_midi.tracks.append(MidiTrack())
            new_midi.save(self.output_file)
            print(f"{Fore.GREEN}Successfully converted and saved as {self.output_file}")
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}")


if __name__ == "__main__":
    MidiModifier().run()
