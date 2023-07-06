# Game of Life Simulator

This repository contains a Python script for simulating Conway's Game of Life, a cellular automaton devised by John Conway.

## Features

- Uses a 2D grid of cells, initially randomized.
- The grid size can be adjusted by changing the value of `N` (default size is 200x200).
- Uses matplotlib for visualization, featuring an animation of the simulation and a color map distinguishing between dead (black) and alive (green) cells.
- Robust error handling for functions such as grid initialization, animation setup, and display.

## Requirements

- numpy
- matplotlib
- scipy

## Usage

Simply run `python game_of_life.py` to start the simulation. The animation will display a sequence of frames showing the evolution of the cells over time, according to the rules of the Game of Life.