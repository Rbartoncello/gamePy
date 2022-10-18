import pygame
import colores
from Character import Character
from Player import Player
from Button import Button
from Rect import Rect
import time

ANCHO_VENTANA = 800
ALTO_VENTANA = 950
FONT_SIZE = 50


def create_zombies(amount: int):
    zombies = []
    for i in range(amount):
        zombies.append(Character(50, 50, "./zombie.png", ANCHO_VENTANA, ALTO_VENTANA, 5 / 16))
    return zombies


def create_sounds(pygame):
    return {
        'background': pygame.mixer.Sound("./background.wav"),
        'game_over': pygame.mixer.Sound("./game_over.mp3")
    }


def create_texts(pygame, player):
    font_text = pygame.font.SysFont("Arial Narrow", FONT_SIZE)
    font_game_over = pygame.font.SysFont("Arial Narrow", 150)
    return {
        'new_game': font_text.render("Nuevo partida", True, colores.GREEN),
        'exit': font_text.render("Salir", True, colores.RED1),
        'submit': font_text.render("Si", True, colores.GREEN),
        'cancel': font_text.render("No", True, colores.RED1),
        'should_exit': font_text.render("Desea salir", True, colores.BLUE),
        'select_character': font_text.render("Seleccione el personaje de desea ser", True, colores.CYAN4),
        'level': font_text.render("Nivel: {}".format(player.get_level()), True, colores.RED4),
        'life': font_text.render("Vida: x{}".format(player.get_life()), True, colores.RED4),
        'game over': font_game_over.render("GAME OVER....", True, colores.RED3),
    }


def create_buttons():
    buttons = {
        'new_game': Button(400, 50, ANCHO_VENTANA, ALTO_VENTANA, ANCHO_VENTANA / 2, ALTO_VENTANA / 2, texts['new_game'], './select_sound.wav'),
        'submit': Button(100, 50, ANCHO_VENTANA, ALTO_VENTANA, ANCHO_VENTANA * 5 / 16, ALTO_VENTANA * 3 / 4, texts['submit'], './select_sound.wav'),
        'cancel': Button(100, 50, ANCHO_VENTANA, ALTO_VENTANA, ANCHO_VENTANA * 11 / 16, ALTO_VENTANA * 3 / 4, texts['cancel'], './select_sound.wav')
    }
    buttons.update({'exit': Button(400, 50, ANCHO_VENTANA, ALTO_VENTANA, ANCHO_VENTANA / 2, buttons['new_game'].get_center_y() + texts['new_game'].get_height() + 30, texts['exit'], './select_sound.wav')})
    return buttons


def create_characters():
    return {
        '1': Player(150, 150, "./character_1.png", ANCHO_VENTANA, ALTO_VENTANA, 5 / 16, "./player_1.mp3"),
        '2': Player(150, 150, "./character_2.png", ANCHO_VENTANA, ALTO_VENTANA, 11 / 16, "./player_2.mp3"),
        'save': Character(50, 50, "./character_to_help.png", ANCHO_VENTANA, ALTO_VENTANA, 11 / 16, "./helped_character.wav"),
        'main': Player(50, 50, "./character_1.png", ANCHO_VENTANA, ALTO_VENTANA, 5 / 16, "./select_sound.wav"),
    }


def create_rects(gif):
    rects = {
        'should_exit': Rect(texts['should_exit'].get_width(), 30, ANCHO_VENTANA, ALTO_VENTANA, 1 / 2),
        'select_character': Rect(texts['select_character'].get_width(), 30, ANCHO_VENTANA, ALTO_VENTANA, 1 / 2),
        'level': Rect(texts['level'].get_width(), 30, ANCHO_VENTANA, ALTO_VENTANA, 0),
        'life': Rect(texts['life'].get_width(), 30, ANCHO_VENTANA, ALTO_VENTANA, 0),
        'game over': Rect(texts['game over'].get_width(), 30, ANCHO_VENTANA, ALTO_VENTANA, 0),
        'level life': Rect(ANCHO_VENTANA + 200, 50, ANCHO_VENTANA, ALTO_VENTANA, 0)
    }
    rects['should_exit'].update(rects['should_exit'].get_rect().centerx, ALTO_VENTANA / 2 + gif.get_height() / 2 + 20)
    rects['select_character'].update(rects['select_character'].get_rect().centerx, ALTO_VENTANA * 5 / 16)
    rects['level'].update(texts['level'].get_width() / 2 + 10, ALTO_VENTANA + 25)
    rects['life'].update(ANCHO_VENTANA - texts['life'].get_width() / 2 - 10, ALTO_VENTANA + 25)
    rects['game over'].update(ANCHO_VENTANA / 2, ALTO_VENTANA / 2)
    rects['level life'].update(ANCHO_VENTANA/2, ALTO_VENTANA + 25)

    return rects


def is_object_a_touching_by_object_b(object_a, object_b):
    return object_a.get_rect().colliderect(object_b.get_rect())

