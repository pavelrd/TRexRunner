import player
import enemy
import scene
import pygame
from utilities import strip_from_sheet
import random
import time

sprite_sheet_t_rex = pygame.image.load('2x-trex.png')
sprite_sheet_obstacle = pygame.image.load('2x-obstacle-large.png')
sprite_sheet_digits = pygame.image.load('numbers-sprite-100.png')
sprite_sheet_font = pygame.image.load('font.png')

t_rex_sprite_sheet_size = sprite_sheet_t_rex.get_size()
obstacle_sprite_sheet_size = sprite_sheet_obstacle.get_size()
digits_sprite_sheet_size = sprite_sheet_digits.get_size()
font_sprite_sheet_size = sprite_sheet_font.get_size()

sprite_count = 6

sprites_t_rex = strip_from_sheet(sprite_sheet_t_rex, (0, 0), (t_rex_sprite_sheet_size[0] / sprite_count,
                                                              t_rex_sprite_sheet_size[1]), sprite_count)

sprites_obstacle = strip_from_sheet(sprite_sheet_obstacle, (0, 0), (obstacle_sprite_sheet_size[0] / sprite_count,
                                                                    obstacle_sprite_sheet_size[1]), sprite_count)

sprites_digits = strip_from_sheet(sprite_sheet_digits, (0, 0), (digits_sprite_sheet_size[0] / 10,
                                                                digits_sprite_sheet_size[1] / 3), 10)

sprites_font = strip_from_sheet(sprite_sheet_font, (0, 0), (font_sprite_sheet_size[0]/15,
                                                            font_sprite_sheet_size[1]/8), 15, 4)

size = sprites_digits[0].get_size()

for i in range(len(sprites_digits)):
    sprites_digits[i] = pygame.transform.scale(sprites_digits[i], (int(size[0]*0.3), int(size[1]*0.3)))

digits = dict()
k = 0
for i in range(16, 26, 1):
    digits[str(k)] = sprites_font[i]
    k += 1

WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0

FRAME_RATE = 60

scene = scene.Scene((800, 600))
scene.screen.fill(WHITE)

size = sprites_t_rex[0].get_size()

for i in range(len(sprites_t_rex)):
    sprites_t_rex[i] = pygame.transform.scale(sprites_t_rex[i], (int(size[0]*0.6), int(size[1]*0.6)))

player = player.Player(sprites_t_rex[2], scene)
player.digits = digits
player.sprites = sprites_t_rex
enemy_sprite = sprites_obstacle[0]
enemy = enemy.Enemy(enemy_sprite, scene)
player.font = sprites_font

scene.add_object(player)
scene.add_object(enemy)

player.set_scene(scene)

done = True

clock = pygame.time.Clock()

player.place_to(50, player.bottom - player.image.get_size()[1]*0.5)

ticker = 5
pressed_space = False

player.set_sprite(sprites_t_rex[0])

# TODO: - display player lives
#  - implement random enemy placing algorithm
#  - implement ducking
#  - create flying enemies
#  - implement GAME OVER +
#  - add 'SCORE: ' before score +
#  - add best result for score
#  - add lives
#  - implement PAUSE

while not pressed_space:
    scene.screen.blit(digits['0'], (0, 0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pressed_space = True
            done = True
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                pressed_space = True
                done = False
                player.is_in_jump = True

    player.jump()
    player.update()
    pygame.display.update()
    clock.tick()

enemy.place_to(enemy.x, enemy.bottom - enemy.image.get_size()[1] * 0.5)
scene.clear()

while not done:
    player.draw_score()
    ticker -= 1
    if ticker < 0:
        ticker = 5
        if player.image == sprites_t_rex[2]:
            player.set_sprite(sprites_t_rex[3])
        else:
            player.set_sprite(sprites_t_rex[2])
        player.score += 1
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                player.is_in_jump = True
            if e.key == pygame.K_ESCAPE:
                player.dt = 0

    scene.clear()
    pygame.draw.line(scene.screen, BLACK, (0, player.bottom), (scene.width, player.bottom))
    player.jump()
    player.update()
    player.draw_score()

    if not player.check_for_collisions():
        enemy.move(-5)
        sound = pygame.mixer.Sound('error.wav')
        #enemy.draw_borders(GREEN)
    else:
        player.lives -= 1
        if player.lives == 0:
            done = True
        sound.play()
        enemy.set_sprite(random.choice(sprites_obstacle))
        enemy.place_to(enemy.scene.width + enemy.image.get_size()[0], enemy.bottom - enemy.image.get_size()[1] * 0.5)
    pygame.display.update()
    elapsed = clock.tick(60)
    player.dt = elapsed * 0.001
