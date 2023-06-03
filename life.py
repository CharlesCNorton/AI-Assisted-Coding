import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set the size of the grid
N = 200

# Set up the initial state of the grid
grid = np.random.choice([0, 1], size=(N, N), p=[0.5, 0.5])

# Define the rules for the Game of Life
def get_next_generation(grid):
    next_generation = np.zeros_like(grid)
    for i in range(N):
        for j in range(N):
            num_neighbors = count_neighbors(grid, i, j)
            next_generation[i, j] = apply_rules(grid, i, j, num_neighbors)
    return next_generation

def count_neighbors(grid, i, j):
    """Count the number of live neighbors around a cell."""
    neighbors = (
        grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, j] + grid[(i-1)%N, (j+1)%N] +
        grid[i, (j-1)%N] + grid[i, (j+1)%N] +
        grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, j] + grid[(i+1)%N, (j+1)%N]
    )
    return neighbors

def apply_rules(grid, i, j, num_neighbors):
    """Apply the rules of the Game of Life."""
    if grid[i, j] == 1 and (num_neighbors < 2 or num_neighbors > 3):
        return 0
    elif grid[i, j] == 0 and num_neighbors == 3:
        return 1
    else:
        return grid[i, j]

# Set up the plot
fig, ax = plt.subplots()
im = ax.imshow(grid, cmap='binary')

# Define the animation function
def animate(frame):
    global grid
    grid = get_next_generation(grid)
    im.set_data(grid)
    return [im]

# Start the animation
ani = animation.FuncAnimation(fig, animate, frames=1000, interval=50, blit=True)

# Set the axis limits of the plot
ax.set_xlim([0, N])
ax.set_ylim([0, N])

# Hide the axis ticks and labels
ax.set_xticks([])
ax.set_yticks([])
ax.set_xticklabels([])
ax.set_yticklabels([])

# Make sure the animation window stays open until closed by the user
plt.show()
