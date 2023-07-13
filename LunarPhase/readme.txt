
# LunarPhase

LunarPhase is a Python script that calculates and displays information about the moon phase for a given date. It uses the Ephemeris and Skyfield libraries to calculate the phase and distance of the moon, and the Rich library to display the results in a nice console output.

## How to Run

You can run LunarPhase by executing the `ImprovedLunarPhase_v3.py` script in a Python environment that has the necessary libraries installed.

## Dependencies

LunarPhase requires the following Python libraries:

- `ephem`
- `skyfield`
- `rich`
- `prompt_toolkit`

You can install these dependencies using pip:

```
pip install ephem skyfield rich prompt_toolkit
```

## Usage

When you run LunarPhase, you'll see a menu with three options:

1. Get Moon Phase for specific date: Enter a date in the format `yyyy/mm/dd`, and LunarPhase will display information about the moon phase for that date.
2. Get Moon Phase for today: LunarPhase will display information about the moon phase for today's date.
3. Exit: Exit the application.

## Note

The calculation of the moon's illumination is an approximation based on a sinusoidal model of the moon's phase. It may not exactly match the precise illumination percentage provided by detailed astronomical computations or observational data.
