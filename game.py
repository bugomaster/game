import PIL
import pygame
import random

import pypokedex
import requests
from sqlalchemy import true
pygame.init()
clock = pygame.time.Clock()
score = 0
screen = pygame.display.set_mode((500, 1000))

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
TEAL = (0, 128, 128)


def printText(text, color, size, x, y):
    text_obj = pygame.font.Font('font.ttf', size).render(text, True, color)
    screen.blit(text_obj, (x, y))


def printPokemon(x, y,  number, is_mirror):
    filename = ""

    if is_mirror == 1:
        filename = f"pokemon_images\pokemon{number}.png"
    else:
        filename = f"pokemon_images\pokemon{number}mirror.png"

    poke_surface = pygame.image.load(
        filename)
    screen.blit(poke_surface, (x, y))

    return poke_surface.get_width(), poke_surface.get_height()


def print_bullets():
    global one_bullet_pics_ptr
    global bullet_pics_ptr
    global y
    y_save = y
    hit_pokemon = False
    bullet_pics_ptr += one_bullet_pics_ptr
    one_bullet_pics_ptr *= -1
    y_dis_from_obs = 0
    pokemon_ii = 0
    for i in range(0, len(pokemons_x)):
        x_bullet = x + 25
        if x_bullet >= pokemons_x[i] and x_bullet <= pokemons_x[i] + pokemons_width[i]:
            hit_pokemon = True
            y_dis_from_obs = pokemons_y[i] + pokemons_height[i]
            pokemon_ii = i
            break
    for y in range(y_dis_from_obs, y, 14):
        screen.blit(bullet_pics[bullet_pics_ptr], (x + 25, y))
    y = y_save
    return hit_pokemon, pokemon_ii


player_width = 50
player_height = 62

player_run1 = pygame.image.load('pics/playerRun1.png').convert_alpha()
player_run1 = pygame.transform.scale(
    player_run1, (player_width, player_height))
player_run2 = pygame.image.load('pics/playerRun2.png').convert_alpha()
player_run2 = pygame.transform.scale(
    player_run2, (player_width, player_height))
background = pygame.image.load('pics/Background.png').convert_alpha()
background = pygame.transform.scale(background, (500, 1000))
bullet_pos1 = pygame.image.load('pics/bullet_pos1.png')
bullet_pos2 = pygame.image.load('pics/bullet_pos2.png')
bullet_pics = [bullet_pos1, bullet_pos2]
dividers_arr = [1000, 500, 250]
running_player = [player_run1, player_run2]
running_ptr = 0
one = 1
bullet_pics_ptr = 0
x = 250
y = 750
running = True

pokemon_width = 0
pokemon_height = 0
bg_y = 0
pokemons_x = []
pokemons_y = []
pokemons_width = []
pokemons_height = []
pokemons_hp = []
pokemons_ids = []
running_pokemon_ptr = 0
one_pokemon_ptr = 1
one_bullet_pics_ptr = 1
number_of_runs = 0
while running:
    shooting = False
    number_of_runs += 1
    clock.tick(30)
    if number_of_runs >= 5:

        running_pokemon_ptr += one_pokemon_ptr
        one_pokemon_ptr *= -1
        number_of_runs = 0
    keyState = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if keyState[pygame.K_x]:
        shooting = True
    if keyState[pygame.K_UP] and keyState[pygame.K_LEFT]:
        running_ptr += one
        one *= -1
        if x != 0:
            x -= 10
    elif keyState[pygame.K_UP] and keyState[pygame.K_RIGHT]:
        running_ptr += one
        one *= -1

        if x != 500:
            x += 10
    elif keyState[pygame.K_UP]:
        running_ptr += one
        one *= -1
        if y >= 760:
            y -= 10
    elif keyState[pygame.K_LEFT]:
        running_ptr += one
        one *= -1
        if x != 0:
            x -= 10
    elif keyState[pygame.K_RIGHT]:
        running_ptr += one
        one *= -1

        if x < 500 - player_width:
            x += 10
    else:
        y += 10
        if y >= 970:
            running = False
    for i in range(0, len(pokemons_y)):
        if y >= pokemons_y[i] and y <= pokemons_y[i] + pokemons_height[i] and x >= pokemons_x[i] and x <= pokemons_x[i] + pokemons_width[i]:
            running = False

    screen.blit(background, (0, -1000 + bg_y))

    screen.blit(background, (0, bg_y))
    bg_y += 10
    try:

        for i in range(0, len(pokemons_y)):
            pokemons_y[i] += 10
            if pokemons_y[i] == 800:
                pokemons_x.pop(i)
                pokemons_y.pop(i)
                pokemons_width.pop(i)
                pokemons_height.pop(i)
                pokemons_hp.pop(i)
                pokemons_ids.pop(i)
    except:
        pass
    new_pokemon = False
    if bg_y % dividers_arr[random.randint(0, len(dividers_arr)-1)] == 0:

        pokemons_ids.append(random.randint(1, 143))

        pokemons_x.append(random.randint(1, 400))
        pokemons_y.append(0)
        new_pokemon = True
    if bg_y == 1000:
        bg_y = 0

    screen.blit(running_player[running_ptr], (x, y))
    i = 0
    for pokemon_id in pokemons_ids:

        pokemon_width, pokemon_height = printPokemon(pokemons_x[i], pokemons_y[i],
                                                     pokemon_id, running_pokemon_ptr)

        i += 1

    if new_pokemon:
        pokemons_width.append(pokemon_width)
        pokemons_height.append(pokemon_height)
        pokemons_hp.append(pokemon_width+pokemon_height)
    if shooting:
        hit, pokemon_indexx = print_bullets()
        if hit:
            print(f"-10 hp to {pokemon_indexx}")
            pokemons_hp[pokemon_indexx] -= 10

    i = 0
    for pokemon_id in pokemons_ids:
        if pokemons_hp[i] <= 1:
            pokemons_x.pop(i)
            pokemons_y.pop(i)
            pokemons_width.pop(i)
            pokemons_height.pop(i)
            pokemons_hp.pop(i)
            pokemons_ids.pop(i)
            print(f"{pokemon_id} died")
            score += 1
        i += 1
    printText(f"{score}", RED, 50, 250, 0)
    pygame.display.flip()
