import time
from colorama import Fore, Back, Style, init

class BattleSimulation:
    def __init__(self):
        init(autoreset=True)
        self.timeline = [
            {"time": "9:00", "event": "Norman army forms at the base of Senlac Hill", "morale_change": 1},
            {"time": "9:05", "event": "Norman scouts report the position of the English army", "morale_change": 2},
            {"time": "9:10", "event": "Norman knights attend mass, receive blessings", "morale_change": 3},
            {"time": "9:15", "event": "Norman army advances towards the English position", "morale_change": 4},
            {"time": "9:20", "event": "English scouts report the Norman movements", "morale_change": 5},
            {"time": "9:25", "event": "English shield wall takes shape atop Senlac Hill", "morale_change": 6},
            {"time": "9:30", "event": "English housecarls prepare for battle", "morale_change": 7},
            {"time": "9:35", "event": "Harold reviews his troops, boosting their morale", "morale_change": 8},
            {"time": "9:40", "event": "Norman archers prepare for the first volley", "morale_change": 9},
            {"time": "9:45", "event": "Norman archers advance and begin firing arrows", "morale_change": 10},
            {"time": "9:50", "event": "English shield wall withstands the arrow barrage", "morale_change": 11},
            {"time": "9:55", "event": "Norman infantry advance up the hill", "morale_change": 12},
            {"time": "10:00", "event": "Norman infantry engage the English shield wall", "morale_change": 13},
            {"time": "10:05", "event": "Fierce fighting continues between the two sides", "morale_change": 14},
            {"time": "10:10", "event": "English archers return fire, causing Norman casualties", "morale_change": 15},
            {"time": "10:15", "event": "Norman infantry pull back momentarily", "morale_change": 16},
            {"time": "10:20", "event": "William gives orders for a renewed assault", "morale_change": 17},
            {"time": "10:25", "event": "Norman archers let fly another volley of arrows", "morale_change": 18},
            {"time": "10:30", "event": "English housecarls surge down the hill, crashing into the Norman lines", "morale_change": 19},
            {"time": "10:35", "event": "Norman cavalry prepare for a flanking maneuver", "morale_change": 20},
            {"time": "10:40", "event": "Rumors of William's death cause momentary confusion in Norman ranks", "morale_change": 21},
            {"time": "10:45", "event": "William removes his helmet to show he is alive, rallying his troops", "morale_change": 22},
            {"time": "10:50", "event": "Norman cavalry charge at the English flank", "morale_change": 23},
            {"time": "10:55", "event": "English shield wall bends but does not break", "morale_change": 24},
            {"time": "11:00", "event": "Norman infantry and cavalry regroup for another assault", "morale_change": 25},
            {"time": "11:05", "event": "Heavy fighting continues, both sides suffer casualties", "morale_change": 26},
            {"time": "11:10", "event": "Normans execute a feigned retreat, drawing English forces out of position", "morale_change": 27},
            {"time": "11:15", "event": "English forces pursue, breaking their shield wall formation", "morale_change": 28},
            {"time": "11:20", "event": "Normans turn and counter-attack, catching English off guard", "morale_change": 29},
            {"time": "11:25", "event": "Harold Godwinson is seen rallying his troops on the front lines", "morale_change": 30},
            {"time": "11:30", "event": "William directs a concentrated attack on the English center", "morale_change": 31},
            {"time": "11:35", "event": "English forces try to reform their shield wall", "morale_change": 32},
            {"time": "11:40", "event": "Harold Godwinson falls, his eye pierced by a Norman arrow", "morale_change": 33},
            {"time": "11:45", "event": "News of Harold's death spreads, causing chaos in the English ranks", "morale_change": 34},
            {"time": "11:50", "event": "Normans press their advantage, pushing the English back", "morale_change": 35},
            {"time": "11:55", "event": "English housecarls, heartbroken and leaderless, begin their weary retreat", "morale_change": 36},
            {"time": "12:00", "event": "Normans continue their onslaught, leaving no quarter for the fleeing English", "morale_change": 37},
            {"time": "12:05", "event": "English forces scatter, some making a last stand", "morale_change": 38},
            {"time": "12:10", "event": "Victorious Normans establish their reign over the hill and surrounding lands", "morale_change": 39},
            {"time": "12:15", "event": "Norman soldiers gather their dead, the hill is silent but for the wind", "morale_change": 40},
            {"time": "12:20", "event": "Norman soldiers, unabashed, loot the fallen and nearby hamlets", "morale_change": 41},
            {"time": "12:25", "event": "William begins planning for the consolidation of his rule", "morale_change": 42},
            {"time": "12:30", "event": "In the wake of a bloody day, William the Conqueror is declared King of England", "morale_change": 43},
            {"time": "12:35", "event": "News of the Norman victory begins to spread, marking the beginning of a new era", "morale_change": 44}
        ]

        # List of morale changes, each index corresponds to the morale_change value in the timeline events
        self.morale_changes = [
            {"side": "Norman", "change": 5},
            {"side": "English", "change": -5},
            {"side": "Norman", "change": 5},
            {"side": "Norman", "change": 5},
            {"side": "English", "change": -5},
            {"side": "English", "change": 5},
            {"side": "English", "change": 5},
            {"side": "English", "change": 10},
            {"side": "Norman", "change": 5},
            {"side": "Norman", "change": 5, "side_2": "English", "change_2": -10},
            {"side": "English", "change": 5},
            {"side": "Norman", "change": 10, "side_2": "English", "change_2": -10},
            {"side": "Norman", "change": 10, "side_2": "English", "change_2": -10},
            {"side": "Norman", "change": -5, "side_2": "English", "change_2": -5},
            {"side": "English", "change": 5, "side_2": "Norman", "change_2": -5},
            {"side": "English", "change": 5},
            {"side": "Norman", "change": 10},
            {"side": "Norman", "change": 5, "side_2": "English", "change_2": -15},
            {"side": "English", "change": 10, "side_2": "Norman", "change_2": -10},
            {"side": "Norman", "change": 5},
            {"side": "Norman", "change": -10},
            {"side": "Norman", "change": 10},
            {"side": "Norman", "change": 10, "side_2": "English", "change_2": -15},
            {"side": "English", "change": 5},
            {"side": "Norman", "change": 10},
            {"side": "Norman", "change": -10, "side_2": "English", "change_2": -10},
            {"side": "Norman", "change": 10},
            {"side": "English", "change": -20},
            {"side": "Norman", "change": 15, "side_2": "English", "change_2": -15},
            {"side": "English", "change": 10},
            {"side": "Norman", "change": 10},
            {"side": "English", "change": 5},
            {"side": "Norman", "change": 20, "side_2": "English", "change_2": -100},
            {"side": "English", "change": -20},
            {"side": "Norman", "change": 10, "side_2": "English", "change_2": -10},
            {"side": "Norman", "change": 10, "side_2": "English", "change_2": -30},
            {"side": "Norman", "change": 10, "side_2": "English", "change_2": -20},
            {"side": "English", "change": -20},
            {"side": "Norman", "change": 10},
            {"side": "Norman", "change": 5},
            {"side": "Norman", "change": 10},
            {"side": "Norman", "change": 5},
            {"side": "Norman", "change": 15},
            {"side": "Norman", "change": 10}
        ]
        self.english_morale = 100
        self.norman_morale = 100
        self.simulation_speed = 1  # Default speed (real-time)

    def update_morale(self, change):
        self.update_morale_side(change["side"], change["change"])
        if "side_2" in change and "change_2" in change:
            self.update_morale_side(change["side_2"], change["change_2"])

    def update_morale_side(self, side, change):
        if side == "English":
            self.english_morale += change
            self.english_morale = max(self.english_morale, 0)
        elif side == "Norman":
            self.norman_morale += change
            self.norman_morale = max(self.norman_morale, 0)

    def simulate_battle(self):
        print(Fore.GREEN + "Welcome to the Battle of Hastings simulation!")
        print("Get ready to experience a pivotal moment in history.\n")

        for event in self.timeline:
            print(f"{Fore.CYAN}{event['time']}: {Fore.WHITE}{event['event']}")
            time.sleep(self.simulation_speed)
            self.update_morale(self.morale_changes[event['morale_change'] - 1])
            print(Fore.YELLOW + "Morale:")
            print(f"{Fore.RED}English Morale: {Fore.WHITE}{self.english_morale}")
            print(f"{Fore.BLUE}Norman Morale: {Fore.WHITE}{self.norman_morale}")
            print()

        print(Fore.GREEN + "Simulation ended.")

    def set_simulation_speed(self):
        print(Fore.MAGENTA + "\nSet Simulation Speed")
        print(Fore.CYAN + "1. Real-time (default)")
        print(Fore.CYAN + "2. Fast (1 second per event)")
        print(Fore.CYAN + "3. Faster (0.5 seconds per event)")
        print(Fore.CYAN + "4. Fastest (0.1 seconds per event)")
        choice = input(Fore.YELLOW + "Choose the simulation speed (1-4): ")

        if choice == '1':
            self.simulation_speed = 8
        elif choice == '2':
            self.simulation_speed = 1
        elif choice == '3':
            self.simulation_speed = 0.5
        elif choice == '4':
            self.simulation_speed = 0.1
        else:
            print(Fore.RED + "Invalid choice, setting to default (real-time).")
            self.simulation_speed = 8

    def run(self):
        while True:
            print(Fore.GREEN + "\nBattle of Hastings Simulation")
            print(Fore.CYAN + "1. Run Simulation")
            print(Fore.CYAN + "2. Set Simulation Speed")
            print(Fore.CYAN + "3. Quit")
            choice = input(Fore.YELLOW + "Choose an option (1-3): ")

            if choice == '1':
                self.simulate_battle()
            elif choice == '2':
                self.set_simulation_speed()
            elif choice == '3':
                break
            else:
                print(Fore.RED + "Invalid choice, please try again.")

if __name__ == "__main__":
    BattleSimulation().run()
