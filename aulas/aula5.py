# Dia 19/08/2026

from PIL import Image


def criar_imagem_rgb(largura, altura, cor_rgb, nome_arquivo):
    """Cria uma imagem RGB com uma cor sólida e a salva em disco."""

    imagem = Image.new("RGB", (largura, altura), cor_rgb)
    imagem.save(f"{nome_arquivo}.png")

    print(f"[Sucesso] Imagem RGB {nome_arquivo} criada com sucesso.")


def criar_imagem_cmyk(largura, altura, cor_cmyk, nome_arquivo):
    """Cria uma imagem CMYK com uma cor sólida e a salva em disco."""

    c_int = int((cor_cmyk[0] / 100) * 255)
    m_int = int((cor_cmyk[1] / 100) * 255)
    y_int = int((cor_cmyk[2] / 100) * 255)
    k_int = int((cor_cmyk[3] / 100) * 255)

    imagem = Image.new(
        "CMYK",
        (largura, altura),
        (c_int, m_int, y_int, k_int)
    )

    imagem.save(f"{nome_arquivo}.jpg")

    print(f"[Sucesso] Imagem CMYK {nome_arquivo} criada com sucesso.")


def rgb_para_cmyk(r, g, b):
    """Converte uma cor RGB para CMYK."""

    # Preto absoluto
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 100

    r_prime = r / 255.0
    g_prime = g / 255.0
    b_prime = b / 255.0

    k = 1.0 - max(r_prime, g_prime, b_prime)

    c = (1.0 - r_prime - k) / (1.0 - k)
    m = (1.0 - g_prime - k) / (1.0 - k)
    y = (1.0 - b_prime - k) / (1.0 - k)

    # Convertendo para porcentagem
    c = round(c * 100, 2)
    m = round(m * 100, 2)
    y = round(y * 100, 2)
    k = round(k * 100, 2)

    return c, m, y, k


if __name__ == "__main__":

    LARGURA = 400
    ALTURA = 400

    # Amarelo em RGB
    cor_amarela_rgb = (255, 255, 0)

    print(f"Cor Amarela em RGB: {cor_amarela_rgb}")

    criar_imagem_rgb(
        LARGURA,
        ALTURA,
        cor_amarela_rgb,
        "cor_rgb"
    )

    # Converter RGB para CMYK
    cor_amarela_cmyk = rgb_para_cmyk(
        cor_amarela_rgb[0],
        cor_amarela_rgb[1],
        cor_amarela_rgb[2]
    )

    print(f"Cor Amarela em CMYK: {cor_amarela_cmyk}")

    criar_imagem_cmyk(
        LARGURA,
        ALTURA,
        cor_amarela_cmyk,
        "cor_cmyk_conversao"
    )