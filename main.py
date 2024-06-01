import pygame
import sys
from random import randint, choice

# Pygame-ის ინიციალიზაცია
pygame.init()

# ფანჯრის არეალის დაყენება
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

GREEN = (50, 209, 93)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Test Pygame")
pygame.display.set_icon(pygame.image.load("title_image.png"))
background = pygame.image.load("back.png")
player = pygame.image.load("player.png")

enemy = pygame.image.load("enemy.png")
coin = pygame.image.load("coin.png")


class Enemy:
    def __init__(self, enemy_type):
        self.enemy_type = enemy_type

        if self.enemy_type == "enemy":
            self.image = pygame.image.load("enemy.png")
        else:
            self.image = pygame.image.load("coin.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = randint(0, WINDOW_WIDTH - self.width)
        self.y = randint(0, WINDOW_HEIGHT - self.height)
        self.speed = choice([2, 3, 4])
        self.touch = False

    def move(self):
        self.x += self.speed
        if self.x > WINDOW_WIDTH:
            self.x = -self.width
            self.y = randint(0, WINDOW_HEIGHT - self.height)
            self.touch = False

    def draw(self):
        window.blit(self.image, (self.x, self.y))


# მტრების შექმნა
enemies = [Enemy("enemy") for _ in range(3)]
enemies.extend([Enemy("coin") for _ in range(4)])

# მოთამაშის აღწერა
player_width = 50
player_height = 50
player_x = 250
player_y = 350
player_speed = 5

score = 0

# თამაშის ციკლი
running = True
game_over = False

while running:
    # ფონის გამოტანა
    window.blit(background, (0, 0))

    # მოვლენების დამუშავება
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ყველა კლავიატურის კლავიშის მდგომარეობის მიღება
    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WINDOW_WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < WINDOW_HEIGHT - player_height:
            player_y += player_speed

        # მტრების გამოჩენა ეკრანზე
        for enemy in enemies:
            enemy.move()
            enemy.draw()


            # მოთამაშის და მტრების შეხება
            if player_x < enemy.x + enemy.width and player_x + player_width > enemy.x \
                    and player_y < enemy.y + enemy.height and player_y + player_height > enemy.y:
                if enemy.enemy_type == "enemy":
                    game_over = True
                if enemy.enemy_type == "coin" and not enemy.touch:  # ქულის სპრაიტზე შეხებისას ქულა ჩაითვალოს მხოლოდ ერთხელ
                    score += 1
                    enemy.touch = True
    else:
        # თამაშის წაგება
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, RED)
        window.blit(text, (250, 250))

    # ქულის გამოჩენა
    font = pygame.font.Font(None, 30)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(text, (10, 10))

    # მოთამაშის გამოჩენა ეკრანზე
    window.blit(player, (player_x, player_y))

    # ეკრანის გნახლება
    pygame.display.update()

    # კადრები სიჩქარის შეზღუდვა
    pygame.time.Clock().tick(120)

pygame.quit()
sys.exit()
