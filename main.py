import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 21, 25
TILE_SIZE = 32
SCREEN_WIDTH = WIDTH * TILE_SIZE // 2
SCREEN_HEIGHT = HEIGHT * TILE_SIZE // 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Tile:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.original_color = color
        self.hitbox = None
        if self.color == BLUE:
            self.hitbox = pygame.Rect(self.col * TILE_SIZE, self.row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.col * TILE_SIZE // 2, self.row * TILE_SIZE // 2, TILE_SIZE // 2, TILE_SIZE // 2))

    def toggle_color(self):
        if self.color == BLUE:
            self.color = self.original_color
            self.hitbox = None
        else:
            self.color = BLUE
            self.hitbox = pygame.Rect(self.col * TILE_SIZE, self.row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = GREEN
        self.radius = TILE_SIZE // 2
        self.hitbox_size = TILE_SIZE // 2
        self.hitbox = pygame.Rect(self.x - self.hitbox_size // 3, self.y - self.hitbox_size // 3, self.hitbox_size, self.hitbox_size)
        self.angle = 0
        self.speed = 20
        self.paused = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x // 2, self.y // 2), self.radius // 2)

    def move(self):
        if not self.paused:
            dx = self.speed * math.cos(math.radians(self.angle))
            dy = -self.speed * math.sin(math.radians(self.angle))
            self.x += dx
            self.y += dy
            self.hitbox.x = self.x - self.hitbox_size // 2
            self.hitbox.y = self.y - self.hitbox_size // 2

    def bounce(self, axis):
        if axis == 'x':
            self.angle = 180 - self.angle
        elif axis == 'y':
            self.angle = -self.angle

    def toggle_pause(self):
        self.paused = not self.paused

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Checkered Grid")
        self.font = pygame.font.Font(None, 12)
        self.reset()
        self.last_key_press_time = None
        self.key_held = None

    def reset(self):
        self.grid = [[Tile(row, col, WHITE if (row + col) % 2 == 0 else BLACK) for col in range(WIDTH)] for row in range(HEIGHT)]
        self.ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.get_angle()

    def get_angle(self):
        angle = input("Enter angle (1-360): ")
        try:
            self.ball.angle = int(angle)
        except ValueError:
            print("Invalid angle")
            self.get_angle()

    def draw_grid(self):
        for row in range(HEIGHT):
            for col in range(WIDTH):
                self.grid[row][col].draw(self.screen)
        self.ball.draw(self.screen)

    def handle_collisions(self):
        if self.ball.hitbox.left <= 0 or self.ball.hitbox.right >= SCREEN_WIDTH * 2:
            self.ball.bounce('x')
        if self.ball.hitbox.top <= 0 or self.ball.hitbox.bottom >= SCREEN_HEIGHT * 2:
            self.ball.bounce('y')
        for row in range(HEIGHT):
            for col in range(WIDTH):
                tile = self.grid[row][col]
                if tile.hitbox and self.ball.hitbox.colliderect(tile.hitbox):
                    self.ball.bounce('x' if abs(self.ball.hitbox.centerx - tile.hitbox.centerx) > abs(self.ball.hitbox.centery - tile.hitbox.centery) else 'y')

    def draw_speed(self):
        speed_text = self.font.render(f"Speed: {self.ball.speed * 60:.2f} px/s", True, RED)
        self.screen.blit(speed_text, (10, 10))

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col = (x * 2) // TILE_SIZE
                    row = (y * 2) // TILE_SIZE
                    if event.button == 3:  # Right click
                        self.grid[row][col].toggle_color()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.reset()
                    elif event.key == pygame.K_SPACE:
                        self.ball.toggle_pause()

            self.ball.move()
            self.handle_collisions()
            self.draw_grid()
            self.draw_speed()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
