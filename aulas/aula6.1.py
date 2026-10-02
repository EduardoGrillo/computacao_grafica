import colorsys
from PIL import Image


def criar_imagem_via_hsv(
    largura,
    altura,
    h_graus,
    s_pct,
    v_pct,
    nome_arquivo
):
    # Converte os valores para a escala de 0 a 1
    h_norm = h_graus / 360.0
    s_norm = s_pct / 100.0
    v_norm = v_pct / 100.0

    # HSV -> RGB
    r_float, g_float, b_float = colorsys.hsv_to_rgb(
        h_norm,
        s_norm,
        v_norm
    )

    # Converte RGB de 0-1 para 0-255
    r = int(r_float * 255)
    g = int(g_float * 255)
    b = int(b_float * 255)

    # Cria e salva a imagem
    imagem = Image.new(
        "RGB",
        (largura, altura),
        (r, g, b)
    )

    imagem.save(nome_arquivo)

    print(
        f"[HSV] Imagem salva: {nome_arquivo} "
        f"| RGB FINAL: ({r}, {g}, {b})"
    )


def criar_imagem_via_hsl(
    largura,
    altura,
    h_graus,
    s_pct,
    l_pct,
    nome_arquivo
):
    # Converte os valores para a escala de 0 a 1
    h_norm = h_graus / 360.0
    s_norm = s_pct / 100.0
    l_norm = l_pct / 100.0

    # O colorsys trabalha com HLS:
    # Hue, Lightness, Saturation
    r_float, g_float, b_float = colorsys.hls_to_rgb(
        h_norm,
        l_norm,
        s_norm
    )

    # Converte RGB de 0-1 para 0-255
    r = int(r_float * 255)
    g = int(g_float * 255)
    b = int(b_float * 255)

    # Cria e salva a imagem
    imagem = Image.new(
        "RGB",
        (largura, altura),
        (r, g, b)
    )

    imagem.save(nome_arquivo)

    print(
        f"[HSL] Imagem salva: {nome_arquivo} "
        f"| RGB FINAL: ({r}, {g}, {b})"
    )


if __name__ == "__main__":

    LARGURA = 400
    ALTURA = 400

    # Ciano usando HSV
    criar_imagem_via_hsv(
        LARGURA,
        ALTURA,
        180,
        100,
        100,
        "ciano_hsv.png"
    )

    # Ciano usando HSL
    criar_imagem_via_hsl(
        LARGURA,
        ALTURA,
        180,
        100,
        50,
        "ciano_hsl.png"
    )

    # Ciano pastel usando HSL
    criar_imagem_via_hsl(
        LARGURA,
        ALTURA,
        180,
        100,
        80,
        "ciano_pastel_hsl.png"
    )