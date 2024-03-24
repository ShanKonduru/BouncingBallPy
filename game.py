import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bouncing Ball Game')

# Clock for controlling FPS
clock = pygame.time.Clock()

# Brick parameters
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_GAP = 10

# Paddle parameters
PADDLE_WIDTH = 150
PADDLE_HEIGHT = 20
PADDLE_SPEED = 10

# Ball parameters
BALL_RADIUS = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Initialize variables
score = 0
highest_score = 0
player_name = ""

# Create bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(
            col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP,
            row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_GAP + 50,
            BRICK_WIDTH,
            BRICK_HEIGHT
        )
        bricks.append(brick)

# Create paddle
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create ball
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = BALL_SPEED_X * random.choice([-1, 1])
ball_speed_y = BALL_SPEED_Y * random.choice([-1, 1])

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.right += PADDLE_SPEED

    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Collision with walls
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1

    # Collision with paddle
    if ball.colliderect(paddle) and ball_speed_y > 0:
        ball_speed_y *= -1

    # Collision with bricks
    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y *= -1
            score += 10

    # Check game over
    if ball.top > SCREEN_HEIGHT:
        if score > highest_score:
            highest_score = score
            player_name = input("Enter your name: ")
        score = 0
        ball_speed_x = BALL_SPEED_X * random.choice([-1, 1])
        ball_speed_y = BALL_SPEED_Y * random.choice([-1, 1])
        ball.x = SCREEN_WIDTH // 2 - BALL_RADIUS
        ball.y = SCREEN_HEIGHT // 2 - BALL_RADIUS
        bricks = [pygame.Rect(
            col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP,
            row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_GAP + 50,
            BRICK_WIDTH,
            BRICK_HEIGHT
        ) for row in range(BRICK_ROWS) for col in range(BRICK_COLS)]

    # Draw bricks
    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)

    # Draw paddle
    pygame.draw.rect(screen, RED, paddle)

    # Draw ball
    pygame.draw.circle(screen, RED, (ball.x + BALL_RADIUS, ball.y + BALL_RADIUS), BALL_RADIUS)

    # Draw scores
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, RED)
    highest_score_text = font.render(f"Highest Score: {highest_score} ({player_name})", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(highest_score_text, (SCREEN_WIDTH - highest_score_text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
