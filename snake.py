import pygame
import pygame.event
import random

pygame.init()

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200

surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake")

TEXT_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SNAKE_BODY_COLOR = (255, 165, 0)
SNAKE_SIZE = 20
APPLE_COLOR = (255, 0, 0)
APPLE_SIZE = 20
BLACK = (0, 0, 0)

FPS = 5
clock = pygame.time.Clock()
score = 0

font = pygame.font.SysFont("gabriola", 32)

score_text = font.render("Score: " + str(score), True, TEXT_COLOR)
score_text_rect = score_text.get_rect()
score_text_rect.left = 5

game_over_text = font.render("Game Over! Press space to continue", True, TEXT_COLOR)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

head_x = WINDOW_WIDTH//2
head_y = WINDOW_HEIGHT//2
snake_dx = 0
snake_dy = 0

body_coords = []

head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect = pygame.draw.rect(surface, SNAKE_COLOR, head_coord)

apple_coord = (120, 120, APPLE_SIZE, APPLE_SIZE)
apple_rect = pygame.draw.rect(surface, APPLE_COLOR, apple_coord)

pick_sound = pygame.mixer.Sound("pick.wav")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_dx = -1 * SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_RIGHT:
                snake_dx = SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_UP:
                snake_dx = 0
                snake_dy = -1 * SNAKE_SIZE
            if event.key == pygame.K_DOWN:
                snake_dx = 0
                snake_dy = SNAKE_SIZE

    # simula o movimento da cobra, sempre inserindo a posição atual e removendo a última
    body_coords.insert(0, head_coord)
    body_coords.pop()

    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

    game_over = False

    if head_x < 0 or head_x == WINDOW_WIDTH:
        game_over = True
    if head_y < 40 or head_y == WINDOW_HEIGHT:
        game_over = True
    if head_coord in body_coords:
        game_over = True

    if head_rect.colliderect(apple_rect):
        pick_sound.play()
        score += 1
        body_coords.append(head_coord)
        apple_x = random.randint(0, WINDOW_WIDTH - SNAKE_SIZE)
        diff = apple_x % SNAKE_SIZE
        if diff != 0:
            apple_x -= diff        
        apple_y = random.randint(40, WINDOW_HEIGHT - SNAKE_SIZE)
        diff = apple_y % SNAKE_SIZE
        if diff != 0:
            apple_y -= diff
        while (apple_x, apple_y) in body_coords:
            print('renderizou no corpo, tentando nova posição')
            apple_x = random.randint(0, WINDOW_WIDTH - SNAKE_SIZE)
            diff = apple_x % SNAKE_SIZE
            if diff != 0:
                apple_x -= diff        
            apple_y = random.randint(40, WINDOW_HEIGHT - SNAKE_SIZE)
            diff = apple_y % SNAKE_SIZE
            if diff != 0:
                apple_y -= diff

        apple_coord = (apple_x, apple_y, APPLE_SIZE, APPLE_SIZE)   

    if game_over:
        surface.blit(game_over_text, game_over_rect)
        pygame.display.update()
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_over = False
                        score = 0
                        head_x = WINDOW_WIDTH//2
                        head_y = WINDOW_HEIGHT//2
                        snake_dx = 0
                        snake_dy = 0
                        body_coords = []
            pygame.display.update()

    surface.fill((255, 255, 255))
    surface.blit(score_text, score_text_rect)

    for body in body_coords:
        pygame.draw.rect(surface, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), body)
    
    score_text = font.render("Score: " + str(score), True, TEXT_COLOR)        

    head_rect = pygame.draw.rect(surface, SNAKE_COLOR, head_coord)
    apple_rect = pygame.draw.rect(surface, APPLE_COLOR, apple_coord)

    pygame.draw.line(surface, BLACK, (0, 40), (WINDOW_WIDTH, 40), 1)


    clock.tick(FPS)
    pygame.display.update()
