import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 15)
    ax.set_title('Aula 1', fontsize=16)
    ax.grid(True, linestyle='--', alpha=0.6)

    triangulo = patches.Polygon([[2, 2], [8, 2], [5, 8]], closed=True, color='blue', alpha=0.7)
    ax.add_patch(triangulo)

    circulo = patches.Circle((10, 8), radius=1.5, color='orange', alpha=0.9)
    ax.add_patch(circulo)

    plt.show()

if __name__ == "__main__":
    main()