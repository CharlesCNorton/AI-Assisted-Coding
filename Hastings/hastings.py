import time

class BattleSimulation:
    def __init__(self):
        self.timeline = [
            {"time": "9:00", "event": "Norman army forms at the base of Senlac Hill"},
            {"time": "9:15", "event": "Norman scouts report the position of the English army"},
            {"time": "9:30", "event": "English shield wall takes shape atop Senlac Hill"},
            {"time": "9:45", "event": "Harold gives a rousing speech, morale in English army soars"},
            {"time": "10:00", "event": "Norman archers let fly a deadly rain of arrows"},
            {"time": "10:15", "event": "English archers return fire, both sides suffer casualties"},
            {"time": "10:30", "event": "English housecarls surge down the hill, crashing into the Norman lines"},
            {"time": "10:45", "event": "Rumors of William's death cause momentary confusion in Norman ranks"},
            {"time": "11:00", "event": "William rides along his line, dispelling rumors of his demise"},
            {"time": "11:15", "event": "Norman cavalry, on William's command, launches a devastating counter-charge"},
            {"time": "11:30", "event": "Harold Godwinson falls, his eye pierced by a Norman arrow"},
            {"time": "11:45", "event": "News of Harold's death spreads, causing chaos in the English ranks"},
            {"time": "12:00", "event": "English housecarls, heartbroken and leaderless, begin their weary retreat"},
            {"time": "12:15", "event": "Normans continue their onslaught, leaving no quarter for the fleeing English"},
            {"time": "12:30", "event": "Victorious Normans establish their reign over the hill and surrounding lands"},
            {"time": "12:45", "event": "Norman soldiers gather their dead, the hill is silent but for the wind"},
            {"time": "13:00", "event": "Norman soldiers, unabashed, loot the fallen and nearby hamlets"},
            {"time": "13:15", "event": "William begins planning for the consolidation of his rule"},
            {"time": "13:30", "event": "In the wake of a bloody day, William the Conqueror is declared King of England"},
            {"time": "13:45", "event": "News of the Norman victory begins to spread, marking the beginning of a new era"}
        ]
        self.morale_changes = {
            "Norman army forms at the base of Senlac Hill": ("Norman", 5),
            "Norman scouts report the position of the English army": ("English", -10),
            "English shield wall takes shape atop Senlac Hill": ("English", 10),
            "Harold gives a rousing speech, morale in English army soars": ("English", 20),
            "Norman archers let fly a deadly rain of arrows": [("English", -20), ("Norman", 5)],
            "English archers return fire, both sides suffer casualties": [("English", 5), ("Norman", 5)],
            "English housecarls surge down the hill, crashing into the Norman lines": [("English", 10), ("Norman", -10)],
            "Rumors of William's death cause momentary confusion in Norman ranks": ("Norman", -5),
            "William rides along his line, dispelling rumors of his demise": ("Norman", 10),
            "Norman cavalry, on William's command, launches a devastating counter-charge": [("Norman", 15), ("English", -25)],
            "Harold Godwinson falls, his eye pierced by a Norman arrow": [("English", -100), ("Norman", 20)],
            "News of Harold's death spreads, causing chaos in the English ranks": ("English", -20),
            "English housecarls, heartbroken and leaderless, begin their weary retreat": [("English", -30), ("Norman", 10)],
            "Normans continue their onslaught, leaving no quarter for the fleeing English": [("English", -20), ("Norman", 10)],
            "Victorious Normans establish their reign over the hill and surrounding lands": ("Norman", 10),
            "Norman soldiers gather their dead, the hill is silent but for the wind": ("Norman", 5),
            "Norman soldiers, unabashed, loot the fallen and nearby hamlets": ("Norman", 10),
            "William begins planning for the consolidation of his rule": ("Norman", 5),
            "In the wake of a bloody day, William the Conqueror is declared King of England": ("Norman", 15),
            "News of the Norman victory begins to spread, marking the beginning of a new era": ("Norman", 10)
        }
        self.english_morale = 100
        self.norman_morale = 100

    def update_morale(self, side, change):
        if side == "English":
            self.english_morale += change
            self.english_morale = max(self.english_morale, 0)
        elif side == "Norman":
            self.norman_morale += change
            self.norman_morale = max(self.norman_morale, 0)

    def simulate_battle(self):
        print("Welcome to the Battle of Hastings simulation!")
        print("Get ready to experience a pivotal moment in history.\n")

        for event in self.timeline:
            print(f"{event['time']}: {event['event']}")
            time.sleep(8)
            if event['event'] in self.morale_changes:
                changes = self.morale_changes[event['event']]
                if isinstance(changes[0], tuple):
                    for change in changes:
                        self.update_morale(*change)
                else:
                    self.update_morale(*changes)
            print("Morale:")
            print(f"English Morale: {self.english_morale}")
            print(f"Norman Morale: {self.norman_morale}")
            print()

        print("Simulation ended.")

    def run(self):
        while True:
            choice = input("Press Enter to run the simulation or 'q' to quit: ")
            if choice.lower() == 'q':
                break
            self.simulate_battle()

if __name__ == "__main__":
    BattleSimulation().run()
