import pygame
import math
import random
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()
logger.info("Program started")

def f(x):
    return x

def g(x):
    return x ** 2

def h(x):
    return math.sin(x)

pygame.init()

w = 600
h = 600

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Draw graph")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    screen.fill((0, 0, 0))


    for x in range(w):
        x = random.randint(0, w)
        y = random.randint(0, h)
        screen.set_at((x, y), (255, 255, 255))
        pygame.draw.line(screen, (255, 255, 255), (x, dy), (x, y))
        # pygame.draw.line(screen, (0, 255, 0), (10, 10), (300, 300))
        dy = y

    pygame.display.flip()

pygame.quit()