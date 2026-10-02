# Dia 07/08/2026

import matplotlib.pyplot as plt
import time

def main():
    print("=== Simulador de FPS (Frames Por Segundo) ===")
    print("Valores: 5 (Travado), 24 (Cinema), 60 (Fluido)")

    try: 
        fps_alvo = int(input("Digite o FPS desejado para a simulação: "))

    except ValueError:
        fps_alvo = 30

    delta_time = 1.0 / fps_alvo
    print(f"Iniciando simulação com FPS padrão: {fps_alvo}")
    print(f"Tempo de atualização por frame: {delta_time:.4f} segundos")

    plt.ion()

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('black')

    ax.set_facecolor('black')
    ax.set_title(f"Simulação Gráfica rodando a {fps_alvo} FPS", color='white')

    ax.grid(True, color='white', linestyle='--', alpha=0.3)
    ax.tick_params(colors='white')

    for spine in ax.spines.values():
        spine.set_color('white')

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)

    objeto, = ax.plot([], [], marker='o', color='red', markersize=20)
    posicao_x = 0
    valocidade = 50

    tempo_anterior = time.time()

    while posicao_x <= 100:
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - tempo_anterior
        tempo_anterior = tempo_atual
        posicao_x += valocidade * tempo_decorrido

        objeto.set_data([posicao_x], [5])
        plt.pause(delta_time)

    print("Animação concluída.")

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()
