import matplotlib.pyplot as plt
import networkx as nx
import random
from collections import deque

def generate_maze(n_rows, n_cols, ix, iy):
    """
    Generate a maze using depth-first search.
    """
    maze = [[0] * n_cols for _ in range(n_rows)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    stack = deque([(ix, iy)])

    while stack:
        x, y = stack[-1]
        maze[y][x] = 1
        possible_directions = [direction for direction in directions
                               if 0 <= x + direction[0]*2 < n_rows
                               and 0 <= y + direction[1]*2 < n_cols
                               and maze[y + direction[1]*2][x + direction[0]*2] == 0]
                               
        if possible_directions:
            dx, dy = random.choice(possible_directions)
            maze[y + dy][x + dx] = 1
            maze[y + dy*2][x + dx*2] = 1
            stack.append((x + dx*2, y + dy*2))
        else:
            stack.pop()
            
    return maze

def construct_graph(maze):
    """
    Convert a maze into a graph representation.
    """
    G = nx.Graph()
    rows, cols = len(maze), len(maze[0])
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 1:
                if r < rows - 1 and maze[r + 1][c] == 1:
                    G.add_edge((r, c), (r + 1, c))
                if c < cols - 1 and maze[r][c + 1] == 1:
                    G.add_edge((r, c), (r, c + 1))
    return G

def plot_maze(maze, path=None, save=False):
    """
    Display the maze, optionally with a path.
    """
    plt.figure(figsize=(10,10))
    plt.imshow(maze, cmap=plt.cm.binary)
    if path is not None:
        x_coords, y_coords = zip(*path)
        plt.plot(y_coords, x_coords, "b-", linewidth=2)
    if save:
        plt.savefig("maze.png")
    plt.show()

def get_input(prompt, default):
    """
    Get user input, with a default value.
    """
    result = input(prompt)
    return default if result.strip() == '' else int(result)

def print_header():
    """
    Display the program header.
    """
    print("\n" + "="*30)
    print(" "*5 + "Maze Generator and Solver")
    print("="*30)

def print_options():
    """
    Display the available menu options.
    """
    print("1. Generate a new maze")
    print("2. Save maze to file")
    print("3. Exit")

def select_difficulty():
    """
    Get user-selected difficulty level and map it to a maze size.
    """
    size_dict = {
        "easy": 11, 
        "medium": 21, 
        "hard": 31, 
        "extreme": 41, 
        "insane": 51
    }
    while True:
        difficulty = input("Select difficulty (Easy, Medium, Hard, Extreme, Insane): ").lower()
        if difficulty in size_dict:
            return size_dict[difficulty]
        else:
            print("Invalid difficulty. Please enter again.")

def main():
    """
    Main program loop.
    """
    path = None
    start, end = None, None
    maze = None
    while True:
        print_header()
        print_options()
        
        user_input = input("\nPlease choose an option: ")
        
        if user_input == "1":
            size = select_difficulty()
            start_row = get_input(f"Enter the start row (0 to {size-2}) or press enter for default: ", 0)
            start_col = get_input(f"Enter the start column (0 to {size-2}) or press enter for default: ", 0)
            end_row = get_input(f"Enter the end row (1 to {size-1}) or press enter for default: ", size-1)
            end_col = get_input(f"Enter the end column (1 to {size-1}) or press enter for default: ", size-1)
            start, end = (start_row, start_col), (end_row, end_col)
            
            path = None
            attempts = 0
            
            while path is None and attempts < 10:
                print("Generating maze...")
                maze = generate_maze(size, size, start_row, start_col)
                maze[start_row][start_col] = 1
                maze[end_row][end_col] = 1
                G = construct_graph(maze)
                print("Calculating path...")
                try:
                    path = nx.dijkstra_path(G, start, end)
                    print("Path found!")
                except nx.NetworkXNoPath:
                    attempts += 1
                    print("No path found. Generating a new maze...")
            if path is None:
                print("No valid maze found after 10 attempts. Try again.")
            else:
                plot_maze(maze, path)
        elif user_input == "2":
            if path is not None:
                plot_maze(maze, path, save=True)
                print("\nMaze image has been saved as maze.png")
            else:
                print("\nYou need to generate a maze first.")
        elif user_input == "3":
            print("\nExiting...")
            break
        else:
            print("\nInvalid option. Please try again.")

if __name__ == "__main__":
    main()