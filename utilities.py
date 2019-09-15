import pygame


def strip_from_sheet(sheet, start, size, columns, rows=1):
    """
    Strips individual frames from a sprite sheet given a start location,
    sprite size, and number of columns and rows.
    """
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(sheet.subsurface(pygame.Rect(location, size)))
    return frames


def get_font(sprites, start_d, start_l):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    font = {}
    for i in range(start_d, start_d + 10, 1):
        font[str(i)] = sprites[i]
    k = 0
    for i in range(start_l, start_l + len(alphabet), 1):
        font[alphabet[k]] = sprites[i]
        k += 1
    return alphabet