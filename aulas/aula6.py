from PIL import Image

def criar_composicao_alpha():
    print("\n--- Composição com Canal Alpha (RGBA) ---")
    largura, altura = 400, 400

    fundo = Image.new("RGBA", (largura, altura), (255, 0, 0, 255)) 
    fundo.save("fundo_alpha.png")
    print("[Sucesso] Imagem 'fundo_alpha.png' salva.")

    primeiro_plano = Image.new("RGBA", (largura, altura), (0, 0, 255, 127))
    primeiro_plano.save("primeiro_plano_alpha.png")
    print("[Sucesso] Imagem 'primeiro_plano_alpha.png' salva.")

    resultado = Image.alpha_composite(fundo, primeiro_plano)
    resultado.save("resultado_alpha.png")
    print("[Sucesso] Imagem 'resultado_alpha.png' salva.")

if __name__ == "__main__":
    criar_composicao_alpha()