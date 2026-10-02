# dia 28/08/26
import  numpy as np

def imprimir_ponto(nome_espaco, vetor):
    print(f"{nome_espaco}: (X: {vetor[0][0]:.2f}, Y: {vetor[1][0]:.2f}, W: {vetor[2][0]:.2f})")

def simulador_pipeline_grafico():
    print("SIMULAÇÃO DO PIPELINE GRÁFICO 2D\n")

    P_SRO = np.array([[5.0],[2.0], [1.0]])
    imprimir_ponto("1. SRO (Objeto)", P_SRO)

    Matriz_Model = np.array([
        [1, 0, 100],
        [0, 1, 50],
        [0, 0, 1]   
    ])

    P_SRU = Matriz_Model @ P_SRO
    imprimir_ponto("2. SRU (Universo)", P_SRU)

    largura_mundo = 200.0
    altura_mundo = 100.0

    Matriz_Normalizacao = np.array([
        [2.0/largura_mundo, 0, -1],
        [0, 2.0/altura_mundo, -1],
        [0, 0, 1]   
    ])

    P_SRN = Matriz_Normalizacao @ P_SRU
    imprimir_ponto("3. SRN (Normalizado)", P_SRN)

    largura_tela = 800.0
    altura_tela = 600.0

    Matriz_Viewport = np.array([
        [largura_tela/2.0, 0, largura_tela/2.0],
        [0, -altura_tela/2.0, altura_tela/2.0],
        [0, 0, 1]
    ])

    P_SRD = Matriz_Viewport @ P_SRN
    imprimir_ponto("4. SRD (Dispositivo/Tela)", P_SRD)

if __name__ == "__main__":
    simulador_pipeline_grafico()