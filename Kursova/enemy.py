import random
from bullet import BossBullet
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, level, all_sprites, boss_bullets):
        super(Enemy, self).__init__()
        self.image = pygame.transform.scale(ENEMY_IMG, (40, 40))
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.level = level
        self.speed_y = random.randint(1, 2 + level)
        self.speed_x = random.choice([-1, 1]) * (1 + level / 2)
        self.all_sprites = all_sprites
        self.boss_bullets = boss_bullets
        self.change_direction_time = random.randint(100, 200)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        if self.rect.left > self.screen_width:
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(-100, -40)
        elif self.rect.right < 0:
            self.rect.x = self.screen_width
            self.rect.y = random.randint(-100, -40)

        if self.rect.top > self.screen_height + 10:
            self.rect.x = random.randint(0, self.screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 2 + self.level)
            self.speed_x = random.choice([-1, 1]) * (1 + self.level / 2)

        if self.change_direction_time <= 0:
            self.speed_x *= -1
            self.change_direction_time = random.randint(100, 200)
        self.change_direction_time -= 1


class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, level, all_sprites, boss_bullets):
        super(BossEnemy, self).__init__()
        self.image = pygame.transform.scale(BOSS_IMG, (80, 80))
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect.x = screen_width // 2 - self.rect.width // 2
        self.rect.y = -self.rect.height
        self.speed_y = 1
        self.max_health = 50 + level * 10
        self.health = self.max_health
        self.direction = 1
        self.last_shot_time = 0
        self.shoot_cooldown = 2000
        self.all_sprites = all_sprites
        self.boss_bullets = boss_bullets

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > 20:
            self.speed_y = 0

        self.rect.x += self.direction * 2

        if self.rect.right >= self.screen_width:
            self.direction = -1
        elif self.rect.left <= 0:
            self.direction = 1

        self.shoot()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_cooldown:
            boss_bullet = BossBullet(self.rect.centerx, self.rect.bottom)
            self.all_sprites.add(boss_bullet)
            self.boss_bullets.add(boss_bullet)
            self.last_shot_time = current_time

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def draw_health_bar(self, surface):
        if self.health > 0:
            bar_length = 100
            bar_height = 10
            fill = (self.health / self.max_health) * bar_length
            outline_rect = pygame.Rect(self.rect.centerx - bar_length // 2, self.rect.top - 20, bar_length, bar_height)
            fill_rect = pygame.Rect(self.rect.centerx - bar_length // 2, self.rect.top - 20, fill, bar_height)
            pygame.draw.rect(surface, pygame.Color('red'), outline_rect)
            pygame.draw.rect(surface, pygame.Color('green'), fill_rect)