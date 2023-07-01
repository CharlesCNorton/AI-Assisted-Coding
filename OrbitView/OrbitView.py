import ephem
import matplotlib.pyplot as plt
from tkinter import *
import numpy as np
from datetime import datetime

"OrbitView: An Interactive Solar System Explorer"

class App:
    def __init__(self, master):
        # Initialize the tkinter master object
        self.master = master
        master.title("OrbitView: An Interactive Solar System Explorer")

        # List of planets to visualize
        self.planets = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

        # Set up dropdown menu for planet selection
        self.planetVar = StringVar(master)
        self.planetVar.set(self.planets[0])  # default value

        self.planetMenu = OptionMenu(master, self.planetVar, *self.planets)
        self.planetMenu.pack()

        # Set up date input field
        self.dateEntry = Entry(master)
        self.dateEntry.insert(0, "yyyy/mm/dd")
        self.dateEntry.pack()

        # Set up button to trigger position calculation and visualization
        self.getPosButton = Button(master, text="Get Position", command=self.update_position)
        self.getPosButton.pack()

        # Set up label to display position information
        self.positionLabel = Label(master, text="")
        self.positionLabel.pack()

        # Set up scale to control viewing range (zoom level)
        self.zoomScale = Scale(master, from_=1, to=32, orient=HORIZONTAL, length=400,
                               label="Viewing range (AU)", sliderlength=20)
        self.zoomScale.set(32)
        self.zoomScale.pack()

    def update_position(self):
        # Get selected planet name and entered date
        planet_name = self.planetVar.get()
        date = self.dateEntry.get()

        # Update planet position and visualize
        try:
            position = self.get_planet_position(planet_name, date)
            self.positionLabel.config(text=str(position))
            self.plot_orbits(planet_name, self.zoomScale.get(), date)
        except (AttributeError, ValueError):
            self.positionLabel.config(text="Error: Invalid input. Please check the planet name and date format (yyyy/mm/dd).")

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
