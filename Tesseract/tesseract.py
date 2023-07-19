import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# Function for 4D rotation
def rotation_matrix(t):
    cos_t, sin_t = np.cos(t), np.sin(t)
    return np.array([
        [cos_t, 0, -sin_t, 0],
        [0, cos_t, 0, -sin_t],
        [sin_t, 0, cos_t, 0],
        [0, sin_t, 0, cos_t]
    ])

# Function for 4D to 3D projection
def proj(mat):
    z = 1/(3 - mat[3,:])
    return np.array([mat[0]*z, mat[1]*z, mat[2]*z])

# Tesseract points (4D coordinates)
tesseract_points = np.array([
    [-1, -1, -1, 1],
    [-1, -1, 1, 1],
    [-1, 1, 1, 1],
    [-1, 1, -1, 1],
    [1, -1, -1, 1],
    [1, -1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, -1, 1],
    [-1, -1, -1, -1],
    [-1, -1, 1, -1],
    [-1, 1, 1, -1],
    [-1, 1, -1, -1],
    [1, -1, -1, -1],
    [1, -1, 1, -1],
    [1, 1, 1, -1],
    [1, 1, -1, -1]
]).T

# Edges of the tesseract
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # front face
    (4, 5), (5, 6), (6, 7), (7, 4),  # back face
    (0, 4), (1, 5), (2, 6), (3, 7),  # connecting edges
    (8, 9), (9, 10), (10, 11), (11, 8),  # bottom face
    (12, 13), (13, 14), (14, 15), (15, 12),  # top face
    (8, 12), (9, 13), (10, 14), (11, 15)  # connecting edges
]

# Precompute stationary points
stationary_points = proj(tesseract_points)

# Create figure
fig = plt.figure(figsize=(8, 4))

# Add subplot for rotating tesseract
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.set_xlim([-2, 2])
ax1.set_ylim([-2, 2])
ax1.set_zlim([-2, 2])
ax1.set_title("Rotating Tesseract")

# Add subplot for stationary tesseract
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.set_xlim([-2, 2])
ax2.set_ylim([-2, 2])
ax2.set_zlim([-2, 2])
ax2.set_title("Stationary Tesseract")

# Lines for the rotating tesseract
lines1 = [ax1.plot([], [], [], color='blue')[0] for _ in edges]

# Lines for the stationary tesseract
lines2 = [ax2.plot([], [], [], color='red')[0] for _ in edges]

# Initialization function for the animation
def init():
    return lines1 + lines2

# Update function for the animation
def update(t):
    # Apply rotation and projection
    rotated_points = proj(rotation_matrix(t) @ tesseract_points)

    # Update line positions
    [line.set_data(rotated_points[0, edge], rotated_points[1, edge]) or line.set_3d_properties(rotated_points[2, edge]) for line, edge in zip(lines1, edges)]
    [line.set_data(stationary_points[0, edge], stationary_points[1, edge]) or line.set_3d_properties(stationary_points[2, edge]) for line, edge in zip(lines2, edges)]

    return lines1 + lines2

# Create animation
ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 200, endpoint=False), init_func=init, blit=True)

# Display the animation
plt.show()
