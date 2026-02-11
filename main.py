import pygame
import random

pygame.init()

# --- Constants ---
GRID_SIZE = 4
CELL_SIZE = 100
BUFFER = CELL_SIZE // 2  # Half-square buffer
LASER_THICKNESS = CELL_SIZE // 4
WINDOW_SIZE = GRID_SIZE * CELL_SIZE + BUFFER * 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 255)
RED = (255, 50, 50)
GRAY = (200, 200, 200)

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Laser Grid Dodge")

clock = pygame.time.Clock()


# --- Square Class ---
class Square:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = BUFFER + col * CELL_SIZE
        self.y = BUFFER + row * CELL_SIZE
        self.rect = pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect, 2)


# --- Player Class ---
class Player:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.update_position()

    def update_position(self):
        self.x = BUFFER + self.col * CELL_SIZE
        self.y = BUFFER + self.row * CELL_SIZE
        self.rect = pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE)

    def move(self, dr, dc):
        self.row = max(0, min(GRID_SIZE - 1, self.row + dr))
        self.col = max(0, min(GRID_SIZE - 1, self.col + dc))
        self.update_position()

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)


# --- Laser Class ---
class Laser:
    def __init__(self):
        self.direction = random.choice(["row", "col"])
        self.index = random.randint(0, GRID_SIZE - 1)
        self.length = 0
        self.speed = CELL_SIZE / 50  # Half-square growth
        self.finished = False
        self.timer = 0

    def update(self):
        if not self.finished:
            self.length += self.speed
            if self.length >= WINDOW_SIZE:
                self.length = WINDOW_SIZE
                self.finished = True
        else:
            self.timer += 1

    def draw(self):
        if self.direction == "row":
            y = BUFFER + self.index * CELL_SIZE + CELL_SIZE // 2 - LASER_THICKNESS // 2
            rect = pygame.Rect(0, y, self.length, LASER_THICKNESS)
        else:
            x = BUFFER + self.index * CELL_SIZE + CELL_SIZE // 2 - LASER_THICKNESS // 2
            rect = pygame.Rect(x, 0, LASER_THICKNESS, self.length)

        pygame.draw.rect(screen, RED, rect)
        return rect


# --- Create Grid ---
grid = []
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        grid.append(Square(row, col))

player = Player()
lasers = []

laser_spawn_timer = 0
laser_spawn_delay = 60
max_active_lasers = random.randint(3, 4)

running = True
alive = True

# --- Game Loop ---
while running:
    clock.tick(60)
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and alive:
            if event.key == pygame.K_UP:
                player.move(-1, 0)
            if event.key == pygame.K_DOWN:
                player.move(1, 0)
            if event.key == pygame.K_LEFT:
                player.move(0, -1)
            if event.key == pygame.K_RIGHT:
                player.move(0, 1)

    # --- Spawn Lasers ---
    laser_spawn_timer += 1

    if laser_spawn_timer >= laser_spawn_delay and len(lasers) < max_active_lasers:
        lasers.append(Laser())
        laser_spawn_timer = 0

    if len(lasers) == 0:
        max_active_lasers = random.randint(2, 3)

    # --- Update & Draw Grid ---
    for square in grid:
        square.draw()

    # --- Update & Draw Player ---
    if alive:
        player.draw()

    # --- Update & Draw Lasers ---
    for laser in lasers[:]:
        laser.update()
        laser_rect = laser.draw()

        if alive and laser_rect.colliderect(player.rect):
            alive = False
            print("Game Over!")

        # Remove laser after 1 second (60 frames)
        if laser.finished and laser.timer > 60:
            lasers.remove(laser)

    pygame.display.flip()

pygame.quit()
