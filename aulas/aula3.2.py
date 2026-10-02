# Dia 12/08/2026

from PIL import Image


def renderizar_circulo(fator_qualidade):
    print("Iniciando laboratório de Rasterização do círculo...")

    largura_base = 300
    raio_base = 50

    largura_tela = int(largura_base * fator_qualidade)
    altura_tela = int(largura_base * fator_qualidade)
    raio = int(raio_base * fator_qualidade)

    centro_x = int(largura_tela / 2)
    centro_y = int(altura_tela / 2)

    raio_quadrado = raio ** 2

    # Cria a imagem com fundo branco
    img = Image.new(
        "RGB",
        (largura_tela, altura_tela),
        "white"
    )

    x_min = centro_x - raio
    x_max = centro_x + raio

    y_min = centro_y - raio
    y_max = centro_y + raio

    # Rasterização do círculo
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):

            distancia_quadrada = (
                (x - centro_x) ** 2 +
                (y - centro_y) ** 2
            )

            if distancia_quadrada <= raio_quadrado:
                img.putpixel((x, y), (255, 0, 0))

    return img


def main():
    print("Iniciando - Resolução e Aliasing...")

    # Gera primeiro uma imagem bem pequena (30x30)
    img_baixa = renderizar_circulo(
        fator_qualidade=0.1
    )

    # Amplia para 300x300 sem suavização
    img_baixa_ampliada = img_baixa.resize(
        (300, 300),
        Image.Resampling.NEAREST
    )

    # Salva a imagem
    img_baixa_ampliada.save(
        "circulo_1_baixa_resolucao.png"
    )

    # Abre a imagem gerada
    img_baixa_ampliada.show()

    print(
        "Gerado: Círculo salvo como "
        "'circulo_1_baixa_resolucao.png'."
    )


if __name__ == "__main__":
    main()