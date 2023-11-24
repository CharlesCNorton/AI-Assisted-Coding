import datetime
import ephem
from skyfield.api import Topos, load
from skyfield.errors import EphemerisRangeError
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import clear, set_title

# Load timescale for skyfield
ts = load.timescale()

# Custom Exception for Moon Information Errors
class MoonInfoError(Exception):
    pass

# Moon Phase Class
class MoonPhase:
    def __init__(self):
        self.planets = load('de421.bsp')
        self.earth, self.moon = self.planets['earth'], self.planets['moon']

    def get_moon_info(self, date):
        try:
            observer = ephem.Observer()
            observer.date = ephem.Date(date.strftime('%Y/%m/%d'))
            moon = ephem.Moon(observer)
            previous_new_moon = ephem.previous_new_moon(observer.date)
            next_new_moon = ephem.next_new_moon(observer.date)
            phase = (observer.date - previous_new_moon) / (next_new_moon - previous_new_moon)
            t = ts.utc(date.year, date.month, date.day)
            geocentric = self.earth.at(t).observe(self.moon)
            _, _, distance = geocentric.radec()
        except (ValueError, TypeError, EphemerisRangeError) as e:
            raise MoonInfoError(f"Error in moon info: {str(e)}")
        return phase, distance.km

    def get_phase_name_and_desc(self, phase):
        phase_info = {
            'New Moon': ('🌑', 'Moon is directly between the Earth and the Sun and not visible from Earth.'),
            'Waxing Crescent': ('🌒', 'Moon is becoming more illuminated by direct sunlight.'),
            'First Quarter': ('🌓', 'Moon is a half circle, right side from Northern Hemisphere and left side from Southern Hemisphere is visible.'),
            'Waxing Gibbous': ('🌔', 'Moon is becoming more illuminated by direct sunlight.'),
            'Full Moon': ('🌕', 'Moon is fully visible from Earth, fully illuminated by direct sunlight.'),
            'Waning Gibbous': ('🌖', 'Moon is starting to become less illuminated by direct sunlight.'),
            'Last Quarter': ('🌗', 'Only the left half of the Moon is visible from Earth.'),
            'Waning Crescent': ('🌘', 'Moon is starting to become less illuminated by direct sunlight.'),
            'Should not happen': ('❓', 'Something went wrong.')
        }
        if phase < 0.02:
            phase_name = 'New Moon'
        elif 0.02 <= phase < 0.22:
            phase_name = 'Waxing Crescent'
        elif 0.22 <= phase < 0.27:
            phase_name = 'First Quarter'
        elif 0.27 <= phase < 0.47:
            phase_name = 'Waxing Gibbous'
        elif 0.47 <= phase < 0.53:
            phase_name = 'Full Moon'
        elif 0.53 <= phase < 0.72:
            phase_name = 'Waning Gibbous'
        elif 0.72 <= phase < 0.78:
            phase_name = 'Last Quarter'
        elif 0.78 <= phase < 0.98:
            phase_name = 'Waning Crescent'
        else:
            phase_name = 'New Moon'
        return phase_name, *phase_info[phase_name]

# UI Functions
def display_menu(console):
    menu_text = Text("MENU", justify="center", style="bold underline white")
    menu_text.append("\\n\\n1. Get Moon Phase for specific date", style="white")
    menu_text.append("\\n2. Get Moon Phase for today", style="white")
    menu_text.append("\\n3. Exit", style="white")
    console.print(Panel(menu_text, style="grey70"))

def validate_date(date_str):
    for date_format in ['%Y/%m/%d', '%Y-%m-%d', '%d/%m/%Y']:
        try:
            return datetime.datetime.strptime(date_str, date_format)
        except ValueError:
            continue
    raise ValueError("Invalid date format. Please use YYYY/MM/DD, YYYY-MM-DD, or DD/MM/YYYY.")
# Main Program Logic
def main():
    set_title("Moon Phase Checker")
    console = Console()
    moon_phase = MoonPhase()

    while True:
        clear()
        display_menu(console)
        choice = prompt("Select your choice: ")

        if choice == '1':
            date_str = console.input("Enter the date [bold cyan](YYYY/MM/DD, YYYY-MM-DD, or DD/MM/YYYY)[/bold cyan]: ")
            try:
                date = validate_date(date_str)
            except ValueError as e:
                console.print(f"[bold red]{str(e)}[/bold red]")
                continue
            show_moon_info(date, moon_phase, console)

        elif choice == '2':
            date = datetime.datetime.now()
            show_moon_info(date, moon_phase, console)

        elif choice == '3':
            break

        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

def show_moon_info(date, moon_phase, console):
    try:
        phase, distance = moon_phase.get_moon_info(date)
        phase_name, moon_pic, moon_desc = moon_phase.get_phase_name_and_desc(phase)
    except MoonInfoError as e:
        console.print(f"[bold red]{str(e)}[/bold red]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="dim", width=12)
    table.add_column("Moon Phase", style="dim", width=20)
    table.add_column("Illumination", style="dim", width=20)
    table.add_column("Moon", style="dim", width=8)
    table.add_column("Distance (km)", style="dim", width=15)
    table.add_row(
        date.strftime('%Y/%m/%d'),
        phase_name,
        f"{min(100, phase * 100):.2f}%",
        moon_pic,
        f"{distance:.2f}"
    )
    rprint("[bold cyan]Moon Phase Information:[/bold cyan]")
    console.print(table)
    rprint(f"[bold cyan]{moon_desc}[/bold cyan]")
    console.print("Press any key to return to the menu...", style="white")
    prompt()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[bold red]Program interrupted by user.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Unhandled error: {str(e)}[/bold red]")