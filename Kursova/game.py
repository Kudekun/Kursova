from enemy import Enemy, BossEnemy
from explosion import Explosion
from player import Player
from settings import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kudekun`s Game")

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()

player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
all_sprites.add(player)


def create_enemies(level):
    for i in range(5 + level * 1):
        enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, level, all_sprites, boss_bullets)
        all_sprites.add(enemy)
        enemies.add(enemy)

    if level % 3 == 0:
        boss = BossEnemy(SCREEN_WIDTH, SCREEN_HEIGHT, level, all_sprites, boss_bullets)
        all_sprites.add(boss)
        enemies.add(boss)


level = 1
create_enemies(level)
score = 0
font = pygame.font.Font(None, 36)


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def show_level_start(level):
    screen.fill(BLACK)
    draw_text(screen, f"Level {level}", 48, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    pygame.display.flip()
    pygame.time.wait(2000)


def show_game_over(score):
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 48, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
    draw_text(screen, f"Score: {score}", 36, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10)
    pygame.display.flip()
    pygame.time.wait(5000)


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot(all_sprites, bullets)

    all_sprites.update()

    for enemy in enemies:
        hits = pygame.sprite.spritecollide(enemy, bullets, True)
        for bullet in hits:
            if isinstance(enemy, Enemy):
                score += 10
                enemy.kill()
                explosion = Explosion(enemy.rect.center, 40)
                all_sprites.add(explosion)
                explosions.add(explosion)
            elif isinstance(enemy, BossEnemy):
                enemy.hit(10)
                if enemy.health <= 0:
                    score += 50
                    enemy.kill()
                    explosion = Explosion(enemy.rect.center, 80)
                    all_sprites.add(explosion)
                    explosions.add(explosion)

    if not enemies:
        level += 1
        show_level_start(level)
        create_enemies(level)

    enemy_hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in enemy_hits:
        player.lives -= 1
        if player.lives <= 0:
            running = False
        else:
            enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, level, all_sprites, boss_bullets)
            all_sprites.add(enemy)
            enemies.add(enemy)

    boss_bullet_hits = pygame.sprite.spritecollide(player, boss_bullets, True)
    for hit in boss_bullet_hits:
        player.lives -= 1
        if player.lives <= 0:
            running = False

    screen.blit(BACKGROUND_IMG, (0, 0))

    all_sprites.draw(screen)

    for enemy in enemies:
        if isinstance(enemy, BossEnemy):
            enemy.draw_health_bar(screen)

    draw_text(screen, f"Score: {score}", 18, SCREEN_WIDTH / 2, 10)
    draw_text(screen, f"Lives: {player.lives}", 18, SCREEN_WIDTH - 100, 10)
    draw_text(screen, f"Level: {level}", 18, SCREEN_WIDTH - 200, 10)

    pygame.display.flip()

show_game_over(score)

pygame.quit()
