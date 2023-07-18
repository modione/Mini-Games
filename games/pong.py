import pygame
from pygame.math import Vector2
import random
import time

pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()


class Schläger:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.score = 0

    def move(self, y):
        if 0 < self.y + y < 600 - 90:
            self.y += y

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, 20, 90)
        pygame.draw.rect(screen, (255, 255, 255), self.rect)


class Ball:
    def __init__(self, pos):
        self.pos = pos
        self.start_pos = pos
        self.speed = 2
        rn = random.choice([-self.speed, self.speed])
        rn2 = random.choice([-self.speed, self.speed])
        self.dir = Vector2(rn, rn2)

    def collissions(self):
        # Collisions with walls
        next_pos = self.pos + self.dir
        if next_pos.x < 0 or next_pos.x > 880:
            self.pos = Vector2(450, 300)
            self.speed = 2
            rn = random.choice([-self.speed, self.speed])
            rn2 = random.choice([-self.speed, self.speed])
            self.dir = Vector2(rn, rn2)
            if next_pos.x < 0:
                p2.score += 1
            else:
                p1.score += 1

        if next_pos.y < 0 or next_pos.y > 580:
            self.dir.y *= -1
        # Collisions with players
        rect = pygame.Rect(next_pos.x, next_pos.y, 20, 20)
        if rect.colliderect(p1.rect) or rect.colliderect(p2.rect):
            self.dir.x = -self.dir.x
            if self.speed < 12:
                if self.dir.x < 0:
                    self.dir.x -= 1
                else:
                    self.dir.x += 1
                if self.dir.y < 0:
                    self.dir.y -= 1
                else:
                    self.dir.y += 1
                self.speed += 1

    def draw(self):
        self.collissions()
        self.pos += self.dir
        rect = pygame.Rect(self.pos.x, self.pos.y, 20, 20)
        pygame.draw.rect(screen, (255, 255, 255), rect)


p1 = Schläger(50, 255)
p2 = Schläger(830, 255)
ball = Ball(Vector2(450, 300))
bot = False

zeit = time.time()


def auto():
    global zeit
    if time.time() >= zeit + 0.01:
        zeit = time.time()
        if ball.dir.x < 0:
            turn = False
        else:
            turn = True
        if turn and ball.pos.y not in range(p2.y, p2.y+45):
            if ball.pos.y > p2.y + 45:
                p2.move(10)
            else:
                p2.move(-10)


def backround():
    font = pygame.font.SysFont(None, 52)
    p1_score = font.render(str(p1.score), True, (255, 255, 255))
    p2_score = font.render(str(p2.score), True, (255, 255, 255))

    screen.blit(p1_score, (350, 100))
    screen.blit(p2_score, (550, 100))

    rect = pygame.Rect(455, 0, 10, 600)
    pygame.draw.rect(screen, (255, 255, 255), rect)


def handle_keys():
    speed = 10
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        p1.move(-speed)
    if keys[pygame.K_s]:
        p1.move(speed)
    if not bot:
        if keys[pygame.K_UP]:
            p2.move(-speed)
        if keys[pygame.K_DOWN]:
            p2.move(speed)


def gameloop():
    global bot
    bot = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        handle_keys()
        screen.fill((0, 0, 0))
        backround()
        p1.draw()
        p2.draw()
        backround()
        ball.draw()
        if bot:
            auto()
        pygame.display.update()
        clock.tick(60)


gameloop()
