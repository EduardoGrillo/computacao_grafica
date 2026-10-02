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
    """
    Recorta automaticamente o fundo muito claro de uma foto de porta.
    Se você trocar a porta por uma textura de madeira sem fundo branco,
    esta função deixa de ser necessária.
    """
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

    return imagem.crop(
        (x_min, y_min, x_max + 1, y_max + 1)
    )

def carregar_textura_do_disco(caminho_arquivo, recortar_porta=False):
    caminho_arquivo = os.path.normpath(caminho_arquivo)

    print("\nCarregando textura:")
    print(caminho_arquivo)

    if not os.path.exists(caminho_arquivo):
        print("ERRO: arquivo nao encontrado!")
        print("A textura rosa/preta sera usada apenas para indicar o erro.")

        largura, altura = 2, 2

        imagem_dados = np.array([
            255, 0, 255, 255,     0, 0, 0, 255,
            0, 0, 0, 255,         255, 0, 255, 255
        ], dtype=np.uint8).tobytes()

    else:
        imagem = Image.open(caminho_arquivo)

        if recortar_porta:
            imagem = recortar_fundo_claro(imagem)

        imagem = imagem.transpose(
            Image.FLIP_TOP_BOTTOM
        )

        imagem_dados = imagem.convert(
            "RGBA"
        ).tobytes()

        largura, altura = imagem.size

        print(
            f"OK: {largura}x{altura}"
        )

    textura_id = glGenTextures(1)

    glBindTexture(
        GL_TEXTURE_2D,
        textura_id
    )

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_MIN_FILTER,
        GL_LINEAR_MIPMAP_LINEAR
    )

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_MAG_FILTER,
        GL_LINEAR
    )

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_WRAP_S,
        GL_REPEAT
    )

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_WRAP_T,
        GL_REPEAT
    )

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

    glGenerateMipmap(
        GL_TEXTURE_2D
    )

    glBindTexture(
        GL_TEXTURE_2D,
        0
    )

    return textura_id

# MATRIZES
def matriz_perspectiva(fov, aspecto, perto, longe):
    f = 1.0 / np.tan(
        np.radians(fov) / 2.0
    )

    m = np.zeros(
        (4, 4),
        dtype=np.float32
    )

    m[0, 0] = f / aspecto
    m[1, 1] = f

    m[2, 2] = (
        (longe + perto) /
        (perto - longe)
    )

    m[2, 3] = (
        (2.0 * longe * perto) /
        (perto - longe)
    )

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

# GEOMETRIA DA CASA
def criar_corpo_casa():
    """
    Corpo retangular da casa.
    X, Y, Z, U, V
    """

    vertices = np.array([
        # Frente
        -1.10, -1.25,  1.00,   0.0, 0.0,
         1.10, -1.25,  1.00,   3.0, 0.0,
         1.10,  1.00,  1.00,   3.0, 3.0,
        -1.10,  1.00,  1.00,   0.0, 3.0,

        # Traseira
         1.10, -1.25, -1.00,   0.0, 0.0,
        -1.10, -1.25, -1.00,   3.0, 0.0,
        -1.10,  1.00, -1.00,   3.0, 3.0,
         1.10,  1.00, -1.00,   0.0, 3.0,

        # Esquerda
        -1.10, -1.25, -1.00,   0.0, 0.0,
        -1.10, -1.25,  1.00,   3.0, 0.0,
        -1.10,  1.00,  1.00,   3.0, 3.0,
        -1.10,  1.00, -1.00,   0.0, 3.0,

        # Direita
         1.10, -1.25,  1.00,   0.0, 0.0,
         1.10, -1.25, -1.00,   3.0, 0.0,
         1.10,  1.00, -1.00,   3.0, 3.0,
         1.10,  1.00,  1.00,   0.0, 3.0,

        # Superior
        -1.10,  1.00,  1.00,   0.0, 0.0,
         1.10,  1.00,  1.00,   2.0, 0.0,
         1.10,  1.00, -1.00,   2.0, 2.0,
        -1.10,  1.00, -1.00,   0.0, 2.0,

        # Inferior
        -1.10, -1.25, -1.00,   0.0, 0.0,
         1.10, -1.25, -1.00,   2.0, 0.0,
         1.10, -1.25,  1.00,   2.0, 2.0,
        -1.10, -1.25,  1.00,   0.0, 2.0
    ], dtype=np.float32)

    indices = np.array([
         0,  1,  2,   2,  3,  0,
         4,  5,  6,   6,  7,  4,
         8,  9, 10,  10, 11,  8,
        12, 13, 14,  14, 15, 12,
        16, 17, 18,  18, 19, 16,
        20, 21, 22,  22, 23, 20
    ], dtype=np.uint32)

    return vertices, indices

