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
def display_menu(console):
    menu_text = Text("MENU", justify="center", style="bold underline")
    menu_text.append("\n\n1. Get Moon Phase for specific date")
    menu_text.append("\n2. Get Moon Phase for today")
    menu_text.append("\n3. Exit")
    console.print(Panel(menu_text))
def get_moon_phase(date):
    observer = ephem.Observer()
    observer.date = ephem.Date(date)
    moon = ephem.Moon(observer)
    previous_new_moon = ephem.previous_new_moon(date)
    next_new_moon = ephem.next_new_moon(date)
    phase = (observer.date - previous_new_moon) / (next_new_moon - previous_new_moon)
    ascii_moon = {
        'New Moon': '🌑',
        'Waxing Crescent': '🌒',
        'First Quarter': '🌓',
        'Waxing Gibbous': '🌔',
        'Full Moon': '🌕',
        'Should not happen': '❓'
    }
    if phase < 0.03 or phase >= 0.97:
        phase_name = 'New Moon'
    elif 0.03 <= phase < 0.22:
        phase_name = 'Waxing Crescent'
    elif 0.22 <= phase < 0.47:
        phase_name = 'First Quarter'
    elif 0.47 <= phase < 0.72:
        phase_name = 'Waxing Gibbous'
    elif 0.72 <= phase < 0.97:
        phase_name = 'Full Moon'
    else:
        phase_name = 'Should not happen'
    return phase_name, phase, ascii_moon[phase_name]
def main():
    set_title("Moon Phase Checker")
    console = Console()
    while True:
        clear()
        display_menu(console)
        choice = prompt("Select your choice: ")
        if choice == '1':
            date_str = console.input("Enter the date [bold cyan](yyyy/mm/dd)[/bold cyan]: ")
            show_moon_phase(date_str, console)
        elif choice == '2':
            date_str = datetime.datetime.now().strftime('%Y/%m/%d')
            show_moon_phase(date_str, console)
        elif choice == '3':
            break
        else:
            console.print("[bold red]Invalid choice. Please choose an option from the menu (1, 2, or 3).[/bold red]")
def show_moon_phase(date_str, console):
    try:
        date = datetime.datetime.strptime(date_str, '%Y/%m/%d')
        phase, percent_illuminated, moon_pic = get_moon_phase(date)
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Date", style="dim", width=12)
        table.add_column("Moon Phase", style="dim", width=20)
        table.add_column("Illumination", style="dim", width=20)
        table.add_column("Moon", style="dim", width=8)
        table.add_row(
            date_str,
            phase,
            f"{min(100, percent_illuminated * 100):.2f}%",
            moon_pic
        )
        rprint("[bold cyan]Moon Phase Information:[/bold cyan]")
        console.print(table)
    except ValueError:
        rprint("[bold red]Invalid date format. Please use yyyy/mm/dd.[/bold red]")
    console.input("Press any key to return to the menu...")
if __name__ == "__main__":
    main()
