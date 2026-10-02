# Dia 12/08/2026
from PIL import Image

def main():
    print("Iniciando laboratório de Rasterização do círculo...")

    largura_tela, altura_tela = 300, 300
    img = Image.new("RGB", (largura_tela, altura_tela), "white")

    centro_x = 150
    centro_y = 150
    raio = 50

    raio_quadrado = raio ** 2

    x_min = centro_x - raio
    x_max = centro_x + raio
    y_min = centro_y - raio
    y_max = centro_y + raio

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            # distancia_quadrada = (x - centro_x) ** 2 + (y - centro_y) ** 2 -> Círculo
            distancia_quadrada = (x - centro_x) + (y - centro_y) # Para fazer um quadrado, basta remover o **2 da linha acima.

            if distancia_quadrada <= raio_quadrado:
                img.putpixel((x, y), (255, 0, 0))

    img.save("circulo_rasterizado.png")
    print("Círculo salvo como 'circulo_rasterizado.png'.")

if __name__ == "__main__":
    main()

