#Dia 16/09
import numpy as np
import matplotlib.pyplot as plt

def desenhar_cenario(ax, matriz_trans, titulo, cor_trans, label_trans, matriz_vertices):
    ax.set_title(titulo, fontweight='bold', fontsize=12)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_xticks(np.arange(-10, 11, 2))
    ax.set_yticks(np.arange(-10, 11, 2))
    ax.set_aspect('equal')

    x_orig, y_orig = matriz_vertices[0, :], matriz_vertices[1, :]
    ax.plot(x_orig, y_orig, 'o-', color='blue', linestyle='--', marker='o', label='Original')
    ax.fill(x_orig, y_orig, color='blue', alpha=0.1)

    x_trans, y_trans = matriz_trans[0, :], matriz_trans[1, :]
    ax.plot(x_trans, y_trans, color=cor_trans, linestyle='--', marker='o', label=label_trans)
    ax.fill(x_trans, y_trans, color=cor_trans, alpha=0.3)

    ax.annotate(f"A(2, 2)", (x_orig[0], y_orig[0]), textcoords="offset points", xytext=(5, 5), color='blue')
    ax.annotate(f"A'({x_trans[0]:.1f}, {y_trans[0]:.1f})", (x_trans[0], y_trans[0]), textcoords="offset points", xytext=(5, 5), color=cor_trans)

    ax.legend(loc='upper left', fontsize=9)

def plotar_reflexao():
    print("=== Reflexão ===\n")

    matriz_vertices = np.array([
        [2, 4, 6, 2],
        [2, 5, 2, 2],
        [1, 1, 1, 1] 
    ], dtype=np.float32)

    M_RefX = np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])

    M_RefY = np.array([
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

    M_RefXY = np.array([
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])

    theta = np.radians(60)
    c, s = np.cos(theta), np.sin(theta)
    M_Ref6O = np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])

    trans_X = M_RefX @ matriz_vertices
    trans_Y = M_RefY @ matriz_vertices
    trans_XY = M_RefXY @ matriz_vertices
    trans_Rot = M_Ref6O @ matriz_vertices

    fig, axs = plt.subplots(2, 2, figsize=(14, 14))

    desenhar_cenario(axs[0, 0], trans_X, "1. Reflexão em relação ao eixo X (Y invertido)", 'red', "Refletido X", matriz_vertices)
    desenhar_cenario(axs[0, 1], trans_Y, "2. Reflexão em relação ao eixo Y (X invertido)", 'green', "Refletido Y", matriz_vertices)
    desenhar_cenario(axs[1, 0], trans_XY, "3. Reflexão nos eixos XY (Origem)", 'purple', "Refletido XY", matriz_vertices)
    desenhar_cenario(axs[1, 1], trans_Rot, "4. Rotação de 60° na origem)", 'orange', "Refletido 60°", matriz_vertices)

    plt.tight_layout()
    print("Renderizando Reflexões...")
    plt.show()

if __name__ == "__main__":
    plotar_reflexao()
