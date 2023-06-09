import random
import pygame
import sys
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            if self.body.index(block) == 0:
                pygame.draw.rect(screen, (255, 0, 0), block_rect)
            else:
                pygame.draw.rect(screen, (255, 0, 0), block_rect)

    def move_snake(self):
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

    def draw_fruit(self):
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

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.random_pos()
            self.snake.add_block()
            self.score += 1

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                print("Self Crash")
                self.game_over()

    def game_over(self):
        print("Score:", self.score)
        pygame.quit()
        sys.exit()


pygame.init()
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()


def handle_keys(key):
    if key == pygame.K_w:
        main_game.snake.direction = Vector2(0, -1)
    if key == pygame.K_s:
        main_game.snake.direction = Vector2(0, 1)
    if key == pygame.K_a:
        main_game.snake.direction = Vector2(-1, 0)
    if key == pygame.K_d:
        main_game.snake.direction = Vector2(1, 0)
    if key == pygame.K_f:
        main_game.snake.direction = Vector2(0, 0)


def handle_events(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == SCREEN_UPDATE:
        main_game.update()
    if event.type == pygame.KEYDOWN:
        handle_keys(event.key)


def game_loop():
    while True:
        for event in pygame.event.get():
            handle_events(event)

        screen.fill((175, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        # Limit FPS: clock.tick(60)


if __name__ == '__main__':
    game_loop()
