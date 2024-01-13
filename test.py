import pygame
import math
from Objects import Object, Rocket

pygame.init()

WIN_HEIGHT = 1000
WIN_WIDTH = 1600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Test")
win.fill((255, 255, 255))

clock = pygame.time.Clock()

rocket = Rocket(win, (800,500), math.pi/2)

run = True
while run == True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Checks left and right keys for object rotation
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        rocket.rotate(2)
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        rocket.rotate(1)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        rocket.rotate(-1)
    else:
        rocket.rotate(0)
    if keys[pygame.K_SPACE]:
        rocket.move(True)
    else:
        rocket.move(False)
    if keys[pygame.K_RETURN]:
        rocket.reset_position()

    #Updates objects
    win.fill((255, 255, 255))
    rocket.draw()

    #Updates the display
    pygame.display.update()