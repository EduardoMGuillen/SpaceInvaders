import pygame
import random
import math
from pygame import mixer
import io
import sys
from button import Button


# Pasar Fuentes a Bytes
def fuente_bytes(fuente):
    # abrir archivo ttf en lectura binaria
    with open(fuente, 'rb') as f:
        # lee todos los bytes del archivo y los almacena en una variable
        ttf_bytes = f.read()
        # Crea un objeto BytesIO a partir d elos bytes del archivo ttf
        return io.BytesIO(ttf_bytes)


# Inicializar Pygame
pygame.init()

# Crear Pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("Assets/ufo.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("Assets/fondo1.jpg")
fondo_menu = pygame.image.load("Assets/fondo2.jpg")

# Agregar Musica
mixer.music.load("Assets/musica_fondo.mp3")
mixer.music.set_volume(0.1)
mixer.music.play(-1)

# Variables del jugador
img_jugador = pygame.image.load("Assets/rocket.png")
posx_jugador = 368
posy_jugador = 530
jugador_x_cambio = 0

# Variables del Enemigo
img_enemigo = []
posx_enemigo = []
posy_enemigo = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 7

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("Assets/enemigo.png"))
    posx_enemigo.append(random.randint(0, 736))
    posy_enemigo.append(random.randint(40, 200))
    enemigo_x_cambio.append(0.9)
    enemigo_y_cambio.append(50)

# Variables de la bala
img_bala = pygame.image.load("Assets/Bala.png")
posx_bala = 0
posy_bala = 530
bala_x_cambio = 0
bala_y_cambio = 0.7
bala_visible = False

# Puntaje
puntaje = 0
fuente_como_bytes = fuente_bytes("ka1.ttf")
fuente = pygame.font.Font(fuente_como_bytes, 32)
texto_x = 10
texto_y = 10

# Texto final del juego
fuente_final = pygame.font.Font("Assets/ka1.ttf", 40)


# Fuente Menu
def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Assets/ka1.ttf", size)


# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# Funcion Jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Funcion dissparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


# Funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))
    if distancia < 25:
        return True
    else:
        return False


# Texto final del juego
def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (170, 200))


# Loop del Juego
se_ejecuta = False
while True:
    while se_ejecuta:
        # RGB
        # pantalla.fill((205, 144, 228))
        pantalla.blit(fondo, (0, 0))

        # Iterar Eventos
        for evento in pygame.event.get():

            # Evento Cerrar
            if evento.type == pygame.QUIT:
                se_ejecuta = False

            # Evento presionar teclas
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    jugador_x_cambio = -0.4
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    jugador_x_cambio = 0.4
                if evento.key == pygame.K_SPACE:
                    if not bala_visible:
                        posx_bala = posx_jugador
                        disparar_bala(posx_bala, posy_bala)

            # Evento Soltar teclas
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_RIGHT or pygame.K_d == evento.key or evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    jugador_x_cambio = 0

        # Modificar Ubicacion al jugador
        posx_jugador += jugador_x_cambio

        # Mantener dentro de bordes al jugador
        if posx_jugador <= 0:
            posx_jugador = 0
        elif posx_jugador >= 736:
            posx_jugador = 736

        # Modificar Ubicacion al enemigo
        for e in range(cantidad_enemigos):
            posx_enemigo[e] += enemigo_x_cambio[e]

            # Fin del Juego
            if posy_enemigo[e] > 500:
                for k in range(cantidad_enemigos):
                    posy_enemigo[k] = 1000
                texto_final()

                # Volver al Menu
                MENU_MOUSE_POS = pygame.mouse.get_pos()
                MENU_BUTTON = Button(image=pygame.image.load("Assets/Menu Rect1.png"), pos=(400, 300),
                                     text_input="Menu principal", font=get_font(32), base_color="White",
                                     hovering_color="#FF0000")

                for button in [MENU_BUTTON]:
                    button.changeColor(MENU_MOUSE_POS)
                    button.update(pantalla)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                            se_ejecuta = False
                            for k in range(cantidad_enemigos):
                                posx_enemigo[k] = random.randint(0, 736)
                                posy_enemigo[k] = random.randint(40, 200)
                            puntaje = 0

                break

            # Mantener dentro de bordes al enemigo
            if posx_enemigo[e] <= 0:
                enemigo_x_cambio[e] = 0.2
                posy_enemigo[e] += enemigo_y_cambio[e]
            elif posx_enemigo[e] >= 736:
                enemigo_x_cambio[e] = -0.2
                posy_enemigo[e] += enemigo_y_cambio[e]

            # Colision
            colision = hay_colision(posx_enemigo[e], posy_enemigo[e], posx_bala, posy_bala)
            if colision:
                sonido_colision = mixer.Sound("Assets/Point.wav")
                mixer.Sound.set_volume(sonido_colision, 0.2)
                sonido_colision.play()
                posy_bala = 530
                bala_visible = False
                puntaje += 1
                posx_enemigo[e] = random.randint(0, 736)
                posy_enemigo[e] = random.randint(0, 200)

            enemigo(posx_enemigo[e], posy_enemigo[e], e)

        # Movimiento bala
        if posy_bala <= -32:
            posy_bala = 500
            bala_visible = False

        if bala_visible:
            disparar_bala(posx_bala, posy_bala)
            posy_bala -= bala_y_cambio

        jugador(posx_jugador, posy_jugador)

        mostrar_puntaje(texto_x, texto_y)

        # Actualizar
        pygame.display.update()

    while not se_ejecuta:
        pantalla.blit(fondo_menu, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(55).render("MAIN MENU", True, "#FF0000")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))
        Name_TEXT = get_font(20).render("Invasion Espacial", True, "#FF0000")
        Name_RECT = Name_TEXT.get_rect(center=(400, 150))

        PLAY_BUTTON = Button(image=pygame.image.load("Assets/Play Rect1.png"), pos=(400, 300),
                             text_input="PLAY", font=get_font(32), base_color="#FF0000", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Assets/Play Rect1.png"), pos=(400, 400),
                             text_input="QUIT", font=get_font(32), base_color="#FF0000", hovering_color="White")

        pantalla.blit(MENU_TEXT, MENU_RECT)
        pantalla.blit(Name_TEXT, Name_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    se_ejecuta = True

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
