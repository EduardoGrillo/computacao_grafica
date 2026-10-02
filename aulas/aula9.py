# dia 04/09/26 - Transformação Escala
import numpy as np
import matplotlib.pyplot as plt

def transformacao_escala():
    print("=== Escala 2D ===\n")

    matriz_vertices = np.array([
        [1, 3, 5, 1],  # linha do eixo x
        [3, 7, 3, 3],  # linha do eixo y
        [1, 1, 1, 1]   # linha do eixo w
    ])

    print("Matriz de Vértices Original (SRO):")
    print(matriz_vertices, "\n")

    sx = 2
    sy = 2

    matriz_escala = np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])

    print(f"Matriz de Escala (sx={sx}, sy={sy}):")
    print(matriz_escala, "\n")

    matriz_transformada = matriz_escala @ matriz_vertices

    print("Matriz de Vértices Escalados (SRU):")
    print(matriz_transformada, "\n")

    fig, ax = plt.subplots(figsize=(10, 10))

    x_orig = matriz_vertices[0, :]
    y_orig = matriz_vertices[1, :]

    x_trans = matriz_transformada[0, :]
    y_trans = matriz_transformada[1, :]

    ax.plot(x_orig, y_orig, color='blue', linestyle='--', linewidth=2, marker='o', label='Original')
    ax.fill(x_orig, y_orig, color='blue', alpha=0.1)

    ax.plot(x_trans, y_trans, color='red', linestyle='-', linewidth=2, marker='s', label='Escalado (2,2)')
    ax.fill(x_trans, y_trans, color='red', alpha=0.3)

    rotulos = ['A', 'B', 'C']
    for i in range(3):
        ax.annotate(f'{rotulos[i]} {x_orig[i]:.0f}, {y_orig[i]:.0f}', (x_orig[i], y_orig[i]), textcoords="offset points", xytext=(0,10), ha='center', color='blue')
        ax.annotate(f'{rotulos[i]} {x_trans[i]:.0f}, {y_trans[i]:.0f}', (x_trans[i], y_trans[i]), textcoords="offset points", xytext=(0,10), ha='center', color='red')

    for i in range(3):
        ax.plot([0, x_trans[i]], [0, y_trans[i]], color='gray', linestyle=':', alpha=0.5)

    ax.set_title("Transformação Escala", fontsize=14, fontweight='bold')
    ax.set_xlabel("Eixo X", fontsize=12)
    ax.set_ylabel("Eixo Y", fontsize=12)

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)

    ax.axhline(0, color='black', linewidth=2)
    ax.axhline(0, color='black', linewidth=2)

    ax.set_xticks(np.arange(0, 13, 1))
    ax.set_yticks(np.arange(0, 17, 1))
    ax.grid(True, linestyle=':', color='gray', alpha=0.7)
    ax.legend(loc='upper left', fontsize=12)

    print("Renderizando o plano cartesiano...")
    plt.show()

if __name__ == "__main__":
    transformacao_escala()