import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.ndimage import convolve
import matplotlib.colors as mcolors

# Define the size of the grid, ensure it's not too small or too large
N = min(max(3, 200), 1000)

# Initialize the random state for reproducibility
np.random.seed(0)

# Check that the probabilities sum to 1 to avoid unexpected behaviour
probabilities = [0.5, 0.5]
assert abs(sum(probabilities) - 1) < 1e-9, "Probabilities must sum to 1"

# Set up the initial state of the grid
try:
    grid = np.random.choice([0, 1], size=(N, N), p=probabilities).astype(np.uint8)
except ValueError as e:
    print("Invalid input for initial state of the grid. Error: ", str(e))
    raise

# Define the neighborhood kernel: 3x3 matrix with 1s surrounding a 0
kernel = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]])

# List to track the number of alive and dead cells at each generation
alive_cells = [np.sum(grid)]
dead_cells = [N*N - alive_cells[0]]

def compute_next_generation(grid):
    """Return the next generation of the grid in the Game of Life."""
    # Count the number of live neighbors for each cell
    try:
        num_neighbors = convolve(grid, kernel, mode='wrap')
    except Exception as e:
        print("Error during convolution. Error: ", str(e))
        raise

    # Apply the rules of the Game of Life using logical operations
    return ((grid == 1) & (num_neighbors >= 2) & (num_neighbors <= 3)) | ((grid == 0) & (num_neighbors == 3))

def setup_plot(grid):
    """Set up the plot for the Game of Life."""
    try:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 16))

        # Use a colormap to make the plot more colorful
        cmap = mcolors.LinearSegmentedColormap.from_list("MyCmap", ["black", "green"])
        image = ax1.imshow(grid, cmap=cmap, interpolation='nearest')
        ax1.set_xticks([])
        ax1.set_yticks([])

        # Add a colorbar
        cbar = plt.colorbar(image, ax=ax1, ticks=[0, 1])
        cbar.ax.set_yticklabels(['Dead', 'Alive'])

        # Initial plot for alive and dead cells over generations
        ax2.set_title('Alive and Dead Cells over Generations')
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Number of Cells')
        lines = ax2.plot(alive_cells, label='Alive')
        lines += ax2.plot(dead_cells, label='Dead')
        ax2.legend()

        return fig, ax1, ax2, image, lines

    except Exception as e:
        print("Error during plot setup. Error: ", str(e))
        raise

fig, ax1, ax2, image, lines = setup_plot(grid)

def update_image(frame, grid, image):
    """Update the image for a new frame."""
    grid[:] = compute_next_generation(grid)
    image.set_array(grid)
    alive_cells.append(np.sum(grid))
    dead_cells.append(N*N - alive_cells[-1])
    for i, line in enumerate(lines):
        line.set_ydata([alive_cells, dead_cells][i])
        line.set_xdata(range(len(alive_cells)))
    ax2.relim()
    ax2.autoscale_view()
    return [image] + lines

# Start the animation
try:
    ani = animation.FuncAnimation(fig, update_image, frames=1000, interval=50, blit=True, fargs=(grid, image))
except Exception as e:
    print("Error during animation setup. Error: ", str(e))
    raise

# Display the animation
try:
    plt.show()
except Exception as e:
    print("Error during animation display. Error: ", str(e))
    raise
