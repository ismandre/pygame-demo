import pygame
import sys
from pygame.locals import *

pygame.init()

PLAYER_ASSETS = "apples_pack_60x60px"
APPLE_ASSETS = "apples_pack_60x60px"
OBSTACLE_ASSETS = "Dungeon assets (extract.me)/PNG/Pole/Outline/Pole_outline_green1.png"

font_small = pygame.font.SysFont("Verdana", 20)

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

APPLES_IN_COL = 10
APPLES_IN_ROW = 5

FPS = 60
clock = pygame.time.Clock()

TOTAL_SCORE = 0



surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
surface.fill((255, 255, 255))
pygame.display.set_caption("Game")


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(OBSTACLE_ASSETS)
        self.image = pygame.transform.scale(self.image, (60, 120))
        self.rect = self.image.get_rect()
        self.rect.center = (300, 300)



class Apple(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.image.load(f"{APPLE_ASSETS}/apple_regular_60x60px.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = center


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(f"{PLAYER_ASSETS}/apple_golden_60x60px.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self, obstacle):
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

P1 = Player()
obstacle = Obstacle()

apples = pygame.sprite.Group()
# Create a grid of apples
apple_grid = []
for y in range(APPLES_IN_COL):
    for x in range(APPLES_IN_ROW):
        apple_x = int((x / APPLES_IN_ROW) * SCREEN_WIDTH) + 30
        apple_y = int((y / APPLES_IN_COL) * SCREEN_HEIGHT) + 30
        print(apple_x, apple_y)
        apple = Apple((apple_x, apple_y))
        apple_grid.append(apple)
apples.add(apple_grid)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    surface.fill((255, 255, 255))

    scores = font_small.render(f"Score: {TOTAL_SCORE}", True, (0, 0, 0))
    surface.blit(scores, (10, 10))

    surface.blit(obstacle.image, obstacle.rect)

    for apple in apples:
        surface.blit(apple.image, apple.rect)

    collided_apple = pygame.sprite.spritecollideany(P1, apples)
    if collided_apple:
        TOTAL_SCORE += 1
        collided_apple.kill()



    surface.blit(P1.image, P1.rect)
    P1.move(obstacle)

    pygame.display.update()
    clock.tick(FPS)



