from PIL import Image, ImageOps
import pypokedex
import requests
from sqlalchemy import false


def color_edges(filename):
    img = Image.open(filename)
    width, height = img.size
    img_rgb = img.convert("RGBA")

    # scan and returns the real height , y top/bottom
    new_height = 0
    y_top = 0
    y_bottom = 0
    for y in range(0, height):
        # _______________
        # ...............
        # ...............
        # ...............
        # ...............
        colored_line = False
        for x in range(0, width):
            rgb_pixel_value = img_rgb.getpixel((x, y))
            if rgb_pixel_value[0] == 0 and rgb_pixel_value[1] == 0 and rgb_pixel_value[2] == 0 and rgb_pixel_value[3] == 0:
                continue
            colored_line = True
            new_height += 1
            y_bottom = y
            break

        if new_height == 1 and colored_line:
            y_top = y

    # scan and returns the real width , x left/right
    new_width = 0
    x_left = 0
    x_right = 0
    for x in range(0, width):
        # |............
        # |............
        # |............
        # |............
        # |............
        colored_line = False
        for y in range(0, height):
            rgb_pixel_value = img_rgb.getpixel((x, y))
            if rgb_pixel_value[0] == 0 and rgb_pixel_value[1] == 0 and rgb_pixel_value[2] == 0 and rgb_pixel_value[3] == 0:
                continue
            colored_line = True
            new_width += 1
            x_right = x
            break

        if new_width == 1 and colored_line:
            x_left = x

    img = img.crop((x_left, y_top, x_right, y_bottom))
    img.save(filename)


pokemonColor = 'default'
for number in range(1, 143):

    pokemon = pypokedex.get(
        dex=number)
    response = requests.get(
        pokemon.sprites.front.get(pokemonColor))
    filename = f"pokemon_images\pokemon{number}mirror.png"
    try:

        file = open(filename, "x")
    except:
        pass
    file = open(filename, "wb")
    file.write(response.content)
    file.close()

    color_edges(filename)

    im = Image.open(filename)
    im_flip = ImageOps.mirror(im)
    im_flip.save(filename, quality=95)
