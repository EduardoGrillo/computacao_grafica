import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import ctypes
import math

# SHADERS
VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
out vec3 Normal;
out float Altura;
uniform mat4 MVP;
uniform mat4 Modelo;
void main() {
    gl_Position = MVP * vec4(aPos, 1.0);
    Normal = normalize(mat3(Modelo) * aNormal);
    Altura = aPos.y;
    gl_PointSize = 5.0;
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec3 Normal;
in float Altura;
out vec4 FragColor;
uniform int modo_cor;
void main() {
    vec3 cor;
    if (modo_cor == 1) {
        if (length(gl_PointCoord - vec2(0.5)) > 0.5) discard;
        cor = vec3(1.0, 0.63, 0.22);
    } else if (modo_cor == 2) {
        cor = vec3(0.24, 0.90, 1.0);
    } else {
        vec3 luz = normalize(vec3(-0.45, 0.85, 0.70));
        float difusa = max(dot(normalize(Normal), luz), 0.0);
        float iluminacao = 0.30 + 0.70 * difusa;
        float mistura = clamp((Altura + 1.35) / 2.70, 0.0, 1.0);
        vec3 base = mix(vec3(0.04, 0.27, 0.55), vec3(0.10, 0.82, 0.72), mistura);
        cor = base * iluminacao;
    }
    FragColor = vec4(cor, 1.0);
}
"""

# MATRIZES - MESMO ESTILO DA CASA 3D
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
    return np.array([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]], dtype=np.float32)

def matriz_rotacao_x(graus):
    c, s = np.cos(np.radians(graus)), np.sin(np.radians(graus))
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]], dtype=np.float32)

def matriz_rotacao_y(graus):
    c, s = np.cos(np.radians(graus)), np.sin(np.radians(graus))
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]], dtype=np.float32)

# =========================================================
# ESFERA PARAMETRICA
# x = r * sen(phi) * cos(theta)
# y = r * cos(phi)
# z = r * sen(phi) * sen(theta)
# phi: 0 a pi | theta: 0 a 2*pi
# =========================================================
def criar_esfera(raio=1.35, paralelos=36, meridianos=54):
    vertices = [0.0, raio, 0.0, 0.0, 1.0, 0.0]  # Polo norte

    for i in range(1, paralelos):
        phi = math.pi * i / paralelos
        for j in range(meridianos):
            theta = 2.0 * math.pi * j / meridianos
            x = raio * math.sin(phi) * math.cos(theta)
            y = raio * math.cos(phi)
            z = raio * math.sin(phi) * math.sin(theta)
            vertices.extend([x, y, z, x / raio, y / raio, z / raio])

    sul = 1 + (paralelos - 1) * meridianos
    vertices.extend([0.0, -raio, 0.0, 0.0, -1.0, 0.0])  # Polo sul
    triangulos, linhas = [], []

    # Primeiro e ultimo anel conectados aos polos.
    for j in range(meridianos):
        proximo = (j + 1) % meridianos
        triangulos.extend([0, 1 + proximo, 1 + j])
        ultimo = 1 + (paralelos - 2) * meridianos
        triangulos.extend([ultimo + j, ultimo + proximo, sul])
        linhas.extend([0, 1 + j, ultimo + j, sul])

    # Malha entre os paralelos: triangulos para superficie e linhas para curvas.
    for i in range(paralelos - 1):
        inicio = 1 + i * meridianos
        for j in range(meridianos):
            atual = inicio + j
            seguinte = inicio + (j + 1) % meridianos
            linhas.extend([atual, seguinte])  # Curvas de latitude
            if i < paralelos - 2:
                abaixo = atual + meridianos
                abaixo_seguinte = seguinte + meridianos
                triangulos.extend([atual, seguinte, abaixo, seguinte, abaixo_seguinte, abaixo])
                linhas.extend([atual, abaixo])  # Curvas de longitude

    return (np.array(vertices, dtype=np.float32), np.array(triangulos, dtype=np.uint32),
            np.array(linhas, dtype=np.uint32))

# MEMORIA DA GPU - VAO, VBO E EBO
def criar_objeto_gpu(vertices, triangulos, linhas):
    VAO, VBO, EBO_triangulos, EBO_linhas = glGenVertexArrays(1), glGenBuffers(1), glGenBuffers(1), glGenBuffers(1)
    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_triangulos)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, triangulos.nbytes, triangulos, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_linhas)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, linhas.nbytes, linhas, GL_STATIC_DRAW)

    passo = 6 * vertices.itemsize
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, passo, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, passo, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)
    return VAO, VBO, EBO_triangulos, EBO_linhas

# DESENHO DA ESFERA
def desenhar_esfera(VAO, EBO_triangulos, EBO_linhas, total_vertices, total_triangulos, total_linhas, modo, loc_cor):
    glBindVertexArray(VAO)

    if modo in (3, 4):
        glUniform1i(loc_cor, 3)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_triangulos)
        if modo == 4:
            glEnable(GL_POLYGON_OFFSET_FILL)
            glPolygonOffset(1.0, 1.0)
        glDrawElements(GL_TRIANGLES, total_triangulos, GL_UNSIGNED_INT, None)
        glDisable(GL_POLYGON_OFFSET_FILL)

    if modo in (2, 4):
        glUniform1i(loc_cor, 2)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_linhas)
        glLineWidth(1.4)
        glDrawElements(GL_LINES, total_linhas, GL_UNSIGNED_INT, None)

    if modo == 1:
        glUniform1i(loc_cor, 1)
        glDrawArrays(GL_POINTS, 0, total_vertices)

    glBindVertexArray(0)

# PROGRAMA PRINCIPAL
def main():
    if not glfw.init():
        print("Nao foi possivel iniciar o GLFW.")
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.SAMPLES, 4)

    janela = glfw.create_window(900, 700, "Esfera 3D - Curvas Parametricas - CEFET-MG", None, None)
    if not janela:
        print("Nao foi possivel criar a janela OpenGL.")
        glfw.terminate()
        return

    glfw.make_context_current(janela)
    glfw.swap_interval(1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_PROGRAM_POINT_SIZE)
    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )

    vertices, triangulos, linhas = criar_esfera(raio=1.35, paralelos=36, meridianos=54)
    VAO, VBO, EBO_tri, EBO_lin = criar_objeto_gpu(vertices, triangulos, linhas)
    loc_mvp = glGetUniformLocation(shader, "MVP")
    loc_modelo = glGetUniformLocation(shader, "Modelo")
    loc_cor = glGetUniformLocation(shader, "modo_cor")
    matriz_view = matriz_translacao(0, 0, -4.8)

    rot_x, rot_y = 18.0, -28.0
    modo = 4  # 1: pontos | 2: linhas | 3: superficie | 4: superficie + linhas
    girar_automaticamente = False
    espaco_anterior = False
    tempo_anterior = glfw.get_time()

    print("=== ESFERA 3D - CURVAS PARAMETRICAS ===")
    print("1: pontos | 2: malha | 3: superficie | 4: superficie + malha")
    print("Setas: rotacionar | ESPACO: rotacao automatica | R: restaurar | ESC: sair")

    while not glfw.window_should_close(janela):
        glfw.poll_events()
        agora = glfw.get_time()
        delta = min(agora - tempo_anterior, 0.1)
        tempo_anterior = agora
        velocidade = 85.0 * delta

        if glfw.get_key(janela, glfw.KEY_RIGHT) == glfw.PRESS: rot_y += velocidade
        if glfw.get_key(janela, glfw.KEY_LEFT) == glfw.PRESS: rot_y -= velocidade
        if glfw.get_key(janela, glfw.KEY_DOWN) == glfw.PRESS: rot_x += velocidade
        if glfw.get_key(janela, glfw.KEY_UP) == glfw.PRESS: rot_x -= velocidade
        if glfw.get_key(janela, glfw.KEY_1) == glfw.PRESS: modo = 1
        if glfw.get_key(janela, glfw.KEY_2) == glfw.PRESS: modo = 2
        if glfw.get_key(janela, glfw.KEY_3) == glfw.PRESS: modo = 3
        if glfw.get_key(janela, glfw.KEY_4) == glfw.PRESS: modo = 4
        if glfw.get_key(janela, glfw.KEY_R) == glfw.PRESS: rot_x, rot_y = 18.0, -28.0
        if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS: glfw.set_window_should_close(janela, True)

        espaco_pressionado = glfw.get_key(janela, glfw.KEY_SPACE) == glfw.PRESS
        if espaco_pressionado and not espaco_anterior: girar_automaticamente = not girar_automaticamente
        espaco_anterior = espaco_pressionado
        if girar_automaticamente: rot_y += velocidade * 0.35

        largura, altura = glfw.get_framebuffer_size(janela)
        if largura == 0 or altura == 0: continue
        glViewport(0, 0, largura, altura)
        projecao = matriz_perspectiva(45.0, largura / altura, 0.1, 100.0)
        modelo = matriz_rotacao_x(rot_x) @ matriz_rotacao_y(rot_y)
        MVP = projecao @ matriz_view @ modelo

        glClearColor(0.045, 0.065, 0.115, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(shader)
        glUniformMatrix4fv(loc_mvp, 1, GL_FALSE, np.ascontiguousarray(MVP.T, dtype=np.float32))
        glUniformMatrix4fv(loc_modelo, 1, GL_FALSE, np.ascontiguousarray(modelo.T, dtype=np.float32))
        desenhar_esfera(VAO, EBO_tri, EBO_lin, len(vertices) // 6, len(triangulos), len(linhas), modo, loc_cor)
        glfw.swap_buffers(janela)

    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteBuffers(1, [EBO_tri])
    glDeleteBuffers(1, [EBO_lin])
    glDeleteProgram(shader)
    glfw.terminate()

if __name__ == "__main__":
    main()