import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import math
import random
import os

LARGURA, ALTURA = 1100, 720

# FUNÇÕES AUXILIARES
def limitar(n, minimo=0.0, maximo=1.0):
    return max(minimo, min(maximo, n))

def misturar(a, b, t):
    t = limitar(t)
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))

def cor(rgb, alpha=1.0):
    glColor4f(*rgb, alpha)

def vertice(p):
    glVertex3f(*p)

def disco_2d(x, y, raio, color, alpha=1.0, segmentos=52):
    glColor4f(*color, alpha)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(segmentos + 1):
        t = 2 * math.pi * i / segmentos
        glVertex2f(x + raio * math.cos(t), y + raio * math.sin(t))
    glEnd()

# CÉU COM DEGRADÊ E SOL (FUNDO 2D DA CENA 3D)
def desenhar_ceu():
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_FOG)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    cores = [(-1.0, (0.31, 0.59, 0.83)), (-0.10, (0.66, 0.81, 0.87)),
             (0.05, (0.98, 0.91, 0.71)), (0.40, (0.83, 0.89, 0.87)),
             (1.0, (0.39, 0.68, 0.89))]
    glBegin(GL_QUADS)
    for (y1, c1), (y2, c2) in zip(cores, cores[1:]):
        cor(c1); glVertex2f(-1, y1); glVertex2f(1, y1)
        cor(c2); glVertex2f(1, y2); glVertex2f(-1, y2)
    glEnd()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    for raio, opacidade in [(0.55, 0.013), (0.40, 0.018), (0.31, 0.023), (0.22, 0.035), (0.15, 0.052), (0.10, 0.065)]:
        disco_2d(0.03, 0.07, raio, (1.0, 0.78, 0.33), opacidade)
    disco_2d(0.03, 0.07, 0.060, (1.0, 0.94, 0.73), 0.18)
    disco_2d(0.03, 0.07, 0.030, (1.0, 1.0, 0.90), 0.48)
    glDisable(GL_BLEND)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_FOG)

# TERRENO DOURADO, GRAMA E SOMBRAS
def desenhar_colinas_distantes():
    rng = random.Random(21)
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(81):
        x = -90 + i * 2.25
        altura = 0.48 + 0.22 * math.sin(i * 0.29) + 0.11 * math.cos(i * 0.57) + rng.uniform(-0.07, 0.07)
        cor((0.58, 0.56, 0.31)); glVertex3f(x, -0.30, -67)
        cor((0.70, 0.67, 0.44)); glVertex3f(x, altura, -67)
    glEnd()

def desenhar_campo():
    rng = random.Random(8)
    # Faixas pequenas com cores variadas dão textura visual sem usar imagens externas.
    glBegin(GL_QUADS)
    for iz in range(125):
        z = -70 + iz * 0.72
        for ix in range(96):
            x = -38 + ix * 0.80
            perto = limitar((z + 70) / 90)
            iluminacao = math.exp(-((x - 1) / 17) ** 2) * (1 - perto) * 0.25
            base = misturar((0.78, 0.65, 0.28), (0.35, 0.34, 0.13), perto * 0.80)
            ruido = rng.uniform(-0.10, 0.10)
            c = tuple(limitar(v + ruido + iluminacao * k) for v, k in zip(base, (0.70, 0.62, 0.04)))
            cor(c)
            glVertex3f(x, 0, z); glVertex3f(x + 0.80, 0, z)
            glVertex3f(x + 0.80, 0, z + 0.72); glVertex3f(x, 0, z + 0.72)
    glEnd()
    # Talos curtos, também em 3D (mais visíveis próximos da câmera).
    glLineWidth(1.0)
    glBegin(GL_LINES)
    for _ in range(13000):
        x, z = rng.uniform(-36, 36), rng.uniform(-60, 17)
        h = rng.uniform(0.035, 0.15) * (0.7 if z < -25 else 1)
        t = rng.uniform(-0.055, 0.055)
        c = rng.choice([(0.69, 0.59, 0.25), (0.31, 0.39, 0.13), (0.85, 0.71, 0.29), (0.56, 0.51, 0.16)])
        cor(c, 0.80); glVertex3f(x, 0.018, z); glVertex3f(x + t, h, z + t)
    glEnd()

def desenhar_sombra_arvore(x, z, altura):
    # Sol ao fundo: a sombra avança para a câmera, diagonalmente à esquerda.
    fim_x, fim_z = x - altura * 1.18, z + altura * 3.15
    glColor4f(0.13, 0.12, 0.06, 0.42)
    glBegin(GL_QUADS)
    glVertex3f(x - 0.24, 0.042, z); glVertex3f(x + 0.24, 0.042, z)
    glVertex3f(fim_x + 0.46, 0.042, fim_z); glVertex3f(fim_x - 0.46, 0.042, fim_z)
    glEnd()
    glLineWidth(1.6)
    glBegin(GL_LINES)
    for desvio in (-0.65, 0.15, 0.75):
        glVertex3f(x, 0.046, z)
        glVertex3f(fim_x + desvio * altura * 0.35, 0.046, fim_z * 0.90 + z * 0.10)
    glEnd()

