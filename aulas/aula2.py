# Dia 07/08/2026

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def construir_plano_cartesiano(eixo_x: float, eixo_y: float, title: str):
    fig, ax = plt.subplots(figsize=(7, 7))

    # Fundo da janela
    fig.patch.set_facecolor('black')

    # Fundo do plano cartesiano
    ax.set_facecolor('black')

    # Limites dos eixos
    ax.set_xlim(0, eixo_x)
    ax.set_ylim(0, eixo_y)

    # Título
    ax.set_title(title, color='white')

    # Grade
    ax.grid(
        color='white',
        linestyle='--',
        alpha=0.3
    )

    # Cor dos números dos eixos
    ax.tick_params(colors='white')

    # Cor das bordas
    for spine in ax.spines.values():
        spine.set_color('white')

    return fig, ax


def main():
    print("Dispositivos de Entrada...")

    fig, ax = construir_plano_cartesiano(
        eixo_x=15,
        eixo_y=15,
        title='Clique 3 vezes para gerar a Primitiva Gráfica'
    )

    # Lista que armazenará as coordenadas dos cliques
    coordenadas_entrada = []

    def ao_clicar(event):

        # Verifica se o clique ocorreu dentro do plano cartesiano
        if event.xdata is None or event.ydata is None:
            return

        # Captura da Entrada (Dispositivo Localizador)
        x = event.xdata
        y = event.ydata

        coordenadas_entrada.append([x, y])

        print(
            f"Entrada do Mouse --> Coordenada: "
            f"({x:.2f}, {y:.2f})"
        )

        # Desenha o ponto onde o usuário clicou
        ax.plot(
            x,
            y,
            'ro'
        )

        fig.canvas.draw()

        # Quando houver exatamente 3 pontos
        if len(coordenadas_entrada) == 3:

            print("Desenhando a primitiva de Polígono")

            triangulo = patches.Polygon(
                coordenadas_entrada,
                closed=True,
                fill=True,
                facecolor='green',
                alpha=0.6,
                edgecolor='red',
                linewidth=3
            )

            # Adiciona o triângulo ao plano
            ax.add_patch(triangulo)

            # Atualiza a tela
            fig.canvas.draw()

            # Limpa as coordenadas para permitir
            # desenhar outro triângulo
            coordenadas_entrada.clear()

    # Cria o "ouvinte" que conecta
    # o clique do mouse à função ao_clicar
    fig.canvas.mpl_connect(
        'button_press_event',
        ao_clicar
    )

    print(
        "Aguardando entrada do usuário "
        "na interface gráfica..."
    )

    plt.show()


if __name__ == "__main__":
    main()