import pygame
import sys
from pygame.locals import *

from map import MAP

pygame.init()

PLAYER_ASSETS = "apples_pack_60x60px"
APPLE_ASSETS = "apples_pack_60x60px"
OBSTACLE_ASSETS = "Dungeon assets (extract.me)/PNG/Pole/Outline/Pole_outline_green2.png"

font_small = pygame.font.SysFont("Verdana", 20)

background = pygame.image.load("grid.jpg")

SCREEN_WIDTH = 576
SCREEN_HEIGHT = 360

APPLES_IN_COL = 10
APPLES_IN_ROW = 16

FPS = 60
clock = pygame.time.Clock()

TOTAL_SCORE = 0



surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
surface.fill((255, 255, 255))
pygame.display.set_caption("Game")


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.image.load(OBSTACLE_ASSETS)
        self.image = pygame.transform.scale(self.image, (30, 60))
        self.rect = self.image.get_rect()
        self.rect.center = center



class Apple(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.image.load(f"{APPLE_ASSETS}/apple_regular_60x60px.png")
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = center


class Player(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.image.load(f"{PLAYER_ASSETS}/apple_golden_60x60px.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self, obstacles):
        movement = 5
        pressed = pygame.key.get_pressed()

        new_rect = self.rect.copy()
        if pressed[K_LEFT] and self.rect.left > 0:
            new_rect.x -= movement
        if pressed[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            new_rect.x += movement
        if pressed[K_UP] and self.rect.top > 0:
            new_rect.y -= movement
        if pressed[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            new_rect.y += movement

        for obstacle in obstacles:
            if new_rect.colliderect(obstacle.rect):
                if pressed[K_LEFT]:
                    self.rect.left = obstacle.rect.right
                if pressed[K_RIGHT]:
                    self.rect.right = obstacle.rect.left
                if pressed[K_UP]:
                    self.rect.top = obstacle.rect.bottom
                if pressed[K_DOWN]:
                    self.rect.bottom = obstacle.rect.top
            else:
                self.rect = new_rect



apples = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

apple_grid = []
obstacles_grid = []
for y in range(APPLES_IN_COL):
    for x in range(APPLES_IN_ROW):
        apple_x = int((x / APPLES_IN_ROW) * SCREEN_WIDTH) + 15
        apple_y = int((y / APPLES_IN_COL) * SCREEN_HEIGHT) + 15
        if MAP[y][x] == "A":
            apple = Apple((apple_x, apple_y))
            apple_grid.append(apple)
        elif MAP[y][x] == "O":
            obstacle = Obstacle((apple_x+3, apple_y-13))
            obstacles_grid.append(obstacle)
        elif MAP[y][x] == "P":
            P1 = Player((apple_x, apple_y))

apples.add(apple_grid)
obstacles.add(obstacles_grid)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    surface.blit(background, (0, 0))

    scores = font_small.render(f"Score: {TOTAL_SCORE}", True, (0, 0, 0))
    surface.blit(scores, (10, 10))

    for apple in apples:
        surface.blit(apple.image, apple.rect)
    for obstacle in obstacles:
        surface.blit(obstacle.image, obstacle.rect)

    collided_apple = pygame.sprite.spritecollideany(P1, apples)
    if collided_apple:
        TOTAL_SCORE += 1
        collided_apple.kill()

    surface.blit(P1.image, P1.rect)
    P1.move(obstacles)

    pygame.display.update()
    clock.tick(FPS)



