import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import ctypes

# SHADERS
VERTEX_SHADER = """
#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

out vec3 vertexColor;

uniform mat4 MVP;

void main()
{
    gl_Position = MVP * vec4(aPos, 1.0);
    vertexColor = aColor;
}
"""


FRAGMENT_SHADER = """
#version 330 core

in vec3 vertexColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(vertexColor, 1.0);
}
"""


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


# CRIAÇÃO DOS OBJETOS
def criar_piramide():
    # Cada vértice possui:
    # X, Y, Z, R, G, B

    vertices = np.array([
        # Base
        -0.8, -0.8,  0.8,   0.2, 0.5, 1.0,
         0.8, -0.8,  0.8,   0.2, 0.5, 1.0,
         0.8, -0.8, -0.8,   0.1, 0.3, 0.8,
        -0.8, -0.8, -0.8,   0.1, 0.3, 0.8,

        # Topo
         0.0,  1.0,  0.0,   1.0, 0.4, 0.1
    ], dtype=np.float32)

    # Base = 2 triângulos
    # Laterais = 4 triângulos
    indices = np.array([
        0, 1, 2,
        2, 3, 0,

        0, 1, 4,
        1, 2, 4,
        2, 3, 4,
        3, 0, 4
    ], dtype=np.uint32)

    return vertices, indices


def criar_prisma():
    # Prisma retangular
    # Cada vértice possui:
    # X, Y, Z, R, G, B

    vertices = np.array([
        # Frente
        -0.8, -0.8,  0.5,   0.1, 0.8, 0.4,
         0.8, -0.8,  0.5,   0.1, 0.8, 0.4,
         0.8,  0.8,  0.5,   0.2, 1.0, 0.5,
        -0.8,  0.8,  0.5,   0.2, 1.0, 0.5,

        # Trás
        -0.8, -0.8, -0.5,   0.0, 0.4, 0.2,
         0.8, -0.8, -0.5,   0.0, 0.4, 0.2,
         0.8,  0.8, -0.5,   0.0, 0.6, 0.3,
        -0.8,  0.8, -0.5,   0.0, 0.6, 0.3
    ], dtype=np.float32)

    # 6 faces, cada uma formada por 2 triângulos
    indices = np.array([
        0, 1, 2,  2, 3, 0,   # Frente
        4, 5, 6,  6, 7, 4,   # Trás
        0, 4, 7,  7, 3, 0,   # Esquerda
        1, 5, 6,  6, 2, 1,   # Direita
        3, 2, 6,  6, 7, 3,   # Superior
        0, 1, 5,  5, 4, 0    # Inferior
    ], dtype=np.uint32)

    return vertices, indices


# ENVIA OBJETO PARA A GPU
def criar_buffers(vertices, indices):
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes,
        vertices,
        GL_STATIC_DRAW
    )

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(
        GL_ELEMENT_ARRAY_BUFFER,
        indices.nbytes,
        indices,
        GL_STATIC_DRAW
    )

    passo = 6 * vertices.itemsize

    glVertexAttribPointer(
        0,
        3,
        GL_FLOAT,
        GL_FALSE,
        passo,
        ctypes.c_void_p(0)
    )
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(
        1,
        3,
        GL_FLOAT,
        GL_FALSE,
        passo,
        ctypes.c_void_p(3 * vertices.itemsize)
    )
    glEnableVertexAttribArray(1)

    glBindVertexArray(0)

    return VAO, VBO, EBO


# PROGRAMA PRINCIPAL
def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(
        glfw.OPENGL_PROFILE,
        glfw.OPENGL_CORE_PROFILE
    )

    janela = glfw.create_window(
        900,
        650,
        "Pirâmide e Prisma 3D - Use as SETAS do Teclado",
        None,
        None
    )

    if not janela:
        glfw.terminate()
        return

    glfw.make_context_current(janela)

    # VSync
    glfw.swap_interval(1)

    # Z-Buffer
    glEnable(GL_DEPTH_TEST)

    # Compila os shaders
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

    # CRIAÇÃO DA PIRÂMIDE
    vertices_piramide, indices_piramide = criar_piramide()

    VAO_piramide, VBO_piramide, EBO_piramide = criar_buffers(
        vertices_piramide,
        indices_piramide
    )

    # CRIAÇÃO DO PRISMA
    vertices_prisma, indices_prisma = criar_prisma()

    VAO_prisma, VBO_prisma, EBO_prisma = criar_buffers(
        vertices_prisma,
        indices_prisma
    )

    # MATRIZES BASE
    largura = 900
    altura = 650

    projecao = matriz_perspectiva(
        45.0,
        largura / altura,
        0.1,
        100.0
    )

    view = matriz_translacao(
        0,
        0,
        -7.0
    )

    loc_mvp = glGetUniformLocation(
        shader,
        "MVP"
    )

    # Estado inicial da rotação
    rot_x = 20.0
    rot_y = 30.0

    velocidade = 2.0

    print("=== Pirâmide e Prisma 3D ===")
    print("Use as SETAS do teclado para rotacionar os objetos.")

    # GAME LOOP
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

        if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(janela, True)

        # Limpeza do frame
        glClearColor(
            0.82,
            0.90,
            1.0,
            1.0
        )

        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        glUseProgram(shader)

        # Rotação compartilhada
        rotacao = (
            matriz_rotacao_x(rot_x) @
            matriz_rotacao_y(rot_y)
        )

        # DESENHA A PIRÂMIDE À ESQUERDA
        modelo_piramide = (
            matriz_translacao(-1.7, 0, 0) @
            rotacao
        )

        MVP_piramide = (
            projecao @
            view @
            modelo_piramide
        )

        glUniformMatrix4fv(
            loc_mvp,
            1,
            GL_TRUE,
            np.ascontiguousarray(
                MVP_piramide,
                dtype=np.float32
            )
        )

        glBindVertexArray(VAO_piramide)

        glDrawElements(
            GL_TRIANGLES,
            len(indices_piramide),
            GL_UNSIGNED_INT,
            None
        )

        # DESENHA O PRISMA À DIREITA
        modelo_prisma = (
            matriz_translacao(1.7, 0, 0) @
            rotacao
        )

        MVP_prisma = (
            projecao @
            view @
            modelo_prisma
        )

        glUniformMatrix4fv(
            loc_mvp,
            1,
            GL_TRUE,
            np.ascontiguousarray(
                MVP_prisma,
                dtype=np.float32
            )
        )

        glBindVertexArray(VAO_prisma)

        glDrawElements(
            GL_TRIANGLES,
            len(indices_prisma),
            GL_UNSIGNED_INT,
            None
        )

        glBindVertexArray(0)

        glfw.swap_buffers(janela)

    # LIMPEZA
    glDeleteVertexArrays(1, [VAO_piramide])
    glDeleteBuffers(1, [VBO_piramide])
    glDeleteBuffers(1, [EBO_piramide])

    glDeleteVertexArrays(1, [VAO_prisma])
    glDeleteBuffers(1, [VBO_prisma])
    glDeleteBuffers(1, [EBO_prisma])

    glDeleteProgram(shader)

    glfw.terminate()


if __name__ == "__main__":
    main()