def criar_telhado():
    """
    Telhado piramidal mais baixo e proporcional,
    mais próximo do exemplo mostrado em aula.

    Cada lateral possui seus próprios vértices,
    permitindo mapear a textura de telha
    de forma independente.
    """

    y_base = 0.98
    y_topo = 1.82

    x_base = 1.30
    z_base = 1.18

    vertices = np.array([
        # Frente
        -x_base, y_base,  z_base,   0.0, 0.0,
         x_base, y_base,  z_base,   3.0, 0.0,
         0.0,    y_topo,  0.0,      1.5, 2.5,

        # Direita
         x_base, y_base,  z_base,   0.0, 0.0,
         x_base, y_base, -z_base,   3.0, 0.0,
         0.0,    y_topo,  0.0,      1.5, 2.5,

        # Traseira
         x_base, y_base, -z_base,   0.0, 0.0,
        -x_base, y_base, -z_base,   3.0, 0.0,
         0.0,    y_topo,  0.0,      1.5, 2.5,

        # Esquerda
        -x_base, y_base, -z_base,   0.0, 0.0,
        -x_base, y_base,  z_base,   3.0, 0.0,
         0.0,    y_topo,  0.0,      1.5, 2.5
    ], dtype=np.float32)

    indices = np.array([
         0,  1,  2,
         3,  4,  5,
         6,  7,  8,
         9, 10, 11
    ], dtype=np.uint32)

    return vertices, indices

def criar_porta():
    """
    Porta como um pequeno prisma muito fino.
    Assim ela deixa de parecer apenas uma imagem
    colada na parede.

    A face frontal recebe a textura.
    """

    esquerda = -0.34
    direita = 0.34

    baixo = -1.24
    cima = 0.28

    z_frente = 1.035
    z_tras = 1.005

    vertices = np.array([
        # Face frontal
        esquerda, baixo, z_frente,   0.0, 0.0,
        direita,  baixo, z_frente,   1.0, 0.0,
        direita,  cima,  z_frente,   1.0, 1.0,
        esquerda, cima,  z_frente,   0.0, 1.0,

        # Face traseira
        direita,  baixo, z_tras,     0.0, 0.0,
        esquerda, baixo, z_tras,     1.0, 0.0,
        esquerda, cima,  z_tras,     1.0, 1.0,
        direita,  cima,  z_tras,     0.0, 1.0,

        # Esquerda
        esquerda, baixo, z_tras,     0.0, 0.0,
        esquerda, baixo, z_frente,   1.0, 0.0,
        esquerda, cima,  z_frente,   1.0, 1.0,
        esquerda, cima,  z_tras,     0.0, 1.0,

        # Direita
        direita, baixo, z_frente,    0.0, 0.0,
        direita, baixo, z_tras,      1.0, 0.0,
        direita, cima,  z_tras,      1.0, 1.0,
        direita, cima,  z_frente,    0.0, 1.0
    ], dtype=np.float32)

    indices = np.array([
         0,  1,  2,   2,  3,  0,
         4,  5,  6,   6,  7,  4,
         8,  9, 10,  10, 11,  8,
        12, 13, 14,  14, 15, 12
    ], dtype=np.uint32)

    return vertices, indices

# GPU
def criar_objeto_gpu(vertices, indices):
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(
        VAO
    )

    glBindBuffer(
        GL_ARRAY_BUFFER,
        VBO
    )

    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes,
        vertices,
        GL_STATIC_DRAW
    )

    glBindBuffer(
        GL_ELEMENT_ARRAY_BUFFER,
        EBO
    )

    glBufferData(
        GL_ELEMENT_ARRAY_BUFFER,
        indices.nbytes,
        indices,
        GL_STATIC_DRAW
    )

    passo = 5 * vertices.itemsize

    glVertexAttribPointer(
        0,
        3,
        GL_FLOAT,
        GL_FALSE,
        passo,
        ctypes.c_void_p(0)
    )

    glEnableVertexAttribArray(
        0
    )

    glVertexAttribPointer(
        1,
        2,
        GL_FLOAT,
        GL_FALSE,
        passo,
        ctypes.c_void_p(
            3 * vertices.itemsize
        )
    )

    glEnableVertexAttribArray(
        1
    )

    glBindVertexArray(
        0
    )

    return VAO, VBO, EBO

def desenhar_objeto(
    VAO,
    indices,
    textura_id,
    loc_tex
):
    glActiveTexture(
        GL_TEXTURE0
    )

    glBindTexture(
        GL_TEXTURE_2D,
        textura_id
    )

    glUniform1i(
        loc_tex,
        0
    )

    glBindVertexArray(
        VAO
    )

    glDrawElements(
        GL_TRIANGLES,
        len(indices),
        GL_UNSIGNED_INT,
        None
    )

    glBindVertexArray(
        0
    )

