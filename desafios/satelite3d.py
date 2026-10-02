import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def matriz_translacao_3d(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ], dtype=np.float32)


def matriz_escala_3d(sx, sy, sz):
    return np.array([
        [sx, 0,  0,  0],
        [0,  sy, 0,  0],
        [0,  0,  sz, 0],
        [0,  0,  0,  1]
    ], dtype=np.float32)


def matriz_rotacao_x(angulo_graus):
    theta = np.radians(angulo_graus)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    return np.array([
        [1, 0,     0,    0],
        [0, cos_t, -sin_t, 0],
        [0, sin_t,  cos_t, 0],
        [0, 0,     0,    1]
    ], dtype=np.float32)


def matriz_rotacao_y(angulo_graus):
    theta = np.radians(angulo_graus)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    return np.array([
        [ cos_t, 0, sin_t, 0],
        [ 0,     1, 0,     0],
        [-sin_t, 0, cos_t, 0],
        [ 0,     0, 0,     1]
    ], dtype=np.float32)


def matriz_rotacao_z(angulo_graus):
    theta = np.radians(angulo_graus)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    return np.array([
        [cos_t, -sin_t, 0, 0],
        [sin_t,  cos_t, 0, 0],
        [0,      0,     1, 0],
        [0,      0,     0, 1]
    ], dtype=np.float32)


def aplicar_transformacao_3d(
    vertices,
    translacao=(0, 0, 0),
    rotacao=(0, 0, 0),
    escala=(1, 1, 1)
):
    tx, ty, tz = translacao
    rx, ry, rz = rotacao
    sx, sy, sz = escala

    M_T = matriz_translacao_3d(tx, ty, tz)
    M_Rx = matriz_rotacao_x(rx)
    M_Ry = matriz_rotacao_y(ry)
    M_Rz = matriz_rotacao_z(rz)
    M_S = matriz_escala_3d(sx, sy, sz)

    # Ordem da direita para a esquerda:
    # Escala -> Rx -> Ry -> Rz -> Translação
    M_composta = M_T @ M_Rz @ M_Ry @ M_Rx @ M_S

    return M_composta @ vertices


def criar_prisma():
    # Prisma/cubo base centrado na origem
    return np.array([
        [-1,  1,  1, -1, -1,  1,  1, -1],  # X
        [-1, -1,  1,  1, -1, -1,  1,  1],  # Y
        [-1, -1, -1, -1,  1,  1,  1,  1],  # Z
        [ 1,  1,  1,  1,  1,  1,  1,  1]   # W
    ], dtype=np.float32)


def criar_piramide():
    # Base quadrada + ápice
    return np.array([
        [-1,  1,  1, -1,  0],  # X
        [-1, -1,  1,  1,  0],  # Y
        [ 0,  0,  0,  0,  2],  # Z
        [ 1,  1,  1,  1,  1]   # W
    ], dtype=np.float32)


def desenhar_prisma(ax, vertices, cor, label, estilo="-"):
    x = vertices[0, :]
    y = vertices[1, :]
    z = vertices[2, :]

    arestas = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # base inferior
        (4, 5), (5, 6), (6, 7), (7, 4),  # base superior
        (0, 4), (1, 5), (2, 6), (3, 7)   # ligações verticais
    ]

    ax.scatter(x, y, z, color=cor, s=25)

    for i, (inicio, fim) in enumerate(arestas):
        lbl = label if i == 0 else ""
        ax.plot(
            [x[inicio], x[fim]],
            [y[inicio], y[fim]],
            [z[inicio], z[fim]],
            color=cor,
            linewidth=2,
            linestyle=estilo,
            label=lbl
        )


def desenhar_piramide(ax, vertices, cor, label, estilo="-"):
    x = vertices[0, :]
    y = vertices[1, :]
    z = vertices[2, :]

    arestas = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # base
        (0, 4), (1, 4), (2, 4), (3, 4)   # laterais
    ]

    ax.scatter(x, y, z, color=cor, s=25)

    for i, (inicio, fim) in enumerate(arestas):
        lbl = label if i == 0 else ""
        ax.plot(
            [x[inicio], x[fim]],
            [y[inicio], y[fim]],
            [z[inicio], z[fim]],
            color=cor,
            linewidth=2,
            linestyle=estilo,
            label=lbl
        )


def main():
    print("=== Satélite 3D no SRU ===\n")

    # =========================================================
    # PRIMITIVAS NO SRO
    # =========================================================

    corpo_base = criar_prisma()
    painel_base = criar_prisma()
    antena_base = criar_piramide()

    # =========================================================
    # TRANSFORMAÇÕES
    # =========================================================

    # Corpo principal
    corpo = aplicar_transformacao_3d(
        corpo_base,
        translacao=(0, 0, 0),
        rotacao=(0, 0, 0),
        escala=(1.5, 0.8, 2.0)
    )

    # Painel esquerdo
    painel_esquerdo = aplicar_transformacao_3d(
        painel_base,
        translacao=(-4.2, 0, 0.3),
        rotacao=(0, 35, 0),
        escala=(2.8, 0.12, 0.6)
    )

    # Painel direito
    painel_direito = aplicar_transformacao_3d(
        painel_base,
        translacao=(4.2, 0, 0.3),
        rotacao=(0, -35, 0),
        escala=(2.8, 0.12, 0.6)
    )

    # Antena
    antena = aplicar_transformacao_3d(
        antena_base,
        translacao=(0, 0, 2.0),
        rotacao=(0, 0, 0),
        escala=(0.5, 0.5, 0.7)
    )

    # =========================================================
    # MOSTRANDO MATRIZES TRANSFORMADAS
    # =========================================================

    print("Corpo:")
    print(np.round(corpo, 2), "\n")

    print("Painel esquerdo:")
    print(np.round(painel_esquerdo, 2), "\n")

    print("Painel direito:")
    print(np.round(painel_direito, 2), "\n")

    print("Antena:")
    print(np.round(antena, 2), "\n")

    # =========================================================
    # RENDERIZAÇÃO 3D
    # =========================================================

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    desenhar_prisma(
        ax,
        corpo,
        "gray",
        "Corpo Principal",
        "-"
    )

    desenhar_prisma(
        ax,
        painel_esquerdo,
        "blue",
        "Painel Esquerdo",
        "-"
    )

    desenhar_prisma(
        ax,
        painel_direito,
        "blue",
        "Painel Direito",
        "-"
    )

    desenhar_piramide(
        ax,
        antena,
        "red",
        "Antena",
        "-"
    )

    # =========================================================
    # CONFIGURAÇÃO DO ESPAÇO CARTESIANO 3D
    # =========================================================

    ax.set_title(
        "Cena Montada: Satélite 3D no SRU",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Eixo X", fontweight="bold")
    ax.set_ylabel("Eixo Y", fontweight="bold")
    ax.set_zlabel("Eixo Z", fontweight="bold")

    limite = 7
    ax.set_xlim([-limite, limite])
    ax.set_ylim([-limite, limite])
    ax.set_zlim([-2, 5])

    ax.view_init(elev=22, azim=45)

    ax.legend()
    plt.tight_layout()

    plt.savefig(
        "satelite_3d.png",
        dpi=300,
        bbox_inches="tight"
    )

    print("Renderizando o satélite 3D...")
    print("Imagem salva como 'satelite_3d.png'.")

    plt.show()


if __name__ == "__main__":
    main()