import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm

def proj(mat):
    """ Project from 4D to 3D. """
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0]
    ]) @ mat

def rotation_matrix(t):
    """ Generate a 4D rotation matrix. """
    return np.array([
        [np.cos(t), 0, 0, -np.sin(t)],
        [0, np.cos(t), -np.sin(t), 0],
        [0, np.sin(t), np.cos(t), 0],
        [np.sin(t), 0, 0, np.cos(t)]
    ])

def tesseract_points():
    """ Generate the vertices of a tesseract. """
    return np.array([
        [1, 1, 1, 1],
        [-1, 1, 1, 1],
        [1, -1, 1, 1],
        [-1, -1, 1, 1],
        [1, 1, -1, 1],
        [-1, 1, -1, 1],
        [1, -1, -1, 1],
        [-1, -1, -1, 1],
        [1, 1, 1, -1],
        [-1, 1, 1, -1],
        [1, -1, 1, -1],
        [-1, -1, 1, -1],
        [1, 1, -1, -1],
        [-1, 1, -1, -1],
        [1, -1, -1, -1],
        [-1, -1, -1, -1],
    ]).T

def draw_edges(points, ax):
    """ Draw the edges of the tesseract. """
    idx_pairs = [
        (0, 1), (1, 3), (3, 2), (2, 0),   # front square
        (4, 5), (5, 7), (7, 6), (6, 4),   # back square
        (0, 4), (1, 5), (2, 6), (3, 7),   # connecting lines
        (8, 9), (9, 11), (11, 10), (10, 8),   # front square (z=-1)
        (12, 13), (13, 15), (15, 14), (14, 12),  # back square (z=-1)
        (8, 12), (9, 13), (10, 14), (11, 15)   # connecting lines (z=-1)
    ]

    for i, j in idx_pairs:
        ax.plot([points[0, i], points[0, j]],
                [points[1, i], points[1, j]],
                [points[2, i], points[2, j]], color='r', alpha=0.2)

def update(t):
    """ Update function for animation. """
    ax.cla()
    points = proj(rotation_matrix(t) @ tesseract_points())

    # Normalize the points for color mapping and discard the fourth dimension
    norm = plt.Normalize(-1,1)
    colors = cm.viridis(norm(points.T[:, 0]))

    ax.scatter(points[0, :], points[1, :], points[2, :], color=colors)
    draw_edges(points, ax)

    # Label the vertices
    for i in range(points.shape[1]):
        ax.text(points[0, i], points[1, i], points[2, i], f'v{i}', color='blue')

    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])

if __name__ == "__main__":
    try:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 100), interval=100)
        plt.show()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
