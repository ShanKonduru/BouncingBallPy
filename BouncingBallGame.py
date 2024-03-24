import pygame
import random
from consts import constants

class BouncingBallGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Create screen
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption('Bouncing Ball Game')

        # Clock for controlling FPS
        self.clock = pygame.time.Clock()

        # Brick parameters
        self.BRICK_WIDTH = 80
        self.BRICK_HEIGHT = 30
        self.BRICK_ROWS = 5
        self.BRICK_COLS = 10
        self.BRICK_GAP = 10

        # Paddle parameters
        self.PADDLE_WIDTH = 150
        self.PADDLE_HEIGHT = 20
        self.PADDLE_SPEED = 10

        # Ball parameters
        self.BALL_RADIUS = 10
        self.BALL_SPEED_X = 5
        self.BALL_SPEED_Y = 5

        # Initialize variables
        self.score = 0
        self.highest_score = 0
        self.player_name = ""

        # Initialize game entities
        self.bricks = self.create_bricks()
        self.paddle = pygame.Rect(constants.SCREEN_WIDTH // 2 - self.PADDLE_WIDTH // 2, constants.SCREEN_HEIGHT - self.PADDLE_HEIGHT - 10, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.ball = pygame.Rect(constants.SCREEN_WIDTH // 2 - self.BALL_RADIUS, constants.SCREEN_HEIGHT // 2 - self.BALL_RADIUS, self.BALL_RADIUS * 2, self.BALL_RADIUS * 2)
        self.ball_speed_x = self.BALL_SPEED_X * random.choice([-1, 1])
        self.ball_speed_y = self.BALL_SPEED_Y * random.choice([-1, 1])

    def create_bricks(self):
        bricks = []
        for row in range(self.BRICK_ROWS):
            for col in range(self.BRICK_COLS):
                brick = pygame.Rect(
                    col * (self.BRICK_WIDTH + self.BRICK_GAP) + self.BRICK_GAP,
                    row * (self.BRICK_HEIGHT + self.BRICK_GAP) + self.BRICK_GAP + 50,
                    self.BRICK_WIDTH,
                    self.BRICK_HEIGHT
                )
                bricks.append(brick)
        return bricks

    def move_paddle(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.paddle.left > 0:
            self.paddle.left -= self.PADDLE_SPEED
        if keys[pygame.K_RIGHT] and self.paddle.right < constants.SCREEN_WIDTH:
            self.paddle.right += self.PADDLE_SPEED

    def move_ball(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        # Collision with walls
        if self.ball.left <= 0 or self.ball.right >= constants.SCREEN_WIDTH:
            self.ball_speed_x *= -1
        if self.ball.top <= 0:
            self.ball_speed_y *= -1

        # Collision with paddle
        if self.ball.colliderect(self.paddle) and self.ball_speed_y > 0:
            self.ball_speed_y *= -1

        # Collision with bricks
        for brick in self.bricks[:]:
            if self.ball.colliderect(brick):
                self.bricks.remove(brick)
                self.ball_speed_y *= -1
                self.score += 10

        # Check game over
        if self.ball.top > constants.SCREEN_HEIGHT:
            self.game_over()

    def game_over(self):
        if self.score > self.highest_score:
            self.highest_score = self.score
            self.player_name = input("Enter your name: ")
        self.score = 0
        self.ball_speed_x = self.BALL_SPEED_X * random.choice([-1, 1])
        self.ball_speed_y = self.BALL_SPEED_Y * random.choice([-1, 1])
        self.ball.x = constants.SCREEN_WIDTH // 2 - self.BALL_RADIUS
        self.ball.y = constants.SCREEN_HEIGHT // 2 - self.BALL_RADIUS
        self.bricks = self.create_bricks()

    def draw(self):
        self.screen.fill(constants.WHITE)

        # Draw bricks
        for brick in self.bricks:
            pygame.draw.rect(self.screen, constants.BLUE, brick)

        # Draw paddle
        pygame.draw.rect(self.screen, constants.RED, self.paddle)

        # Draw ball
        pygame.draw.circle(self.screen, constants.RED, (self.ball.x + self.BALL_RADIUS, self.ball.y + self.BALL_RADIUS), self.BALL_RADIUS)

        # Draw scores
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, constants.RED)
        highest_score_text = font.render(f"Highest Score: {self.highest_score} ({self.player_name})", True, constants.RED)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(highest_score_text, (constants.SCREEN_WIDTH - highest_score_text.get_width() - 10, 10))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.move_paddle()
            self.move_ball()
            self.draw()

            self.clock.tick(60)

        pygame.quit()