# ÁRVORES SECAS: TRONCOS CILÍNDRICOS E RAMOS RECURSIVOS
def cilindro_entre(a, b, raio_a, raio_b, cor_base, faces=7):
    d = [b[i] - a[i] for i in range(3)]
    modulo = math.sqrt(sum(v * v for v in d))
    if modulo < 0.00001:
        return
    d = [v / modulo for v in d]
    referencia = (0, 0, 1) if abs(d[2]) < 0.82 else (1, 0, 0)
    u = (d[1] * referencia[2] - d[2] * referencia[1], d[2] * referencia[0] - d[0] * referencia[2], d[0] * referencia[1] - d[1] * referencia[0])
    norma_u = math.sqrt(sum(v * v for v in u))
    u = [v / norma_u for v in u]
    v = (d[1] * u[2] - d[2] * u[1], d[2] * u[0] - d[0] * u[2], d[0] * u[1] - d[1] * u[0])
    glBegin(GL_QUAD_STRIP)
    for i in range(faces + 1):
        t = i * 2 * math.pi / faces
        direcao = [math.cos(t) * u[k] + math.sin(t) * v[k] for k in range(3)]
        tom = 0.80 + 0.18 * math.cos(t)
        glColor3f(*(c * tom for c in cor_base))
        vertice(tuple(a[k] + raio_a * direcao[k] for k in range(3)))
        vertice(tuple(b[k] + raio_b * direcao[k] for k in range(3)))
    glEnd()

def desenhar_ramos(inicio, fim, raio, nivel, rng):
    if nivel <= 1:
        glColor3f(0.19, 0.15, 0.10)
        glBegin(GL_LINES); vertice(inicio); vertice(fim); glEnd()
    else:
        cilindro_entre(inicio, fim, raio, raio * 0.60, (0.28, 0.23, 0.17), 6)
    if nivel <= 0:
        return
    direcao = [fim[k] - inicio[k] for k in range(3)]
    for sinal in (-1, 1):
        novo = (fim[0] + direcao[0] * 0.45 + sinal * rng.uniform(0.25, 0.54),
                fim[1] + direcao[1] * rng.uniform(0.57, 0.76),
                fim[2] + direcao[2] * 0.42 + rng.uniform(-0.28, 0.28))
        desenhar_ramos(fim, novo, raio * 0.59, nivel - 1, rng)
    if nivel == 4:
        novo = (fim[0] + rng.uniform(-0.20, 0.20), fim[1] + 0.88, fim[2] + rng.uniform(-0.25, 0.25))
        desenhar_ramos(fim, novo, raio * 0.48, nivel - 1, rng)

def desenhar_arvore(x, z, altura, semente):
    rng = random.Random(semente)
    glPushMatrix()
    glTranslatef(x, 0, z)
    glScalef(altura / 4.2, altura / 4.2, altura / 4.2)
    cilindro_entre((0, 0, 0), (0, 1.22, 0), 0.16, 0.105, (0.30, 0.24, 0.17), 8)
    desenhar_ramos((0, 1.22, 0), (0.08, 2.02, 0.02), 0.094, 4, rng)
    desenhar_ramos((0, 0.87, 0), (-0.68, 1.63, 0.12), 0.07, 3, rng)
    desenhar_ramos((0, 1.02, 0), (0.64, 1.75, -0.10), 0.065, 3, rng)
    glPopMatrix()

# CASA 3D: PAREDES, TELHADO, PORTA, JANELAS E CHAMINÉ
def bloco(x1, x2, y1, y2, z1, z2, c):
    glBegin(GL_QUADS)
    cor(misturar(c, (1, 1, 1), 0.08))
    for p in [(x1,y1,z2),(x2,y1,z2),(x2,y2,z2),(x1,y2,z2)]: vertice(p)
    cor(misturar(c, (0, 0, 0), 0.12))
    for p in [(x2,y1,z1),(x1,y1,z1),(x1,y2,z1),(x2,y2,z1)]: vertice(p)
    cor(misturar(c, (0, 0, 0), 0.07))
    for p in [(x1,y1,z1),(x1,y1,z2),(x1,y2,z2),(x1,y2,z1)]: vertice(p)
    cor(misturar(c, (0, 0, 0), 0.20))
    for p in [(x2,y1,z2),(x2,y1,z1),(x2,y2,z1),(x2,y2,z2)]: vertice(p)
    cor(misturar(c, (1, 1, 1), 0.18))
    for p in [(x1,y2,z2),(x2,y2,z2),(x2,y2,z1),(x1,y2,z1)]: vertice(p)
    cor(c)
    for p in [(x1,y1,z1),(x2,y1,z1),(x2,y1,z2),(x1,y1,z2)]: vertice(p)
    glEnd()

