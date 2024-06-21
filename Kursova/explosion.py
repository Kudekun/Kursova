import pygame
from settings import EXPLOSION_IMG

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super(Explosion, self).__init__()
        self.image = pygame.transform.scale(EXPLOSION_IMG, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 20

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 9:
                self.kill()
