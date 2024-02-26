#ver1
import pygame
import random
import math

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Змейка")

black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)

block_size = 20
snake_speed = 30

font = pygame.font.SysFont(None, 50)
text_surface = font.render("Выход - Q___Повтор - R", True, white)
text_rect = text_surface.get_rect()
text_rect.center = (width // 2, height // 2)

def draw_snake(snake_body):
    for block in snake_body:
        pygame.draw.rect(window, green, [block[0], block[1], block_size, block_size])

def draw_apple(apple_pos):
    pygame.draw.rect(window, red, [apple_pos[0], apple_pos[1], block_size, block_size])

def generate_apple(snake_body):
    while True:
        apple_pos = [random.randrange(1, width // block_size) * block_size,
                     random.randrange(1, height // block_size) * block_size]
        if apple_pos not in snake_body:
            return apple_pos

def get_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def find_safe_direction(snake_head, snake_body, apple_pos):
    directions = [(block_size, 0), (-block_size, 0), (0, block_size), (0, -block_size)]
    safe_directions = []
    for direction in directions:
        new_head = [snake_head[0] + direction[0], snake_head[1] + direction[1]]
        if new_head not in snake_body and 0 <= new_head[0] < width and 0 <= new_head[1] < height:
            safe_directions.append(direction)
    if safe_directions:
        if len(safe_directions) > 1:
            safe_directions.sort(key=lambda direction: get_distance([snake_head[0] + direction[0], snake_head[1] + direction[1]], apple_pos))
        return safe_directions[0]
    else:
        return (0, 0)

def find_empty_space(snake_head, snake_body):
    directions = [(block_size, 0), (-block_size, 0), (0, block_size), (0, -block_size)]
    empty_spaces = []
    for direction in directions:
        new_head = [snake_head[0] + direction[0], snake_head[1] + direction[1]]
        if new_head not in snake_body and 0 <= new_head[0] < width and 0 <= new_head[1] < height:
            empty_spaces.append(new_head)
    return empty_spaces

def find_path(start, goal, snake_body):
    open_set = [start]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: get_distance(start, goal)}

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        open_set.remove(current)

        for direction in [(block_size, 0), (-block_size, 0), (0, block_size), (0, -block_size)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if neighbor[0] < 0 or neighbor[0] >= width or neighbor[1] < 0 or neighbor[1] >= height:
                continue
            if neighbor in snake_body:
                continue

            tentative_g_score = g_score[current] + get_distance(current, neighbor)

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + get_distance(neighbor, goal)
                if neighbor not in open_set:
                    open_set.append(neighbor)

    return None

def game_loop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_body = []
    length_of_snake = 1

    apple_pos = generate_apple(snake_body)

    while not game_over:
        while game_close:
            window.fill(black)
            window.blit(text_surface, text_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if len(snake_body) < (width // block_size) * (height // block_size) // 4:
            direction = find_safe_direction([x1, y1], snake_body, apple_pos)
            x1_change, y1_change = direction
        else:
            empty_spaces = find_empty_space([x1, y1], snake_body)
            if empty_spaces:
                empty_spaces.sort(key=lambda space: get_distance(space, apple_pos))
                goal = empty_spaces[0]
            else:
                goal = apple_pos

            path = find_path((x1, y1), goal, snake_body)

            if path:
                next_node = path[1]
                x1_change = next_node[0] - x1
                y1_change = next_node[1] - y1

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        window.fill(black)
        draw_apple(apple_pos)

        snake_head = [x1, y1]
        snake_body.append(snake_head)

        if len(snake_body) > length_of_snake:
            del snake_body[0]

        for block in snake_body[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_body)
        pygame.display.update()

        if snake_head == apple_pos:
            apple_pos = generate_apple(snake_body)
            length_of_snake += 1

        pygame.time.Clock().tick(snake_speed)

    pygame.quit()

game_loop()