def desenhar_janela(x, y, z):
    bloco(x-0.43, x+0.43, y-0.52, y+0.52, z, z+0.07, (0.23, 0.20, 0.17))
    bloco(x-0.33, x+0.33, y-0.42, y+0.42, z+0.07, z+0.09, (0.43, 0.50, 0.47))
    bloco(x-0.035, x+0.035, y-0.45, y+0.45, z+0.09, z+0.12, (0.25, 0.22, 0.20))
    bloco(x-0.35, x+0.35, y-0.035, y+0.035, z+0.09, z+0.12, (0.25, 0.22, 0.20))

def desenhar_casa():
    glPushMatrix()
    glTranslatef(16.5, 0, -24.0)
    glRotatef(-16, 0, 1, 0)
    # Paredes envelhecidas, com diferenças sutis entre os lados.
    bloco(-3.0, 3.0, 0, 4.50, -2.90, 2.90, (0.67, 0.63, 0.56))
    # Linhas sutis sugerindo pedras e reboco, sem arquivos de textura.
    glLineWidth(1.0)
    glColor3f(0.61, 0.56, 0.49)
    glBegin(GL_LINES)
    for j in range(1, 9):
        y = j * 0.48
        for zz in (2.91, -2.91): glVertex3f(-3, y, zz); glVertex3f(3, y, zz)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.68, 0.63, 0.54)
    for p in [(-3,4.5,2.9),(3,4.5,2.9),(0,6.5,2.9)]: vertice(p)
    glColor3f(0.57, 0.53, 0.47)
    for p in [(3,4.5,-2.9),(-3,4.5,-2.9),(0,6.5,-2.9)]: vertice(p)
    glEnd()

    # Dois planos inclinados formam o telhado de duas águas.
    glBegin(GL_QUADS)
    glColor3f(0.45, 0.23, 0.17)
    for p in [(-3.48,4.44,3.36),(0,6.66,3.36),(0,6.66,-3.36),(-3.48,4.44,-3.36)]: vertice(p)
    glColor3f(0.53, 0.29, 0.21)
    for p in [(0,6.66,3.36),(3.48,4.44,3.36),(3.48,4.44,-3.36),(0,6.66,-3.36)]: vertice(p)
    glEnd()
    
    # Telhas: linhas de fiadas sobre as faces inclinadas.
    glLineWidth(1.0)
    glColor3f(0.30, 0.15, 0.12)
    glBegin(GL_LINES)
    for i in range(1, 13):
        t = i / 13
        for lado in (-1, 1):
            x, y = lado * (3.48 * (1-t)), 4.44 + 2.22*t + 0.008
            glVertex3f(x, y, -3.37); glVertex3f(x, y, 3.37)
    
    for k in range(10):
        z = -3.1 + k * 0.69
        for lado in (-1, 1):
            glVertex3f(lado * 3.49, 4.46, z); glVertex3f(0, 6.68, z)
    glEnd()
    
    # Porta frontal com batentes, duas janelas e chaminé.
    bloco(-0.65, 0.70, 0.03, 2.60, 2.92, 3.00, (0.20, 0.16, 0.13))
    bloco(-0.72, -0.60, 0, 2.75, 3.00, 3.13, (0.35, 0.27, 0.21))
    bloco(0.65, 0.78, 0, 2.75, 3.00, 3.13, (0.35, 0.27, 0.21))
    bloco(-0.72, 0.78, 2.61, 2.76, 3.00, 3.13, (0.35, 0.27, 0.21))
    bloco(0.45, 0.52, 1.22, 1.30, 3.01, 3.08, (0.84, 0.72, 0.41))
    
    desenhar_janela(-2.05, 2.60, 2.94)
    desenhar_janela(2.05, 2.60, 2.94)
    
    bloco(1.65, 2.35, 5.10, 7.65, -1.65, -1.00, (0.48, 0.37, 0.30))
    bloco(1.55, 2.45, 7.60, 7.85, -1.75, -0.90, (0.33, 0.29, 0.26))
    
    # Degrau de pedra em frente à porta.
    bloco(-0.94, 1.00, -0.08, 0.14, 2.87, 3.80, (0.52, 0.50, 0.43))
    glPopMatrix()

def desenhar_sombra_casa():
    glColor4f(0.18, 0.14, 0.07, 0.25)
    glBegin(GL_QUADS)
    
    for p in [(13,0.045,-20),(20,0.045,-20),(7.0,0.045,9),(1.0,0.045,9)]: vertice(p)
   
    glEnd()

