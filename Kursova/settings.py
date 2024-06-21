import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

FPS = 60

PLAYER_IMG = pygame.image.load('assets/player.png')
ENEMY_IMG = pygame.image.load('assets/enemy.png')
BULLET_IMG = pygame.image.load('assets/bullet.png')
EXPLOSION_IMG = pygame.image.load('assets/explosion.png')
BOSS_IMG = pygame.image.load('assets/Boss.png')
BACKGROUND_IMG = pygame.image.load('assets/background.png')
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))
