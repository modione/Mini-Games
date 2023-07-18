import random

import pygame
from pygame.math import Vector2

from sql import SQL


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            if self.body.index(block) == 0:
                pygame.draw.rect(screen, (255, 0, 0), block_rect)
            else:
                pygame.draw.rect(screen, (255, 0, 0), block_rect)

    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class FRUIT:
    def __init__(self):
        self.random_pos()

    def draw(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def random_pos(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.dead = False
        self.score = 0
        self.running = True
        self.high_score = 0

    def update(self):
        self.snake.move()
        self.collisions()
        self.check_tod()

    def draw(self):
        if self.running:
            self.snake.draw()
            self.fruit.draw()
            font = pygame.font.SysFont(None, 24)
            score = font.render("Score " + str(self.score), True, (255, 255, 255))
            screen.blit(score, (10, 10))
        else:
            font = pygame.font.SysFont(None, 36)
            final_score = font.render("Final score:" + str(self.score) + " High Score:" + str(self.high_score), True,
                                      (255, 255, 255))
            x, y = screen.get_size()
            center = (
                (x - final_score.get_width()) / 2,
                (y - final_score.get_height()) / 2
            )
            screen.blit(final_score, center)
            restart_text = font.render("Restart", True, (255, 255, 255))
            center = (
                (x - restart_text.get_width()) / 2,
                ((y - restart_text.get_height()) / 2) + final_score.get_height() + 20
            )
            rect = pygame.Rect(center[0] - 5, center[1] - 5, restart_text.get_width() + 10,
                               restart_text.get_height() + 10)
            global restart_button
            a, b = pygame.mouse.get_pos()
            if rect.x <= a <= rect.x + rect.width and rect.y <= b <= rect.y + rect.height:
                color = (180, 180, 180)
            else:
                color = (110, 110, 110)
            restart_button = pygame.draw.rect(screen, color, rect)
            screen.blit(restart_text, center)

    def collisions(self):
        if self.fruit.pos == self.snake.body[0]:
            collision = True
            while collision:
                collision = False
                self.fruit.random_pos()
                for teil in self.snake.body:
                    if teil == self.fruit.pos:
                        collision = True
            self.snake.add_block()
            self.score += 1

    def check_tod(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        if self.running:
            print("Game over")
            self.running = False
            sql = SQL()
            sql.insert_score(name, "Snake", self.score)
            self.high_score = sql.get_score(name, "Snake")
            sql.close_conn()


pygame.init()
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()
restart = False
name = ""
restart_button = None


def handle_keys(key):
    if key == pygame.K_w and not main_game.snake.direction == Vector2(0, 1):
        main_game.snake.direction = Vector2(0, -1)
    if key == pygame.K_s and not main_game.snake.direction == Vector2(0, -1):
        main_game.snake.direction = Vector2(0, 1)
    if key == pygame.K_a and not main_game.snake.direction == Vector2(1, 0):
        main_game.snake.direction = Vector2(-1, 0)
    if key == pygame.K_d and not main_game.snake.direction == Vector2(-1, 0):
        main_game.snake.direction = Vector2(1, 0)
    if key == pygame.K_f:
        global restart
        restart = True


def handle_events(event):
    if event.type == pygame.QUIT:
        pygame.quit()
    if event.type == SCREEN_UPDATE:
        main_game.update()
    if event.type == pygame.KEYDOWN:
        handle_keys(event.key)
    if event.type == pygame.MOUSEBUTTONUP:
        if restart_button is not None:
            if restart_button.collidepoint(event.pos):
                global restart
                restart = True


def game_loop(username):
    while True:
        global main_game
        global restart
        global name
        name = username
        if restart:
            main_game = MAIN()
            restart = False
            global restart_button
            restart_button = None
        for event in pygame.event.get():
            handle_events(event)

        screen.fill((175, 215, 70))
        main_game.draw()
        pygame.display.update()
        # Limit FPS: clock.tick(60)


if __name__ == '__main__':
    game_loop("test")