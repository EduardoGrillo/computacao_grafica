def main():
    print("Iniciando a síntese do círculo vetorial...")

    largura_tela = 300
    altura_tela = 300

    centro_x = 150
    centro_y = 150

    raio = 50
    cor_preenchimento = "red"

    # Criação do código SVG
    codigo_vetorial_svg = f"""
<svg width="{largura_tela}"
     height="{altura_tela}"
     xmlns="http://www.w3.org/2000/svg">

    <rect width="100%" height="100%" fill="white" />

    <circle
        cx="{centro_x}"
        cy="{centro_y}"
        r="{raio}"
        fill="{cor_preenchimento}"
    />

</svg>
"""

    nome_arquivo_svg = "circulo_vetorial.svg"

    # Salva o SVG em um arquivo
    with open(nome_arquivo_svg, "w", encoding="utf-8") as arquivo_svg:
        arquivo_svg.write(codigo_vetorial_svg)

    print(f"Arquivo vetorial gerado: '{nome_arquivo_svg}'.")
    print("Você pode abrir o arquivo no navegador para visualizar o círculo.")


if __name__ == "__main__":
    main()