# MONTAGEM DO CENÁRIO (DISPLAY LIST: GEOMETRIA ESTÁTICA)
def construir_cenario():
    lista = glGenLists(1)
    glNewList(lista, GL_COMPILE)
    desenhar_colinas_distantes()
    desenhar_campo()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    arvores = [(-10.5,1.0,7.3,12),(-12.2,-8,5.8,24),(-9.0,-17,5.7,36),
               (-7.6,-25,5.2,43),(-5.0,-34,4.5,56),(-2.1,-41,4.0,66),
               (1.6,-43,4.4,76),(4.6,-34,5.6,84),(8.0,-42,4.6,91),
               (9.4,-26,5.4,95),(23.5,-32,7.2,101),(-24,-28,9.0,115)]
    for x, z, h, seed in arvores:
        desenhar_sombra_arvore(x, z, h)
    desenhar_sombra_casa()
    glDisable(GL_BLEND)
    
    for x, z, h, seed in sorted(arvores, key=lambda p: p[1]):
        desenhar_arvore(x, z, h, seed)
    
    desenhar_casa()
    glEndList()
    
    return lista

# TELA, TECLADO E PROJEÇÃO
def salvar_imagem(janela):
    try:
        from PIL import Image
        largura, altura = glfw.get_framebuffer_size(janela)
        dados = glReadPixels(0, 0, largura, altura, GL_RGB, GL_UNSIGNED_BYTE)
        imagem = Image.frombytes('RGB', (largura, altura), dados)
        imagem = imagem.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paisagem_resultado.png')
        imagem.save(caminho)
        print(f'Imagem salva em: {caminho}')
    
    except Exception as erro:
        print(f'Não foi possível salvar a imagem: {erro}')

def main():
    if not glfw.init():
        print('Erro ao iniciar o GLFW.'); return
    # O modo clássico é necessário porque o professor utiliza glBegin/glEnd.
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    
    janela = glfw.create_window(LARGURA, ALTURA, 'Paisagem 3D - OpenGL | CEFET-MG', None, None)
    
    if not janela:
        glfw.terminate(); raise RuntimeError('Não foi possível criar a janela OpenGL.')
    
    glfw.make_context_current(janela)
    glfw.swap_interval(1)
    
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glDisable(GL_CULL_FACE)
    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogfv(GL_FOG_COLOR, (0.84, 0.79, 0.62, 1.0))
    glFogf(GL_FOG_START, 32.0)
    glFogf(GL_FOG_END, 100.0)
    glLineWidth(1.2)
    
    print('Paisagem 3D: setas = mover a visão | R = restaurar | P = salvar PNG | ESC = sair')
    
    cenario = construir_cenario()
    azimute, inclinacao = 0.0, -4.0
    tecla_p_anterior = False
    tempo_anterior = glfw.get_time()
    while not glfw.window_should_close(janela):
        glfw.poll_events()
        tempo = glfw.get_time()
        delta = min(tempo - tempo_anterior, 0.06)
        tempo_anterior = tempo
        velocidade = 31 * delta
        
        if glfw.get_key(janela, glfw.KEY_LEFT) == glfw.PRESS: azimute -= velocidade
        if glfw.get_key(janela, glfw.KEY_RIGHT) == glfw.PRESS: azimute += velocidade
        if glfw.get_key(janela, glfw.KEY_UP) == glfw.PRESS: inclinacao = limitar(inclinacao + velocidade, -25, 25)
        if glfw.get_key(janela, glfw.KEY_DOWN) == glfw.PRESS: inclinacao = limitar(inclinacao - velocidade, -25, 25)
        if glfw.get_key(janela, glfw.KEY_R) == glfw.PRESS: azimute, inclinacao = 0.0, -4.0
        if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS: glfw.set_window_should_close(janela, True)
        
        largura, altura = glfw.get_framebuffer_size(janela)
        if largura <= 0 or altura <= 0: continue
        
        glViewport(0, 0, largura, altura)
        glClearColor(0.45, 0.70, 0.89, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        desenhar_ceu()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(59.0, largura / altura, 0.1, 140.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        olho = (0.0, 3.7, 18.0)
        direcao_x = math.sin(math.radians(azimute))
        direcao_z = -math.cos(math.radians(azimute))
        direcao_y = math.tan(math.radians(inclinacao))
        gluLookAt(*olho, olho[0] + 30 * direcao_x, olho[1] + 30 * direcao_y, olho[2] + 30 * direcao_z, 0, 1, 0)
        glCallList(cenario)
        tecla_p = glfw.get_key(janela, glfw.KEY_P) == glfw.PRESS
        
        if tecla_p and not tecla_p_anterior: salvar_imagem(janela)
        
        tecla_p_anterior = tecla_p
        glfw.swap_buffers(janela)
    
    glDeleteLists(cenario, 1)
    glfw.terminate()

if __name__ == '__main__':
    main()