import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_cozy_fireplace():
    fig, ax = plt.subplots()

    fig.patch.set_facecolor("darkslategray")

    fireplace = patches.Rectangle((0.1, 0.1), 0.8, 0.8, fill=True, color="saddlebrown", edgecolor="black", linewidth=2, joinstyle="round")
    ax.add_patch(fireplace)

    firebox = patches.Rectangle((0.2, 0.15), 0.6, 0.6, fill=True, color="gray", joinstyle="round")
    ax.add_patch(firebox)

    for i in np.linspace(0.3, 0.7, 10):
        log = patches.Ellipse((i, 0.2), 0.12, 0.05, fill=True, color=np.random.choice(["sienna", "saddlebrown", "peru"]))
        ax.add_patch(log)

    for i in np.linspace(0.3, 0.7, 20):
        flame_height = np.random.uniform(0.1, 0.4)
        flame = patches.Polygon(((i, 0.25), (i+0.05, 0.25+flame_height), (i+0.1, 0.25)), closed=True, fill=True, color=np.random.choice(["orange", "yellow", "red"]))
        ax.add_patch(flame)

    mantlepiece = patches.Rectangle((0.1, 0.75), 0.8, 0.05, fill=True, color="burlywood", edgecolor="black", linewidth=2, joinstyle="round")
    ax.add_patch(mantlepiece)

    decoration1 = patches.Rectangle((0.2, 0.8), 0.1, 0.15, fill=True, color="gold", edgecolor="black", linewidth=1)
    ax.add_patch(decoration1)
    decoration2 = patches.Ellipse((0.8, 0.875), 0.1, 0.15, fill=True, color="silver", edgecolor="black", linewidth=1)
    ax.add_patch(decoration2)

    rug = patches.Rectangle((0.1, 0), 0.8, 0.1, fill=True, color="navajowhite", edgecolor="black", linewidth=1)
    ax.add_patch(rug)

    cat = patches.Ellipse((0.5, 0.05), 0.1, 0.05, fill=True, color="gray", edgecolor="black", linewidth=1)
    ax.add_patch(cat)

    window = patches.Rectangle((0.05, 0.4), 0.05, 0.2, fill=True, color="skyblue", edgecolor="black", linewidth=2)
    ax.add_patch(window)

    plt.xlim(0, 1)
    plt.ylim(0, 1)
    ax.axis("off")
    plt.show()

def main():
    while True:
        print("\nCozy Fireplace Scene")
        print("1. Draw Scene")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            draw_cozy_fireplace()
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
