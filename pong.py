import sys

import pygame
from pygame.math import Vector2

pygame.init()
clock = pygame.time.Clock()
größe = (600, 600)
screen = pygame.display.set_mode(größe)


class Ball:
    def __init__(self):
        self.pos = Vector2(größe[0] / 2, größe[1] / 2)
        self.direction = Vector2(-1, 0)
        self.radius = 10

    def draw(self):
        self.pos += self.direction
        self.rect = pygame.draw.circle(screen, (255, 0, 0), self.pos, self.radius)


class Schläger:
    def __init__(self, x, y, höhe, breite):
        self.pos = Vector2(x, y)
        self.direction = 0
        self.moving = False
        self.höhe = höhe
        self.breite = breite

    def draw(self):
        self.pos.y += self.direction
        rect = pygame.Rect(self.pos.x, self.pos.y, self.breite, self.höhe)
        self.rect = pygame.draw.rect(screen, (255, 0, 0), rect)


class Game:
    def __init__(self):
        spieler_höhe = 80
        spieler_breite = 20
        self.spieler1 = Schläger(30, größe[1] / 2 - (spieler_höhe / 2), spieler_höhe, spieler_breite)
        self.spieler2 = Schläger(größe[0] - (30 + spieler_breite), größe[1] / 2 - (spieler_höhe / 2), spieler_höhe,
                                 spieler_breite)
        self.ball = Ball()
        self.geschwindigkeit_spieler = 4

    def draw(self):
        self.spieler1.draw()
        self.spieler2.draw()
        self.ball.draw()
        self.check_collisions()

    def check_collisions(self):
        for spieler in [self.spieler1, self.spieler2]:
            if self.ball.rect.colliderect(spieler.rect):
                self.ball.direction *= Vector2(-1, -1)


game = Game()


def handle_keys(key, down):
    if key == pygame.K_w or key == pygame.K_s:
        game.spieler1.moving = down
        if game.spieler1.moving:
            if key == pygame.K_w:
                game.spieler1.direction = -game.geschwindigkeit_spieler
            elif key == pygame.K_s:
                game.spieler1.direction = game.geschwindigkeit_spieler
        else:
            game.spieler1.direction = 0
    if key == pygame.K_UP or key == pygame.K_DOWN:
        game.spieler2.moving = down
        if game.spieler2.moving:
            if key == pygame.K_UP:
                game.spieler2.direction = -game.geschwindigkeit_spieler
            elif key == pygame.K_DOWN:
                game.spieler2.direction = game.geschwindigkeit_spieler
        else:
            game.spieler2.direction = 0


def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                handle_keys(event.key, True)
            if event.type == pygame.KEYUP:
                handle_keys(event.key, False)

        screen.fill((0, 0, 0))
        game.draw()
        pygame.display.update()
        clock.tick(60)


game_loop()