def main():
    if not glfw.init():
        return

    glfw.window_hint(
        glfw.CONTEXT_VERSION_MAJOR,
        3
    )

    glfw.window_hint(
        glfw.CONTEXT_VERSION_MINOR,
        3
    )

    glfw.window_hint(
        glfw.OPENGL_PROFILE,
        glfw.OPENGL_CORE_PROFILE
    )

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

    glfw.make_context_current(
        janela
    )

    glfw.swap_interval(
        1
    )

    glEnable(
        GL_DEPTH_TEST
    )

    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(
            VERTEX_SHADER,
            GL_VERTEX_SHADER
        ),
        OpenGL.GL.shaders.compileShader(
            FRAGMENT_SHADER,
            GL_FRAGMENT_SHADER
        )
    )

    # CAMINHOS
    pasta_atual = os.path.dirname(
        os.path.abspath(__file__)
    )

    caminho_parede = os.path.join(
        pasta_atual,
        "texturas",
        "parede.jpg"
    )

    caminho_porta = os.path.join(
        pasta_atual,
        "texturas",
        "porta.jpg"
    )

    caminho_telhado = os.path.join(
        pasta_atual,
        "texturas",
        "telhado.jpg"
    )

    # TEXTURAS
    textura_parede = carregar_textura_do_disco(
        caminho_parede
    )

    textura_porta = carregar_textura_do_disco(
        caminho_porta,
        recortar_porta=True
    )

    textura_telhado = carregar_textura_do_disco(
        caminho_telhado
    )

    # OBJETOS
    vertices_corpo, indices_corpo = criar_corpo_casa()
    vertices_telhado, indices_telhado = criar_telhado()
    vertices_porta, indices_porta = criar_porta()

    VAO_corpo, VBO_corpo, EBO_corpo = criar_objeto_gpu(
        vertices_corpo,
        indices_corpo
    )

    VAO_telhado, VBO_telhado, EBO_telhado = criar_objeto_gpu(
        vertices_telhado,
        indices_telhado
    )

    VAO_porta, VBO_porta, EBO_porta = criar_objeto_gpu(
        vertices_porta,
        indices_porta
    )

    # MATRIZES BASE
    matriz_proj = matriz_perspectiva(
        45.0,
        largura_janela / altura_janela,
        0.1,
        100.0
    )

    matriz_view = matriz_translacao(
        0,
        -0.20,
        -6.7
    )

    loc_mvp = glGetUniformLocation(
        shader,
        "MVP"
    )

    loc_tex = glGetUniformLocation(
        shader,
        "textura_bloco"
    )

    # Vista inicial em perspectiva
    rot_x = 10.0
    rot_y = -28.0

    velocidade = 2.0

    print("\n=== CASA 3D ===")
    print("Setas: rotacionar")
    print("R: restaurar vista")
    print("ESC: fechar")

    # LOOP
    while not glfw.window_should_close(janela):
        glfw.poll_events()

        if glfw.get_key(
            janela,
            glfw.KEY_RIGHT
        ) == glfw.PRESS:
            rot_y += velocidade

        if glfw.get_key(
            janela,
            glfw.KEY_LEFT
        ) == glfw.PRESS:
            rot_y -= velocidade

        if glfw.get_key(
            janela,
            glfw.KEY_DOWN
        ) == glfw.PRESS:
            rot_x += velocidade

        if glfw.get_key(
            janela,
            glfw.KEY_UP
        ) == glfw.PRESS:
            rot_x -= velocidade

        if glfw.get_key(
            janela,
            glfw.KEY_R
        ) == glfw.PRESS:
            rot_x = 10.0
            rot_y = -28.0

        if glfw.get_key(
            janela,
            glfw.KEY_ESCAPE
        ) == glfw.PRESS:
            glfw.set_window_should_close(
                janela,
                True
            )

        glClearColor(
            0.40,
            0.70,
            0.92,
            1.0
        )

        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        glUseProgram(
            shader
        )

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
            np.ascontiguousarray(
                MVP.T,
                dtype=np.float32
            )
        )

        desenhar_objeto(
            VAO_corpo,
            indices_corpo,
            textura_parede,
            loc_tex
        )

        desenhar_objeto(
            VAO_telhado,
            indices_telhado,
            textura_telhado,
            loc_tex
        )

        desenhar_objeto(
            VAO_porta,
            indices_porta,
            textura_porta,
            loc_tex
        )

        glfw.swap_buffers(
            janela
        )

    glfw.terminate()

if __name__ == "__main__":
    main()