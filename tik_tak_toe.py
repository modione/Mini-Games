import sys

import pygame

pygame.init()
clock = pygame.time.Clock()
cell_size = 200
screen = pygame.display.set_mode((cell_size * 3 + 100, 100 + cell_size * 3))


def draw_lines():
    pygame.draw.line(screen, pygame.Color("green"), (0, cell_size), (cell_size, 0))


def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_lines()
        pygame.display.update()
        clock.tick(60)


game_loop()
