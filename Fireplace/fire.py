import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_cozy_fireplace_realistic():
    fig, ax = plt.subplots()

    fig.patch.set_facecolor("darkslategray")

    # Fireplace
    fireplace = patches.Rectangle((0.1, 0.1), 0.8, 0.8, fill=True, color="saddlebrown", edgecolor="black", linewidth=2)
    ax.add_patch(fireplace)

    firebox = patches.Rectangle((0.2, 0.15), 0.6, 0.6, fill=True, color="gray")
    ax.add_patch(firebox)

    # Logs and flames with more realistic distribution
    for i in np.random.normal(loc=0.5, scale=0.1, size=10):
        if 0.2 < i < 0.8:  # Keep logs within firebox
            log = patches.Ellipse((i, 0.2), 0.12, 0.05, fill=True, color=np.random.choice(["sienna", "saddlebrown", "peru"]))
            ax.add_patch(log)

    for i in np.random.normal(loc=0.5, scale=0.1, size=20):
        if 0.2 < i < 0.8:  # Keep flames within firebox
            flame_height = np.random.uniform(0.1, 0.4)
            flame = patches.Polygon(((i, 0.25), (i+0.05, 0.25+flame_height), (i+0.1, 0.25)), closed=True, fill=True, color=np.random.choice(["orange", "yellow", "red"]))
            ax.add_patch(flame)

    # Mantlepiece
    mantlepiece = patches.Rectangle((0.1, 0.75), 0.8, 0.05, fill=True, color="burlywood", edgecolor="black", linewidth=2)
    ax.add_patch(mantlepiece)

    decoration1 = patches.Rectangle((0.2, 0.8), 0.1, 0.15, fill=True, color="gold", edgecolor="black", linewidth=1)
    ax.add_patch(decoration1)
    decoration2 = patches.Ellipse((0.8, 0.875), 0.1, 0.15, fill=True, color="silver", edgecolor="black", linewidth=1)
    ax.add_patch(decoration2)

    # Rug
    rug = patches.Rectangle((0.1, 0), 0.8, 0.1, fill=True, color="navajowhite", edgecolor="black", linewidth=1)
    ax.add_patch(rug)

    # Cat
    cat = patches.Ellipse((0.5, 0.05), 0.1, 0.05, fill=True, color="gray", edgecolor="black", linewidth=1)
    ax.add_patch(cat)

    # Window
    window = patches.Rectangle((0.05, 0.4), 0.05, 0.2, fill=True, color="skyblue", edgecolor="black", linewidth=2)
    ax.add_patch(window)

    # Armchair
    armchair = patches.Polygon([(0.75, 0.15), (0.9, 0.15), (0.9, 0.35), (0.83, 0.35), (0.83, 0.25), (0.75, 0.25)], fill=True, color="saddlebrown", edgecolor="black", linewidth=2)
    ax.add_patch(armchair)

    # Picture
    picture = patches.Rectangle((0.1, 0.9), 0.2, 0.1, fill=True, color="burlywood", edgecolor="black", linewidth=2)
    ax.add_patch(picture)

    # Bookshelf
    bookshelf = patches.Rectangle((0.05, 0.1), 0.05, 0.7, fill=True, color="saddlebrown", edgecolor="black", linewidth=2)
    ax.add_patch(bookshelf)
    for i in np.linspace(0.1, 0.8, 20):  # Add books
        book = patches.Rectangle((0.05, i), 0.05, 0.03, fill=True, color=np.random.choice(["tan", "wheat", "khaki"]))
        ax.add_patch(book)

    # Ceiling lamp
    lamp = patches.Polygon([(0.5, 0.95), (0.55, 0.9), (0.5, 0.85), (0.45, 0.9)], fill=True, color="yellow", edgecolor="black", linewidth=1)
    ax.add_patch(lamp)
    glow = patches.Circle((0.5, 0.9), 0.15, color="yellow", alpha=0.2)
    ax.add_patch(glow)

    # Plant
    plant_pot = patches.Ellipse((0.075, 0.875), 0.05, 0.03, fill=True, color="sienna", edgecolor="black", linewidth=1)
    ax.add_patch(plant_pot)
    for i in np.linspace(-0.02, 0.02, 10):
        leaf = patches.Polygon(((0.075+i, 0.9), (0.075+i+0.01, 0.97), (0.075+i+0.02, 0.9)), closed=True, fill=True, color="green")
        ax.add_patch(leaf)

    plt.xlim(0, 1)
    plt.ylim(0, 1)
    ax.axis("off")
    plt.show()
