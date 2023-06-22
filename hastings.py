import time
TIMELINE = [
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
english_morale = 100
norman_morale = 100
def update_morale(side, change):
    global english_morale, norman_morale
    if side == "English":
        english_morale += change
        english_morale = max(english_morale, 0)
    elif side == "Norman":
        norman_morale += change
        norman_morale = max(norman_morale, 0)
def simulate_battle():
    global english_morale, norman_morale
    print("Welcome to the Battle of Hastings simulation!")
    print("Get ready to experience a pivotal moment in history.\n")
    for event in TIMELINE:
        print(f"{event['time']}: {event['event']}")
        time.sleep(2)
        choice = input("Press Enter to continue or 'q' to quit: ")
        if choice.lower() == 'q':
            print("Simulation ended.")
            break
        if "English" in event['event']:
            update_morale("English", 10)
        elif "Norman" in event['event']:
            update_morale("Norman", 10)
        if "Norman army forms at the base of Senlac Hill" in event['event']:
            update_morale("Norman", 5)
        if "Norman scouts report the position of the English army" in event['event']:
            update_morale("English", -10)
        if "English shield wall takes shape atop Senlac Hill" in event['event']:
            update_morale("English", 10)
        if "Harold gives a rousing speech, morale in English army soars" in event['event']:
            update_morale("English", 20)
        if "Norman archers let fly a deadly rain of arrows" in event['event']:
            update_morale("English", -20)
            update_morale("Norman", 5)
        if "English archers return fire, both sides suffer casualties" in event['event']:
            update_morale("English", 5)
            update_morale("Norman", 5)
        if "English housecarls surge down the hill, crashing into the Norman lines" in event['event']:
            update_morale("English", 10)
            update_morale("Norman", -10)
        if "Rumors of William's death cause momentary confusion in Norman ranks" in event['event']:
            update_morale("Norman", -5)
        if "William rides along his line, dispelling rumors of his demise" in event['event']:
            update_morale("Norman", 10)
        if "Norman cavalry, on William's command, launches a devastating counter-charge" in event['event']:
            update_morale("Norman", 15)
            update_morale("English", -25)
        if "Harold Godwinson falls, his eye pierced by a Norman arrow" in event['event']:
            update_morale("English", -100)
            update_morale("Norman", 20)
        if "News of Harold's death spreads, causing chaos in the English ranks" in event['event']:
            update_morale("English", -20)
        if "English housecarls, heartbroken and leaderless, begin their weary retreat" in event['event']:
            update_morale("English", -30)
            update_morale("Norman", 10)
        if "Normans continue their onslaught, leaving no quarter for the fleeing English" in event['event']:
            update_morale("English", -20)
            update_morale("Norman", 10)
        if "Victorious Normans establish their reign over the hill and surrounding lands" in event['event']:
            update_morale("Norman", 10)
        if "Norman soldiers gather their dead, the hill is silent but for the wind" in event['event']:
            update_morale("Norman", 5)
        if "Norman soldiers, unabashed, loot the fallen and nearby hamlets" in event['event']:
            update_morale("Norman", 10)
        if "William begins planning for the consolidation of his rule" in event['event']:
            update_morale("Norman", 5)
        if "In the wake of a bloody day, William the Conqueror is declared King of England" in event['event']:
            update_morale("Norman", 15)
        if "News of the Norman victory begins to spread, marking the beginning of a new era" in event['event']:
            update_morale("Norman", 10)
        print("Morale:")
        print(f"English Morale: {english_morale}")
        print(f"Norman Morale: {norman_morale}")
        print()
simulate_battle()
