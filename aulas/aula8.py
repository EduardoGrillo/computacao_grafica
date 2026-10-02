# Dia 02/09/2026

import numpy as np
import matplotlib.pyplot as plt


def transformacao_translacao():
    print("=== Transformação de Translação ===\n")

    matriz_vertices = np.array([
        [1, 3, 5, 1],  # linha do eixo x
        [3, 7, 3, 3],  # linha do eixo y
        [1, 1, 1, 1]   # linha do eixo w (coordenada homogênea)
    ])

    print("Matriz de Vértices Original (SRO):")
    print(matriz_vertices, "\n")

    tx = 2
    ty = 2

    matriz_translacao = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])

    print(f"Matriz de Translação (tx={tx}, ty={ty}):")
    print(matriz_translacao, "\n")

    # Multiplicação matricial
    matriz_transformada = matriz_translacao @ matriz_vertices

    print("Matriz de Vértices Transladada (SRU):")
    print(matriz_transformada, "\n")

    fig, ax = plt.subplots(figsize=(10, 8))

    # Coordenadas originais
    x_orig = matriz_vertices[0, :]
    y_orig = matriz_vertices[1, :]

    # Coordenadas após a translação
    x_trans = matriz_transformada[0, :]
    y_trans = matriz_transformada[1, :]

    # Figura original
    ax.plot(
        x_orig,
        y_orig,
        color='blue',
        linestyle='--',
        linewidth=2,
        marker='o',
        label='Original'
    )

    ax.fill(
        x_orig,
        y_orig,
        color='blue',
        alpha=0.1
    )

    # Figura transladada
    ax.plot(
        x_trans,
        y_trans,
        color='red',
        linestyle='-',
        linewidth=2,
        marker='o',
        label='Transladado'
    )

    ax.fill(
        x_trans,
        y_trans,
        color='red',
        alpha=0.1
    )

    # Rótulos dos vértices
    rotulos = ['A', 'B', 'C']

    for i in range(3):

        ax.annotate(
            f'{rotulos[i]} ({x_orig[i]:.1f}, {y_orig[i]:.1f})',
            (x_orig[i], y_orig[i]),
            textcoords="offset points",
            xytext=(-15, -15),
            color='blue'
        )

        ax.annotate(
            f'{rotulos[i]}\' ({x_trans[i]:.1f}, {y_trans[i]:.1f})',
            (x_trans[i], y_trans[i]),
            textcoords="offset points",
            xytext=(-15, -15),
            color='darkred'
        )

    ax.set_title(
        "Exemplo de Translação",
        fontsize=14,
        fontweight='bold'
    )

    ax.set_xlabel("Eixo X", fontsize=12)
    ax.set_ylabel("Eixo Y", fontsize=12)

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 12)

    # Eixos cartesianos
    ax.axhline(0, color='black', linewidth=2)
    ax.axvline(0, color='black', linewidth=2)

    # Escala
    ax.set_xticks(np.arange(0, 16, 1))
    ax.set_yticks(np.arange(0, 13, 1))

    ax.grid(
        True,
        linestyle=':',
        color='gray',
        alpha=0.7
    )

    ax.legend(loc='upper left', fontsize=12)

    print("[*] Renderizando o plano cartesiano...")

    plt.show()


if __name__ == "__main__":
    transformacao_translacao()