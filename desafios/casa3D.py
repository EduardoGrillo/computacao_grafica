import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from PIL import Image
import ctypes
import os

# SHADERS
VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCord;
out vec2 TexCord;
uniform mat4 MVP;
void main()
{
    gl_Position = MVP * vec4(aPos, 1.0);
    TexCord = aTexCord;
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec2 TexCord;
out vec4 FragColor;
uniform sampler2D textura_bloco;
void main()
{
    FragColor = texture(textura_bloco, TexCord);
}
"""

# TEXTURAS
def recortar_fundo_claro(imagem):
    imagem_rgb = imagem.convert("RGB")
    dados = np.array(imagem_rgb)
    mascara = np.any(dados < 220, axis=2)

    if not np.any(mascara):
        return imagem

    ys, xs = np.where(mascara)
    margem = 4

    x_min = max(int(xs.min()) - margem, 0)
    x_max = min(int(xs.max()) + margem, imagem.width - 1)
    y_min = max(int(ys.min()) - margem, 0)
    y_max = min(int(ys.max()) + margem, imagem.height - 1)

    return imagem.crop((x_min, y_min, x_max + 1, y_max + 1))

def carregar_textura(caminho_arquivo, recortar_porta=False):
    caminho_arquivo = os.path.normpath(caminho_arquivo)

    print("\nCarregando textura:")
    print(caminho_arquivo)

    if not os.path.exists(caminho_arquivo):
        print("ERRO: arquivo nao encontrado!")
        print("Sera usada a textura de erro rosa/preta.")

        largura, altura = 2, 2
        imagem_dados = np.array([
            255, 0, 255, 255, 0, 0, 0, 255,
            0, 0, 0, 255, 255, 0, 255, 255
        ], dtype=np.uint8).tobytes()
    else:
        imagem = Image.open(caminho_arquivo)

        if recortar_porta:
            imagem = recortar_fundo_claro(imagem)

        imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)
        imagem_dados = imagem.convert("RGBA").tobytes()
        largura, altura = imagem.size
        print(f"OK: {largura}x{altura}")

    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        largura,
        altura,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        imagem_dados
    )

    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)

    return textura_id

# MATRIZES
def matriz_perspectiva(fov, aspecto, perto, longe):
    f = 1.0 / np.tan(np.radians(fov) / 2.0)
    m = np.zeros((4, 4), dtype=np.float32)

    m[0, 0] = f / aspecto
    m[1, 1] = f
    m[2, 2] = (longe + perto) / (perto - longe)
    m[2, 3] = (2.0 * longe * perto) / (perto - longe)
    m[3, 2] = -1.0

    return m

def matriz_translacao(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def matriz_rotacao_x(graus):
    c = np.cos(np.radians(graus))
    s = np.sin(np.radians(graus))

    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def matriz_rotacao_y(graus):
    c = np.cos(np.radians(graus))
    s = np.sin(np.radians(graus))

    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

# PRISMA TEXTURIZADO GENERICO
def criar_prisma_texturizado(
    x_min,
    x_max,
    y_min,
    y_max,
    z_min,
    z_max,
    repeticao_u=1.0,
    repeticao_v=1.0
):
    u = repeticao_u
    v = repeticao_v

    vertices = np.array([
        # Frente
        x_min, y_min, z_max, 0.0, 0.0,
        x_max, y_min, z_max, u, 0.0,
        x_max, y_max, z_max, u, v,
        x_min, y_max, z_max, 0.0, v,

        # Traseira
        x_max, y_min, z_min, 0.0, 0.0,
        x_min, y_min, z_min, u, 0.0,
        x_min, y_max, z_min, u, v,
        x_max, y_max, z_min, 0.0, v,

        # Esquerda
        x_min, y_min, z_min, 0.0, 0.0,
        x_min, y_min, z_max, u, 0.0,
        x_min, y_max, z_max, u, v,
        x_min, y_max, z_min, 0.0, v,

        # Direita
        x_max, y_min, z_max, 0.0, 0.0,
        x_max, y_min, z_min, u, 0.0,
        x_max, y_max, z_min, u, v,
        x_max, y_max, z_max, 0.0, v,

        # Superior
        x_min, y_max, z_max, 0.0, 0.0,
        x_max, y_max, z_max, u, 0.0,
        x_max, y_max, z_min, u, v,
        x_min, y_max, z_min, 0.0, v,

        # Inferior
        x_min, y_min, z_min, 0.0, 0.0,
        x_max, y_min, z_min, u, 0.0,
        x_max, y_min, z_max, u, v,
        x_min, y_min, z_max, 0.0, v
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        8, 9, 10, 10, 11, 8,
        12, 13, 14, 14, 15, 12,
        16, 17, 18, 18, 19, 16,
        20, 21, 22, 22, 23, 20
    ], dtype=np.uint32)

    return vertices, indices

# ESTRUTURA DA CASA
def criar_corpo_casa():
    return criar_prisma_texturizado(
        x_min=-1.35,
        x_max=1.35,
        y_min=-1.15,
        y_max=0.85,
        z_min=-1.10,
        z_max=1.10,
        repeticao_u=4.0,
        repeticao_v=3.0
    )

def criar_telhado():
    y_base = 0.82
    y_topo = 1.72
    x_base = 1.65
    z_base = 1.42

    vertices = np.array([
        # Frente
        -x_base, y_base, z_base, 0.0, 0.0,
        x_base, y_base, z_base, 3.2, 0.0,
        0.0, y_topo, 0.0, 1.6, 2.4,

        # Direita
        x_base, y_base, z_base, 0.0, 0.0,
        x_base, y_base, -z_base, 3.2, 0.0,
        0.0, y_topo, 0.0, 1.6, 2.4,

        # Traseira
        x_base, y_base, -z_base, 0.0, 0.0,
        -x_base, y_base, -z_base, 3.2, 0.0,
        0.0, y_topo, 0.0, 1.6, 2.4,

        # Esquerda
        -x_base, y_base, -z_base, 0.0, 0.0,
        -x_base, y_base, z_base, 3.2, 0.0,
        0.0, y_topo, 0.0, 1.6, 2.4
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2,
        3, 4, 5,
        6, 7, 8,
        9, 10, 11
    ], dtype=np.uint32)

    return vertices, indices

def criar_porta():
    return criar_prisma_texturizado(
        x_min=-0.30,
        x_max=0.30,
        y_min=-1.14,
        y_max=0.05,
        z_min=1.095,
        z_max=1.135,
        repeticao_u=1.0,
        repeticao_v=1.0
    )

def criar_batente_esquerdo():
    return criar_prisma_texturizado(
        x_min=-0.36,
        x_max=-0.30,
        y_min=-1.14,
        y_max=0.12,
        z_min=1.105,
        z_max=1.17,
        repeticao_u=0.3,
        repeticao_v=1.0
    )

def criar_batente_direito():
    return criar_prisma_texturizado(
        x_min=0.30,
        x_max=0.36,
        y_min=-1.14,
        y_max=0.12,
        z_min=1.105,
        z_max=1.17,
        repeticao_u=0.3,
        repeticao_v=1.0
    )

def criar_batente_superior():
    return criar_prisma_texturizado(
        x_min=-0.36,
        x_max=0.36,
        y_min=0.05,
        y_max=0.13,
        z_min=1.105,
        z_max=1.17,
        repeticao_u=1.0,
        repeticao_v=0.2
    )

def criar_soleira():
    return criar_prisma_texturizado(
        x_min=-0.38,
        x_max=0.38,
        y_min=-1.18,
        y_max=-1.10,
        z_min=1.05,
        z_max=1.32,
        repeticao_u=1.0,
        repeticao_v=0.4
    )

def criar_base():
    # Pequeno embasamento para a casa não parecer flutuar.
    return criar_prisma_texturizado(
        x_min=-1.42,
        x_max=1.42,
        y_min=-1.23,
        y_max=-1.14,
        z_min=-1.17,
        z_max=1.17,
        repeticao_u=4.0,
        repeticao_v=0.4
    )

def criar_janela_esquerda():
    return criar_prisma_texturizado(
        x_min=-1.12,
        x_max=-0.62,
        y_min=-0.32,
        y_max=0.42,
        z_min=1.105,
        z_max=1.145,
        repeticao_u=1.0,
        repeticao_v=1.0
    )

def criar_janela_direita():
    return criar_prisma_texturizado(
        x_min=0.62,
        x_max=1.12,
        y_min=-0.32,
        y_max=0.42,
        z_min=1.105,
        z_max=1.145,
        repeticao_u=1.0,
        repeticao_v=1.0
    )

def criar_chamine():
    return criar_prisma_texturizado(
        x_min=0.62,
        x_max=0.92,
        y_min=1.18,
        y_max=2.02,
        z_min=-0.48,
        z_max=-0.18,
        repeticao_u=1.0,
        repeticao_v=1.5
    )

def criar_chao():
    return criar_prisma_texturizado(
        x_min=-3.60,
        x_max=3.60,
        y_min=-1.28,
        y_max=-1.22,
        z_min=-3.20,
        z_max=3.20,
        repeticao_u=10.0,
        repeticao_v=10.0
    )

# MEMORIA DA GPU
def criar_objeto_gpu(vertices, indices):
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    passo = 5 * vertices.itemsize

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, passo, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(
        1,
        2,
        GL_FLOAT,
        GL_FALSE,
        passo,
        ctypes.c_void_p(3 * vertices.itemsize)
    )
    glEnableVertexAttribArray(1)

    glBindVertexArray(0)

    return VAO, VBO, EBO

def desenhar_objeto(VAO, indices, textura_id, loc_tex):
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glUniform1i(loc_tex, 0)

    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    glBindVertexArray(0)

# MAIN
def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    largura_janela = 900
    altura_janela = 700

    janela = glfw.create_window(
        largura_janela,
        altura_janela,
        "Casa 3D com Texturas - Use as SETAS",
        None,
        None
    )

    if not janela:
        glfw.terminate()
        return

    glfw.make_context_current(janela)
    glfw.swap_interval(1)

    glEnable(GL_DEPTH_TEST)

    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )

    # CAMINHOS DAS TEXTURAS
    pasta_atual = os.path.dirname(os.path.abspath(__file__))

    caminho_parede = os.path.join(pasta_atual, "texturas", "parede.jpg")
    caminho_porta = os.path.join(pasta_atual, "texturas", "porta.jpg")
    caminho_telhado = os.path.join(pasta_atual, "texturas", "telhado.jpg")
    caminho_grama = os.path.join(pasta_atual, "texturas", "grama.jpg")
    caminho_janela = os.path.join(pasta_atual, "texturas", "janela.jpg")

    textura_parede = carregar_textura(caminho_parede)
    textura_porta = carregar_textura(caminho_porta, recortar_porta=True)
    textura_telhado = carregar_textura(caminho_telhado)
    textura_grama = carregar_textura(caminho_grama)
    textura_janela = carregar_textura(caminho_janela)

    # GEOMETRIA
    geometrias = [
        # O chao e desenhado primeiro.
        (*criar_chao(), textura_grama),

        # Estrutura principal.
        (*criar_corpo_casa(), textura_parede),
        (*criar_telhado(), textura_telhado),

        # Detalhes da frente.
        (*criar_porta(), textura_porta),
        (*criar_batente_esquerdo(), textura_porta),
        (*criar_batente_direito(), textura_porta),
        (*criar_batente_superior(), textura_porta),
        (*criar_soleira(), textura_parede),

        # Janelas.
        (*criar_janela_esquerda(), textura_janela),
        (*criar_janela_direita(), textura_janela),

        # Chamine.
        (*criar_chamine(), textura_parede)
    ]

    objetos = []

    for vertices, indices, textura in geometrias:
        VAO, VBO, EBO = criar_objeto_gpu(vertices, indices)
        objetos.append((VAO, VBO, EBO, indices, textura))

    # MATRIZES
    matriz_proj = matriz_perspectiva(
        45.0,
        largura_janela / altura_janela,
        0.1,
        100.0
    )

    matriz_view = matriz_translacao(0, -0.05, -7.4)

    loc_mvp = glGetUniformLocation(shader, "MVP")
    loc_tex = glGetUniformLocation(shader, "textura_bloco")

    rot_x = 14.0
    rot_y = -36.0

    velocidade = 2.0

    print("\n=== CASA 3D ===")
    print("Setas: rotacionar")
    print("R: restaurar vista")
    print("ESC: fechar")

    # LOOP DE RENDERIZACAO
    while not glfw.window_should_close(janela):
        glfw.poll_events()

        if glfw.get_key(janela, glfw.KEY_RIGHT) == glfw.PRESS:
            rot_y += velocidade

        if glfw.get_key(janela, glfw.KEY_LEFT) == glfw.PRESS:
            rot_y -= velocidade

        if glfw.get_key(janela, glfw.KEY_DOWN) == glfw.PRESS:
            rot_x += velocidade

        if glfw.get_key(janela, glfw.KEY_UP) == glfw.PRESS:
            rot_x -= velocidade

        if glfw.get_key(janela, glfw.KEY_R) == glfw.PRESS:
            rot_x = 14.0
            rot_y = -36.0

        if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(janela, True)

        glClearColor(0.40, 0.70, 0.92, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader)

        matriz_model = (
            matriz_rotacao_x(rot_x) @
            matriz_rotacao_y(rot_y)
        )

        MVP = (
            matriz_proj @
            matriz_view @
            matriz_model
        )

        glUniformMatrix4fv(
            loc_mvp,
            1,
            GL_FALSE,
            np.ascontiguousarray(MVP.T, dtype=np.float32)
        )

        for VAO, VBO, EBO, indices, textura in objetos:
            desenhar_objeto(
                VAO,
                indices,
                textura,
                loc_tex
            )

        glfw.swap_buffers(janela)

    # LIMPEZA
    for VAO, VBO, EBO, indices, textura in objetos:
        glDeleteVertexArrays(1, [VAO])
        glDeleteBuffers(1, [VBO])
        glDeleteBuffers(1, [EBO])

    glDeleteTextures([textura_parede, textura_porta, textura_telhado, textura_grama, textura_janela])

    glDeleteProgram(shader)
    glfw.terminate()

if __name__ == "__main__":
    main()