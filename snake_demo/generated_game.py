```python
import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Colors
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Player
player_x = 370
player_y = 480
player_width = 50
player_height = 60
player_speed = 5

# Enemy
enemy_x = random.randint(0, screen_width - 40)
enemy_y = random.randint(50, 150)
enemy_radius = 25
enemy_speed = 3

# Bullet
bullet_x = 0
bullet_y = 480
bullet_width = 10
bullet_height = 20
bullet_speed = 10
bullet_state = "ready"

# Game loop
running = True
clock = pygame.time.Clock() # Create a clock object
while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y
                bullet_state = "fire"

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Enemy movement
    enemy_y += enemy_speed
    if enemy_y > screen_height:
        enemy_x = random.randint(0, screen_width - 40)
        enemy_y = random.randint(50, 150)

    # Bullet movement
    if bullet_state == "fire":
        bullet_y -= bullet_speed
        if bullet_y <= 0:
            bullet_state = "ready"

    # Collision detection
    distance = math.sqrt((enemy_x + enemy_radius - (bullet_x + bullet_width // 2))**2 + (enemy_y + enemy_radius - (bullet_y + bullet_height // 2))**2)
    if bullet_state == "fire" and distance <= enemy_radius + bullet_width//2:
        enemy_x = random.randint(0, screen_width - 40)
        enemy_y = random.randint(50, 150)
        bullet_state = "ready"


    # Draw objects
    pygame.draw.rect(screen, blue, (player_x, player_y, player_width, player_height))
    pygame.draw.circle(screen, red, (enemy_x + enemy_radius, enemy_y + enemy_radius), enemy_radius)
    if bullet_state == "fire":
        pygame.draw.rect(screen, green, (bullet_x, bullet_y, bullet_width, bullet_height))

    pygame.display.update()
    clock.tick(60) # added FPS limiter

pygame.quit()
```