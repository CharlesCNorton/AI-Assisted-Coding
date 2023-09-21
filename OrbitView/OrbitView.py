import ephem
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import numpy as np
from datetime import datetime
from tkcalendar import DateEntry

class App:
    def __init__(self, master):
        # Initialize the tkinter master object
        self.master = master
        master.title("OrbitView: An Interactive Solar System Explorer")

        # List of planets to visualize
        self.planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

        # Set up labels, dropdown menu for planet selection, date picker, and button in grid layout
        Label(master, text="Select Planet:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        Label(master, text="Select Date:").grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.planetVar = StringVar(master)
        self.planetVar.set(self.planets[0])  # default value

        self.planetMenu = ttk.Combobox(master, textvariable=self.planetVar, values=self.planets)
        self.planetMenu.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.dateEntry = DateEntry(master, date_pattern='yyyy/mm/dd')
        self.dateEntry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.getPosButton = Button(master, text="Get Position", command=self.update_position)
        self.getPosButton.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Set up label to display position information
        self.positionLabel = Label(master, text="")
        self.positionLabel.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Set up scale to control viewing range (zoom level)
        Label(master, text="Viewing range (AU):").grid(row=4, column=0, padx=5, pady=5, sticky='w')

        self.zoomScale = Scale(master, from_=1, to=32, orient=HORIZONTAL, length=400, sliderlength=20)
        self.zoomScale.set(32)
        self.zoomScale.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        # Add a Clear button to reset inputs
        self.clearButton = Button(master, text="Clear", command=self.clear_inputs)
        self.clearButton.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def clear_inputs(self):
        # Reset the input fields to their default values
        self.planetVar.set(self.planets[0])
        self.dateEntry.set_date(datetime.now())
        self.zoomScale.set(32)
        self.positionLabel.config(text="")




    def update_position(self):
        # Get selected planet name and entered date
        planet_name = self.planetVar.get()
        date = self.dateEntry.get()

        # Check if the date variable is a string. If it is, convert it to a datetime object.
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y/%m/%d')

        # Update planet position and visualize
        try:
            position = self.get_planet_position(planet_name, date.strftime('%Y/%m/%d'))
            self.positionLabel.config(text=f"Planet: {planet_name}\nDate: {date.strftime('%Y/%m/%d')}\nPosition: {position}")
            self.plot_orbits(planet_name, self.zoomScale.get(), date.strftime('%Y/%m/%d'))
        except (AttributeError, ValueError) as e:
            messagebox.showerror("Error", "Invalid input. Please check the planet name and date format (yyyy/mm/dd).")

    @staticmethod
    def get_planet_position(planet_name, date):
        # Create a planet object and set the date
        planet = getattr(ephem, planet_name)()
        planet.compute(date)
        return planet.earth_distance, planet.hlong

    def plot_orbits(self, planet_name, zoom, date):
        # Set up figure for orbital plot
        plt.figure(figsize=[7, 7])
        ax = plt.subplot(111, polar=True)

        # Plot orbits for each planet
        for planet in self.planets:
            planet_obj = getattr(ephem, planet)()
            planet_obj.compute(date)
            ax.plot([0, planet_obj.hlong], [0, planet_obj.earth_distance], label=planet)
            ax.scatter(planet_obj.hlong, planet_obj.earth_distance, s=200, alpha=0.75)

        # Plot the Sun
        ax.scatter(0, 0, color='yellow', s=300, label='Sun')

        # Configure plot appearance
        ax.set_theta_zero_location("S")  # Set 0 degrees to the top of the plot
        ax.set_ylim(0, zoom)  # Set the maximum radial limit to match the zoom level
        ax.set_rticks(np.linspace(0, zoom, num=6))  # Adjust radial ticks to match viewing range
        ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
        ax.grid(True)
        ax.legend()
        plt.show()

root = Tk()
app = App(root)
root.mainloop()