def randomization_character(main, save, list_zombies):
    main.update_random()
    save.update_random()

    for zombie in list_zombies:
        zombie.update_random()
        while is_object_a_touching_by_object_b(main, zombie):
            zombie.update_random()


pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.01)

sounds = create_sounds(pygame)
sounds['background'].set_volume(0.03)

screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA + 50))
pygame.display.set_caption("Game")

# TIMER
timer = pygame.USEREVENT + 0
pygame.time.set_timer(timer, 100)

gif = pygame.transform.scale(pygame.image.load("./end_game.gif"), (250, 250))

characters = create_characters()
texts = create_texts(pygame, characters['main'])
buttons = create_buttons()
list_zombies = {}
rects = create_rects(gif)

flag_run = True
new_game = False
exit_game = False
player_select = False
is_playing = False
game_over = False

while flag_run:
    sounds['background'].play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag_run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not new_game:
                if buttons['new_game'].get_rect_view().collidepoint(event.pos):
                    buttons['new_game'].do_sound(sounds['background'])
                    new_game = True
                if buttons['exit'].get_rect_view().collidepoint(event.pos):
                    buttons['exit'].do_sound(sounds['background'])
                    exit_game = True
            if buttons['submit'].get_rect_view().collidepoint(event.pos):
                buttons['submit'].do_sound(sounds['background'])
                flag_run = False
            if buttons['cancel'].get_rect_view().collidepoint(event.pos):
                buttons['cancel'].do_sound(sounds['background'])
                exit_game = False
            if characters['1'].get_rect().collidepoint(event.pos):
                characters['1'].do_sound(sounds['background'], characters['1'].get_lenght_sound())
                player_select = True
                characters['main'].set_image('./character_1.png')
                break
            if characters['2'].get_rect().collidepoint(event.pos):
                characters['2'].do_sound(sounds['background'], characters['2'].get_lenght_sound())
                player_select = True
                characters['main'].set_image('./character_2.png')
                break
        if is_playing:
            for zombie in list_zombies:
                while is_object_a_touching_by_object_b(characters['save'], zombie):
                    zombie.update_random()
                if is_object_a_touching_by_object_b(characters['main'], zombie):
                    zombie.delete()
                    characters['main'].set_life()
                    if characters['main'].is_dead():
                        new_game = False
                        game_over = True
                        break
            if is_object_a_touching_by_object_b(characters['main'], characters['save']):
                characters['save'].do_sound(sounds['background'], characters['save'].get_lenght_sound())
                characters['save'].update_random()
                list_zombies.extend(create_zombies(5))
                characters['main'].set_level()
                for zombie in list_zombies:
                    zombie.increase_speed()
                    while is_object_a_touching_by_object_b(characters['main'], zombie) or is_object_a_touching_by_object_b(
                            characters['save'], zombie):
                        zombie.update_random()
            if event.type == pygame.USEREVENT:
                if event.type == timer:
                    for zombie in list_zombies:
                        zombie.move()

    screen.fill(colores.BLACK)

    if new_game:
        if player_select:
            list_zombies = create_zombies(10)
            randomization_character(characters['main'], characters['save'], list_zombies)

            player_select = False
            is_playing = True
        elif is_playing:
            characters['main'].move_by_key(pygame.key.get_pressed())

            characters['main'].to_show(screen)
            characters['save'].to_show(screen) 
            
            for zombie in list_zombies: zombie.to_show(screen)

            pygame.draw.rect(screen, colores.AQUAMARINE3, rects['level life'])
            font = pygame.font.SysFont("Arial Narrow", FONT_SIZE)

            rects['level'].to_show(font.render("Nivel: {}".format(characters['main'].get_level()), True, colores.RED4), screen)
            rects['life'].to_show(font.render("Vida: x{}".format(characters['main'].get_life()), True, colores.RED4), screen)
        else:
            sounds['background'].set_volume(0.01)
            rects['select_character'].to_show(texts['select_character'], screen)
            characters['1'].to_show(screen)
            characters['2'].to_show(screen)

    elif exit_game:

        buttons['new_game'].to_show(colores.BLACK, screen)
        buttons['exit'].to_show(colores.BLACK, screen)

        buttons['submit'].to_show(colores.WHITE, screen)
        buttons['cancel'].to_show(colores.WHITE, screen)

        screen.blit(gif, (275, 355))
        rects['should_exit'].to_show(texts['should_exit'], screen)
    elif game_over:
        is_playing = False
        for zombie in list_zombies: del zombie
        characters['main'].reset()
        rects['game over'].to_show(texts['game over'], screen)
        pygame.display.flip()
        sounds['background'].stop()
        sounds['game_over'].play()
        sounds['game_over'].set_volume(1)
        time.sleep(sounds['game_over'].get_length())
        sounds['game_over'].stop()
        sounds['background'].play()
        game_over = False
    else:
        buttons['new_game'].to_show(colores.WHITE, screen)
        buttons['exit'].to_show(colores.WHITE, screen)

    pygame.display.flip()
pygame.quit()
