import cv2
import numpy as np
import math

def desenhar_estrela_5_pontas(tela, centro_x, centro_y, raio_externo, cor):
    pontos = []
    raio_interno = raio_externo * 0.45

    for i in range(10):
        angulo_graus = -90 + i * 36
        angulo_rad = math.radians(angulo_graus)

        if i % 2 == 0:
            raio_atual = raio_externo
        else:
            raio_atual = raio_interno

        x = int(centro_x + raio_atual * math.cos(angulo_rad))
        y = int(centro_y + raio_atual * math.sin(angulo_rad))

        pontos.append([x, y])

    pontos = np.array(pontos, np.int32)
    pontos = pontos.reshape((-1, 1, 2))

    cv2.fillPoly(
        tela,
        [pontos],
        cor
    )

def main():
    print("Iniciando desenho da Bandeira do Brasil...")

    largura = 900
    altura = 600

    tela = np.zeros(
        (altura, largura, 3),
        dtype=np.uint8
    )

    verde = (0, 156, 0)
    amarelo = (0, 220, 255)
    azul = (130, 50, 0)
    branco = (255, 255, 255)

    # Fundo verde
    tela[:] = verde

    # Centro da bandeira
    centro_x = largura // 2
    centro_y = altura // 2

    losango = np.array([
        [centro_x, 100],
        [750, centro_y],
        [centro_x, 500],
        [150, centro_y]
    ], np.int32)

    losango = losango.reshape((-1, 1, 2))

    cv2.fillPoly(
        tela,
        [losango],
        amarelo
    )

    raio_circulo = 95

    cv2.circle(
        tela,
        (centro_x, centro_y),
        raio_circulo,
        azul,
        -1
    )

    camada_faixa = np.zeros_like(tela)

    cv2.rectangle(
        camada_faixa,
        (centro_x - 110, centro_y - 8),
        (centro_x + 110, centro_y + 8),
        branco,
        -1
    )

    mascara_circulo = np.zeros(
        (altura, largura),
        dtype=np.uint8
    )

    cv2.circle(
        mascara_circulo,
        (centro_x, centro_y),
        raio_circulo,
        255,
        -1
    )

    faixa_recortada = cv2.bitwise_and(
        camada_faixa,
        camada_faixa,
        mask=mascara_circulo
    )

    tela = cv2.add(
        tela,
        faixa_recortada
    )

    estrelas = [
        (-12, -68, 5),
        (18, -62, 5),
        (42, -52, 5),
        (-38, -58, 5),
        (-58, -40, 5),
        (-22, -48, 4),
        (4, -44, 4),
        (28, -38, 4),
        (56, -30, 4),
        (-44, -24, 4),
        (-8, -28, 4),
        (14, -22, 4),
        (40, -18, 4),

        (-70, 22, 5),
        (-52, 36, 4),
        (-30, 50, 5),
        (-6, 58, 5),
        (18, 46, 4),
        (40, 36, 4),
        (62, 24, 5),
        (-42, 20, 4),
        (-18, 28, 4),
        (6, 24, 4),
        (28, 22, 4),
        (52, 18, 4),
        (-8, 76, 3),
        (34, 62, 4)
    ]

    for estrela in estrelas:
        desloc_x, desloc_y, raio = estrela

        desenhar_estrela_5_pontas(
            tela,
            centro_x + desloc_x,
            centro_y + desloc_y,
            raio,
            branco
        )

    cv2.imwrite(
        "bandeira_brasil.png",
        tela
    )

    print("Imagem salva como 'bandeira_brasil.png'.")

    cv2.imshow(
        "Bandeira do Brasil - CEFET-MG",
        tela
    )

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()