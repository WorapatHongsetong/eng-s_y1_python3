import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flying Circle")

clock = pygame.time.Clock()

running = True
while running:

    screen.fill(BLACK)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
