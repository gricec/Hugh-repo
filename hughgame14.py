import pygame
import random
import time

pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("WASD Movement Example")

# Player attributes
player_width, player_height = 50, 50
player_x, player_y = (screen_width - player_width) // 2, (screen_height - player_height) // 2
base_speed = 0.5
speed_multiplier = 0
player_speed = base_speed

# Coin attributes
coin_size = 30
coin_x = random.randint(coin_size, screen_width - coin_size)
coin_y = random.randint(coin_size, screen_height - coin_size)

# Special Coin attributes
special_coin_size = 30
special_coin_x = random.randint(special_coin_size, screen_width - special_coin_size)
special_coin_y = random.randint(special_coin_size, screen_height - special_coin_size)

# Wall attributes
wall_thickness = 10

# Wall positions
top_wall = pygame.Rect(0, 0, screen_width, wall_thickness)
bottom_wall = pygame.Rect(0, screen_height - wall_thickness, screen_width, wall_thickness)

# Score attributes
score = 0
font = pygame.font.Font(None, 36)

# Timer attributes
start_time = time.time()
game_duration = 120  # 2 minutes in seconds

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of the keyboard
    keys = pygame.key.get_pressed()

    # Update player position based on key input
    if keys[pygame.K_w] and player_y > wall_thickness:
        player_y -= player_speed
    if keys[pygame.K_s] and player_y < screen_height - player_height - wall_thickness:
        player_y += player_speed
    if keys[pygame.K_a] and player_x > wall_thickness:
        player_x -= player_speed
    if keys[pygame.K_d] and player_x < screen_width - player_width - wall_thickness:
        player_x += player_speed

    # Check for collision between player and coin
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)
    if player_rect.colliderect(coin_rect):
        # If player and coin collide, generate new coin position and increment score
        coin_x = random.randint(coin_size, screen_width - coin_size)
        coin_y = random.randint(coin_size, screen_height - coin_size)
        score += 1

    # Check for collision between player and special coin
    special_coin_rect = pygame.Rect(special_coin_x, special_coin_y, special_coin_size, special_coin_size)
    if player_rect.colliderect(special_coin_rect):
        # If player and special coin collide, generate new special coin position and deduct 3 from the score
        special_coin_x = random.randint(special_coin_size, screen_width - special_coin_size)
        special_coin_y = random.randint(special_coin_size, screen_height - special_coin_size)
        score = max(0, score - 3)

    # Draw the player, coin, special coin, walls, scoreboard, and update the display
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, (255, 255, 0), (coin_x, coin_y, coin_size, coin_size))
    pygame.draw.rect(screen, (0, 0, 255), (special_coin_x, special_coin_y, special_coin_size, special_coin_size))
    pygame.draw.rect(screen, (0, 255, 0), top_wall)
    pygame.draw.rect(screen, (0, 255, 0), bottom_wall)

    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Calculate the remaining time
    elapsed_time = int(time.time() - start_time)
    remaining_time = max(0, game_duration - elapsed_time)
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
    screen.blit(time_text, (10, 50))

    pygame.display.flip()

    # Check if the speed multiplier key is pressed (e.g., Left Shift)
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        player_speed = base_speed * speed_multiplier
    else:
        player_speed = base_speed

    # End the game if the score reaches 25 or the time runs out
    if score >= 25 or remaining_time <= 0:
        running = False

# Quit the game
pygame.quit()

