import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My first Game")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game objects
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)  # You can change the color as needed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PacMan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the image
        self.original_image = pygame.image.load("pacman.png").convert_alpha()
        # Scale the image if needed (adjust the size as necessary)
        self.original_image = pygame.transform.scale(self.original_image, (40, 40))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = 285
        self.rect.y = 285
        self.speed = 5
        self.direction = [0, 0]

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction[0] *= 0
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.direction[1] *= 0

class Ghost(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.original_image = pygame.image.load("pacman_ghost.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (40, 40))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(0, HEIGHT - 30)
        self.speed = 3
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction[0] *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.direction[1] *= -1

class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprite groups
all_sprites = pygame.sprite.Group()
ghosts = pygame.sprite.Group()
pellets = pygame.sprite.Group()

# Create Pac-Man
pacman = PacMan()
all_sprites.add(pacman)

# Create Ghosts
for _ in range(6):
    ghost = Ghost(RED)
    all_sprites.add(ghost)
    ghosts.add(ghost)

# Create Pellets
for _ in range(75):
    x = random.randint(0, WIDTH - 10)
    y = random.randint(0, HEIGHT - 10)
    pellet = Pellet(x, y)
    all_sprites.add(pellet)
    pellets.add(pellet)

# Game variables
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.direction = [-1, 0]
            elif event.key == pygame.K_RIGHT:
                pacman.direction = [1, 0]
            elif event.key == pygame.K_UP:
                pacman.direction = [0, -1]
            elif event.key == pygame.K_DOWN:
                pacman.direction = [0, 1]

    # Update
    all_sprites.update()

    # Check for pellet collection
    pellets_collected = pygame.sprite.spritecollide(pacman, pellets, True)
    score += len(pellets_collected)

    # Check for ghost collision
    if pygame.sprite.spritecollide(pacman, ghosts, False):
        running = False

    # Draw
    window.fill(BLACK)
    all_sprites.draw(window)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Game over
pygame.quit()
