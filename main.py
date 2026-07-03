import pygame
import sys
import random

pygame.init()

width, height = 600, 600
size = 20

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# color palette

background = (255, 234, 244)
grid = (245, 220, 235)
snake_head = (255, 111, 174)
snake_body = (255, 154, 207)
FOOD = (255, 77, 109)
text = (180, 90, 140)

def food_treats():
    x = random.randrange(0, width, size)
    y = random.randrange(0, height, size)
    return (x, y)

def reset():
    snake = [(300, 300), (280, 300), (260, 300)]
    direction = (size, 0)
    food = food_treats()
    score = 0
    speed = 10
    return snake, direction, food, score, speed

snake, direction, food, score, speed = reset()
game_over = False

def draw_grid():
    for x in range(0, width, size):
        pygame.draw.line(screen, grid, (x, 0), (x, height))
    for y in range(0, height, size):
        pygame.draw.line(screen, grid, (0, y), (width, y))

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False
            
            if not game_over:
                if event.key == pygame.K_UP and direction != (0, size):
                    direction = (0, -size)
                elif event.key == pygame.K_DOWN and direction != (0, -size):
                    direction = (0, size)
                elif event.key == pygame.K_LEFT and direction != (size, 0):
                    direction = (-size, 0)
                elif event.key == pygame.K_RIGHT and direction != (-size, 0):
                    direction = (size, 0)

            elif game_over and event.key == pygame.K_RETURN:
                snake, direction, food, score, speed = reset() 
                game_over = False

    if not game_over:
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # wall 
        if (new_head[0] < 0 or new_head[0] >= width or
            new_head[1] < 0 or new_head[1] >= height):
            game_over = True

        snake.insert(0, new_head)

        # self
        if new_head in snake[1:]:
            game_over = True

        # food spawn
        if new_head == food:
            food = food_treats()
            score += 1
            if score % 3 == 0:
                speed += 1
        
        else:
            snake.pop()

        # background

        screen.fill(background)
        draw_grid()

        pygame.draw.rect(screen, FOOD, (food[0], food[1], size, size), border_radius=6)

        for i, segment in enumerate(snake):
            color = snake_head if i == 0 else snake_body
            pygame.draw.rect(
                screen,
                color,
                (segment[0], segment[1], size, size),
                border_radius=8
            )

        score_text = font.render(f"Score: {score}", True, text)
        screen.blit(score_text, (10, 10))

        if game_over:
            over_text = font.render("Game Over! Press ENTER", True, text)
            screen.blit(over_text, (120, 280))

        
        pygame.display.flip()
        clock.tick(speed)

pygame.quit()
sys.exit()

