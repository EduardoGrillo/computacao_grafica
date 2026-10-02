# Dia 12/08/2026
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("Iniciando laboratório de Rasterização de imagens...")

    # Definando resolução da imagem. "Monitor Simulado (15x15 pixels)"
    largura, altura = 15, 15

    framebuffer = np.zeros((altura, largura))

    x0, y0 = 2, 2
    x1, y1 = 12, 9

    passos = max(abs(x1 - x0), abs(y1 - y0))

    inc_x = (x1 - x0) / passos
    inc_y = (y1 - y0) / passos

    x_atual, y_atual = x0, y0

    for i in range(passos + 1):
        pixel_x = int(round(x_atual))
        pixel_y = int(round(y_atual))

        framebuffer[pixel_y, pixel_x] = 1.0

        x_atual += inc_x
        y_atual += inc_y

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        fig.patch.set_facecolor('black')
        
        ax1.set_facecolor('black')
        ax1.set_title("O Vetor (Matemática Contínua)", color='white')
        ax1.set_xlim(0, largura)
        ax1.set_ylim(0, altura)

        ax1.plot([x0, x1], [y0, y1], color='red', linewidth=2, label='Vetor Ideal')
        ax1.grid(True, color='white', alpha=0.2)
        ax1.legend()
        ax1.tick_params(colors='white')

        ax2.set_title("Rasterização (Grade de Pixels)", color='white')
        ax2.imshow(framebuffer, cmap='gray', origin='lower', extent=[0, largura, 0, altura])
        ax2.plot([x0, x1], [y0, y1], color='red', linewidth=2, linestyle='--', alpha=0.5)
        ax2.grid(True, color='white', alpha=0.2)
        ax2.tick_params(colors='white')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()