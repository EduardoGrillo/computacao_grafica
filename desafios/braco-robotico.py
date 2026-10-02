import cv2
import numpy as np
import math


def main():
    print("Iniciando Braço Robótico 2D...")
    largura = 600
    altura = 600

    tela = np.zeros(
        (altura, largura, 3),
        dtype=np.uint8
    )

    base_x = 150
    base_y = 500
    comprimento_1 = 230
    comprimento_2 = 180
    angulo_ombro = 65
    angulo_cotovelo = -45

    angulo_ombro_rad = math.radians(
        angulo_ombro
    )

    # O segundo elo depende da soma dos ângulos
    angulo_total_rad = math.radians(
        angulo_ombro + angulo_cotovelo
    )

    cotovelo_x = base_x + int(
        comprimento_1 *
        math.cos(angulo_ombro_rad)
    )

    # Subtraímos porque na tela o eixo Y cresce para baixo
    cotovelo_y = base_y - int(
        comprimento_1 *
        math.sin(angulo_ombro_rad)
    )

    ponta_x = cotovelo_x + int(
        comprimento_2 *
        math.cos(angulo_total_rad)
    )

    ponta_y = cotovelo_y - int(
        comprimento_2 *
        math.sin(angulo_total_rad)
    )

    # Mostra as coordenadas calculadas
    print(
        f"Base: ({base_x}, {base_y})"
    )

    print(
        f"Cotovelo: ({cotovelo_x}, {cotovelo_y})"
    )

    print(
        f"Ponta: ({ponta_x}, {ponta_y})"
    )

    cv2.rectangle(
        tela,
        (100, 500),
        (200, 590),
        (100, 100, 100),
        -1
    )

    cv2.line(
        tela,
        (base_x, base_y),
        (cotovelo_x, cotovelo_y),
        (220, 220, 220),
        14
    )

    cv2.line(
        tela,
        (cotovelo_x, cotovelo_y),
        (ponta_x, ponta_y),
        (220, 220, 220),
        14
    )

    cv2.circle(
        tela,
        (base_x, base_y),
        18,
        (0, 0, 255),
        -1
    )

    cv2.circle(
        tela,
        (cotovelo_x, cotovelo_y),
        18,
        (0, 0, 255),
        -1
    )

    cv2.circle(
        tela,
        (ponta_x, ponta_y),
        15,
        (0, 255, 255),
        -1
    )

    cv2.imshow(
        "Braco Robotico 2D - CEFET-MG",
        tela
    )

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()