import colorsys
from PIL import Image, ImageDraw

def aplicar_chroma_key(
    nome_imagem,
    nome_saida,
    hue_min=90,
    hue_max=150,
    saturacao_min=25,
    brilho_min=15
):
    print("Iniciando aplicação do Chroma Key...")
    imagem = Image.open(nome_imagem).convert("RGBA")
    largura, altura = imagem.size

    # Cria uma máscara inicialmente totalmente opaca
    mascara = Image.new(
        "L",
        (largura, altura),
        255
    )

    desenho_mascara = ImageDraw.Draw(mascara)

    hue_min_norm = hue_min / 360.0
    hue_max_norm = hue_max / 360.0

    saturacao_min_norm = saturacao_min / 100.0
    brilho_min_norm = brilho_min / 100.0

    pixels = imagem.load()

    for y in range(altura):
        for x in range(largura):

            r, g, b, a = pixels[x, y]

            # RGB de 0-255 -> RGB normalizado de 0.0-1.0
            r_norm = r / 255.0
            g_norm = g / 255.0
            b_norm = b / 255.0

            # Converte RGB para HSV
            h, s, v = colorsys.rgb_to_hsv(
                r_norm,
                g_norm,
                b_norm
            )

            # Verifica se o pixel pertence à faixa de verde
            eh_verde = (
                hue_min_norm <= h <= hue_max_norm
                and s >= saturacao_min_norm
                and v >= brilho_min_norm
            )

            # Pixels verdes recebem Alpha = 0
            if eh_verde:
                desenho_mascara.point(
                    (x, y),
                    fill=0
                )

    imagem.putalpha(mascara)

    # Salva obrigatoriamente em PNG,
    # pois o formato suporta transparência
    imagem.save(nome_saida)

    print(
        f"Chroma Key concluído. "
        f"Imagem salva como '{nome_saida}'."
    )

    return imagem

def adicionar_novo_fundo(
    imagem_transparente,
    nome_fundo,
    nome_saida
):
    print("Adicionando novo fundo...")
    fundo = Image.open(nome_fundo).convert("RGBA")

    # Faz o fundo possuir o mesmo tamanho da imagem principal
    fundo = fundo.resize(
        imagem_transparente.size
    )

    # Sobrepõe a pessoa transparente ao novo fundo
    resultado = Image.alpha_composite(
        fundo,
        imagem_transparente
    )

    resultado.save(nome_saida)

    print(
        f"Imagem final salva como '{nome_saida}'."
    )


def main():
    imagem_transparente = aplicar_chroma_key(
        nome_imagem="chroma_original.png",
        nome_saida="chroma_transparente.png"
    )

    adicionar_novo_fundo(
        imagem_transparente,
        nome_fundo="fundo.png",
        nome_saida="chroma_resultado.png"
    )

if __name__ == "__main__":
    main()