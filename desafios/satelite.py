import numpy as np
import matplotlib.pyplot as plt


def matriz_translacao(tx, ty):
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=np.float32)


def matriz_rotacao(angulo_graus):
    theta = np.radians(angulo_graus)

    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    return np.array([
        [cos_t, -sin_t, 0],
        [sin_t,  cos_t, 0],
        [0,      0,     1]
    ], dtype=np.float32)


def matriz_escala(sx, sy):
    return np.array([
        [sx, 0,  0],
        [0,  sy, 0],
        [0,  0,  1]
    ], dtype=np.float32)


def aplicar_transformacao(vertices, translacao, rotacao, escala):
    M_T = matriz_translacao(
        translacao[0],
        translacao[1]
    )

    M_R = matriz_rotacao(
        rotacao
    )

    M_S = matriz_escala(
        escala[0],
        escala[1]
    )

    # Ordem da direita para a esquerda:
    # Escala -> Rotação -> Translação
    M_composta = M_T @ M_R @ M_S

    return M_composta @ vertices


def desenhar_objeto(
    ax,
    vertices,
    cor,
    label,
    alpha=0.35,
    linestyle="-"
):
    x = vertices[0, :]
    y = vertices[1, :]

    ax.plot(
        x,
        y,
        color=cor,
        linewidth=2,
        linestyle=linestyle,
        label=label
    )

    ax.fill(
        x,
        y,
        color=cor,
        alpha=alpha
    )


def main():
    print("=== Desafio do Engenheiro de Satélites Espaciais ===\n")

    # =========================================================
    # PRIMITIVAS NO SRO
    # =========================================================

    # Corpo e painéis:
    # p1(-1,-1), p2(1,-1), p3(1,1), p4(-1,1)

    quadrado = np.array([
        [-1,  1,  1, -1, -1],
        [-1, -1,  1,  1, -1],
        [ 1,  1,  1,  1,  1]
    ], dtype=np.float32)

    # Antena:
    # p1(-1,0), p2(1,0), p3(0,2)

    antena = np.array([
        [-1, 1, 0, -1],
        [ 0, 0, 2,  0],
        [ 1, 1, 1,  1]
    ], dtype=np.float32)

    # =========================================================
    # TRANSFORMAÇÕES DO CORPO
    # =========================================================

    corpo = aplicar_transformacao(
        quadrado,
        translacao=(0, 0),
        rotacao=0,
        escala=(2, 2)
    )

    # =========================================================
    # TRANSFORMAÇÕES DO PAINEL ESQUERDO
    # =========================================================

    painel_esquerdo = aplicar_transformacao(
        quadrado,
        translacao=(-4, 0),
        rotacao=35,
        escala=(2.8, 0.55)
    )

    # =========================================================
    # TRANSFORMAÇÕES DO PAINEL DIREITO
    # =========================================================

    painel_direito = aplicar_transformacao(
        quadrado,
        translacao=(4, 0),
        rotacao=-35,
        escala=(2.8, 0.55)
    )

    # =========================================================
    # TRANSFORMAÇÕES DA ANTENA
    # =========================================================

    antena_transformada = aplicar_transformacao(
        antena,
        translacao=(0, 2),
        rotacao=0,
        escala=(0.7, 0.5)
    )

    # =========================================================
    # MOSTRA AS MATRIZES RESULTANTES
    # =========================================================

    print("Corpo transformado:")
    print(np.round(corpo, 2), "\n")

    print("Painel esquerdo transformado:")
    print(np.round(painel_esquerdo, 2), "\n")

    print("Painel direito transformado:")
    print(np.round(painel_direito, 2), "\n")

    print("Antena transformada:")
    print(np.round(antena_transformada, 2), "\n")

    # =========================================================
    # RENDERIZAÇÃO
    # =========================================================

    fig, ax = plt.subplots(
        figsize=(10, 8)
    )

    desenhar_objeto(
        ax,
        corpo,
        "gray",
        "Corpo Principal",
        alpha=0.30
    )

    desenhar_objeto(
        ax,
        painel_esquerdo,
        "blue",
        "Painel Esquerdo",
        alpha=0.25
    )

    desenhar_objeto(
        ax,
        painel_direito,
        "blue",
        "Painel Direito",
        alpha=0.25
    )

    desenhar_objeto(
        ax,
        antena_transformada,
        "red",
        "Antena",
        alpha=0.30
    )

    # =========================================================
    # CONFIGURAÇÃO DO SRU
    # =========================================================

    ax.set_title(
        "Cena Montada: Satélite no SRU",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")

    ax.set_xlim(-8, 8)
    ax.set_ylim(-6, 6)

    ax.axhline(
        0,
        color="black",
        linewidth=1
    )

    ax.axvline(
        0,
        color="black",
        linewidth=1
    )

    ax.grid(
        True,
        linestyle=":",
        alpha=0.5
    )

    ax.set_aspect(
        "equal",
        adjustable="box"
    )

    ax.legend(
        loc="upper right"
    )

    # Salva a imagem para usar no relatório
    plt.savefig(
        "satelite_sru.png",
        dpi=300,
        bbox_inches="tight"
    )

    print("Renderizando o satélite...")
    print("Imagem salva como 'satelite_sru.png'.")

    plt.show()


if __name__ == "__main__":
    main()