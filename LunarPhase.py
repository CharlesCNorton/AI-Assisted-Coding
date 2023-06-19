#LunarPhase
#Moon Phase Checker application with menu, moon phase calculation, and display functionality.
#Made with GPT-4 on June 19th 2023.
import datetime
import ephem
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import clear, print_formatted_text as pft, set_title
import skyfield
from skyfield.api import Topos, load
ts = load.timescale()
console = Console()
def display_menu(console):
    menu_text = Text("MENU", justify="center", style="bold underline white")
    menu_text.append("\n\n1. Get Moon Phase for specific date", style="white")
    menu_text.append("\n2. Get Moon Phase for today", style="white")
    menu_text.append("\n3. Exit", style="white")
    console.print(Panel(menu_text, style="grey70"))
def get_moon_info(date):
    try:
        observer = ephem.Observer()
        observer.date = ephem.Date(date)
        moon = ephem.Moon(observer)
        previous_new_moon = ephem.previous_new_moon(date)
        next_new_moon = ephem.next_new_moon(date)
        phase = (observer.date - previous_new_moon) / (next_new_moon - previous_new_moon)
        planets = load('de421.bsp')
        earth, moon = planets['earth'], planets['moon']
        t = ts.utc(date.year, date.month, date.day)
        geocentric = earth.at(t).observe(moon)
    except (ValueError, TypeError) as e:
        console.print(f"[bold red]Error occurred while calculating moon phase: {str(e)}[/bold red]")
        console.print(f"[bold red]Please ensure the date is in the correct format (YYYY/MM/DD).[/bold red]")
        return None
    except skyfield.errors.EphemerisRangeError as e:
        console.print(f"[bold red]The date provided is out of range. Please provide a date between 1899-07-29 and 2053-10-09.[/bold red]")
        return None
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {str(e)}[/bold red]")
        return None
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
    moon_pic, moon_desc = phase_info[phase_name]
    planets = load('de421.bsp')
    earth, moon = planets['earth'], planets['moon']
    t = ts.utc(date.year, date.month, date.day)
    geocentric = earth.at(t).observe(moon)
    _, _, distance = geocentric.radec()
    return phase_name, phase, moon_pic, moon_desc, distance.km
def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y/%m/%d')
        return True
    except ValueError:
        return False
def main():
    set_title("Moon Phase Checker")
    console = Console()
    while True:
        clear()
        display_menu(console)
        choice = prompt("Select your choice: ")
        if choice == '1':
            date_str = console.input("Enter the date [bold cyan](yyyy/mm/dd)[/bold cyan]: ")
            if not validate_date(date_str):
                console.print("[bold red]Invalid date format. Please use yyyy/mm/dd.[/bold red]")
                continue
            show_moon_info(date_str, console)
        elif choice == '2':
            date_str = datetime.datetime.now().strftime('%Y/%m/%d')
            show_moon_info(date_str, console)
        elif choice == '3':
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")
            continue
def show_moon_info(date_str, console):
    date = datetime.datetime.strptime(date_str, '%Y/%m/%d')
    moon_info = get_moon_info(date)
    if moon_info is None:
        console.print("[bold red]Unable to fetch moon info. Please try again later.[/bold red]")
        return
    phase, percent_illuminated, moon_pic, moon_desc, distance = moon_info
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="dim", width=12)
    table.add_column("Moon Phase", style="dim", width=20)
    table.add_column("Illumination", style="dim", width=20)
    table.add_column("Moon", style="dim", width=8)
    table.add_column("Distance (km)", style="dim", width=15)
    table.add_row(
        date_str,
        phase,
        f"{min(100, percent_illuminated * 100):.2f}%",
        moon_pic,
        f"{distance:.2f}"
    )
    rprint("[bold cyan]Moon Phase Information:[/bold cyan]")
    console.print(table)
    rprint(f"[bold cyan]{moon_desc}[/bold cyan]")
    console.print("Press any key to return to the menu...", style="white")
    input()
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[bold red]Program interrupted by user.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Unhandled error: {str(e)}[/bold red]")
