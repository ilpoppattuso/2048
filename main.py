import pygame
import random

pygame.init()

screen_width = 400
screen_height = 500
screen_size = (screen_width, screen_height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("2048")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
light_gray = (200, 200, 200)
tile_colors = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    "other": (119, 110, 101)
}

# Font
font_size = 40
font = pygame.font.Font(None, font_size)
score_font_size = 30
score_font = pygame.font.Font(None, score_font_size)

# Grid size
grid_size = 4
spacing = 10
tile_width = (screen_width - spacing * (grid_size + 1)) // grid_size
tile_height = tile_width

# Game grid
grid = [[0] * grid_size for _ in range(grid_size)]

# Animation settings
animation_speed = 5
moving_tiles = []

# Score
score = 0
high_score = 0


try:
    with open("high_score.txt", "r") as f:
        high_score = int(f.read())
except FileNotFoundError:
    pass

def draw_tile(x, y, value, offset_x=0, offset_y=0):
    color = tile_colors.get(value, tile_colors["other"])
    x_pos = x + offset_x
    y_pos = y + offset_y
    pygame.draw.rect(screen, color, (x_pos, y_pos, tile_width, tile_height))
    if value != 0:
        text = font.render(str(value), True, black)
        text_rect = text.get_rect(center=(x_pos + tile_width // 2, y_pos + tile_height // 2))
        screen.blit(text, text_rect)

# draw the grid
def draw_grid():
    for row in range(grid_size):
        for col in range(grid_size):
            value = grid[row][col]
            x = col * (tile_width + spacing) + spacing
            y = row * (tile_height + spacing) + spacing + 100
            draw_tile(x, y, value)

def add_new_tile():
    empty_cells = [(r, c) for r in range(grid_size) for c in range(grid_size) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = 2 if random.random() < 0.9 else 4

# Function to move tiles
def move(direction):
    global moving_tiles, score
    moved = False
    moving_tiles = []

    if direction == "up":
        for col in range(grid_size):
            for row in range(1, grid_size):
                if grid[row][col] != 0:
                    for r in range(row, 0, -1):
                        if grid[r - 1][col] == 0:

                            moving_tiles.append({
                                "from_row": r,
                                "from_col": col,
                                "to_row": r - 1,
                                "to_col": col,
                                "value": grid[r][col],
                                "progress": 0
                            })
                            grid[r - 1][col] = grid[r][col]
                            grid[r][col] = 0
                            moved = True
                        elif grid[r - 1][col] == grid[r][col]:

                            moving_tiles.append({
                                "from_row": r,
                                "from_col": col,
                                "to_row": r - 1,
                                "to_col": col,
                                "value": grid[r][col],
                                "progress": 0
                            })
                            grid[r - 1][col] *= 2
                            score += grid[r-1][col] # Update score
                            grid[r][col] = 0
                            moved = True
                            break
                        else:
                            break
    elif direction == "down":
        for col in range(grid_size):
            for row in range(grid_size - 2, -1, -1):
                if grid[row][col] != 0:
                    for r in range(row, grid_size - 1):
                        if grid[r + 1][col] == 0:
                            moving_tiles.append({
                                "from_row": r,
                                "from_col": col,
                                "to_row": r + 1,
                                "to_col": col,
                                "value": grid[r][col],
                                "progress": 0
                            })
                            grid[r + 1][col] = grid[r][col]
                            grid[r][col] = 0
                            moved = True
                        elif grid[r + 1][col] == grid[r][col]:
                            moving_tiles.append({
                                "from_row": r,
                                "from_col": col,
                                "to_row": r + 1,
                                "to_col": col,
                                "value": grid[r][col],
                                "progress": 0
                            })
                            grid[r + 1][col] *= 2
                            score += grid[r+1][col] # Update score
                            grid[r][col] = 0
                            moved = True
                            break
                        else:
                            break
    elif direction == "left":
        for row in range(grid_size):
            for col in range(1, grid_size):
                if grid[row][col] != 0:
                    for c in range(col, 0, -1):
                        if grid[row][c - 1] == 0:
                            moving_tiles.append({
                                "from_row": row,
                                "from_col": c,
                                "to_row": row,
                                "to_col": c - 1,
                                "value": grid[row][c],
                                "progress": 0
                            })
                            grid[row][c - 1] = grid[row][c]
                            grid[row][c] = 0
                            moved = True
                        elif grid[row][c - 1] == grid[row][c]:
                            moving_tiles.append({
                                "from_row": row,
                                "from_col": c,
                                "to_row": row,
                                "to_col": c - 1,
                                "value": grid[row][c],
                                "progress": 0
                            })
                            grid[row][c - 1] *= 2
                            score += grid[row][c-1] # Update score
                            grid[row][c] = 0
                            moved = True
                            break
                        else:
                            break
    elif direction == "right":
        for row in range(grid_size):
            for col in range(grid_size - 2, -1, -1):
                if grid[row][col] != 0:
                    for c in range(col, grid_size - 1):
                        if grid[row][c + 1] == 0:
                            moving_tiles.append({
                                "from_row": row,
                                "from_col": c,
                                "to_row": row,
                                "to_col": c + 1,
                                "value": grid[row][c],
                                "progress": 0
                            })
                            grid[row][c + 1] = grid[row][c]
                            grid[row][c] = 0
                            moved = True
                        elif grid[row][c + 1] == grid[row][c]:
                            moving_tiles.append({
                                "from_row": row,
                                "from_col": c,
                                "to_row": row,
                                "to_col": c + 1,
                                "value": grid[row][c],
                                "progress": 0
                            })
                            grid[row][c + 1] *= 2
                            score += grid[row][c+1] # Update score
                            grid[row][c] = 0
                            moved = True
                            break
                        else:
                            break

    if moved:
        # Animate the tiles
        animate_tiles()
        add_new_tile()

# title animation
def animate_tiles():
    global moving_tiles, grid

    # update animation
    for tile in moving_tiles:
        tile["progress"] += animation_speed

    moving_tiles = [tile for tile in moving_tiles if tile["progress"] < 100]

    
    for tile in moving_tiles:
        from_x = tile["from_col"] * (tile_width + spacing) + spacing
        from_y = tile["from_row"] * (tile_height + spacing) + spacing + 100
        to_x = tile["to_col"] * (tile_width + spacing) + spacing
        to_y = tile["to_row"] * (tile_height + spacing) + spacing + 100
        progress = tile["progress"] / 100
        offset_x = (to_x - from_x) * progress
        offset_y = (to_y - from_y) * progress
        draw_tile(from_x, from_y, tile["value"], offset_x, offset_y)




def check_game_state():
    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] == 2048:
                return "You Won!"
    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] == 0:
                return "In Progress"
    for row in range(grid_size):
        for col in range(grid_size - 1):
            if grid[row][col] == grid[row][col + 1]:
                return "In Progress"
    for row in range(grid_size - 1):
        for col in range(grid_size):
            if grid[row][col] == grid[row + 1][col]:
                return "In Progress"
    return "Game Over!"


def display_game_over_message(message):



    pygame.draw.rect(screen, white, (50, screen_height // 2 - 60, screen_width - 100, 120))

    text = font.render(message, True, black)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    pygame.display.update()
    pygame.time.delay(2000)

# menu
def display_start_menu():
    screen.fill(gray)

    title_text = font.render("2048", True, white)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(title_text, title_rect)

    high_score_text = score_font.render(f"High Score: {high_score}", True, white)
    high_score_rect = high_score_text.get_rect(center=(screen_width // 2, screen_height // 4 + 50))
    screen.blit(high_score_text, high_score_rect)

    start_text = score_font.render("Press Enter to Start", True, white)
    start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2 + 25))
    screen.blit(start_text, start_rect)

    instructions = [
        "How to play:",
        "- Use arrow keys to move tiles.",
        "- Combine tiles with the same number.",
        "- Reach the 2048 tile to win!"
    ]
    y_offset = screen_height // 2 + 80
    for line in instructions:
        instruction_text = score_font.render(line, True, white)
        instruction_rect = instruction_text.get_rect(center=(screen_width // 2, y_offset))
        screen.blit(instruction_text, instruction_rect)
        y_offset += 40

    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_input = False

# display the score bar
def display_score():
    # score bar bg
    pygame.draw.rect(screen, light_gray, (0, 0, screen_width, 60))

    # Score text
    score_text = score_font.render(f"Score: {score}", True, black)
    score_rect = score_text.get_rect(left=10, centery=30)
    screen.blit(score_text, score_rect)

    # high score
    high_score_text = score_font.render(f"High Score: {high_score}", True, black)
    high_score_rect = high_score_text.get_rect(right=screen_width - 10, centery=30)
    screen.blit(high_score_text, high_score_rect)

add_new_tile()
add_new_tile()

display_start_menu()

# Main loop
running = True
game_started = False
while running:
    if not game_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_started = True  # start

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move("up")
                elif event.key == pygame.K_DOWN:
                    move("down")
                elif event.key == pygame.K_LEFT:
                    move("left")
                elif event.key == pygame.K_RIGHT:
                    move("right")

        screen.fill(gray)
        display_score() # score bar
        draw_grid()
        animate_tiles()  # call animation function

        game_state = check_game_state()
        if game_state != "In Progress":
            display_game_over_message(game_state)
            if game_state == "Game Over!":
                if score > high_score:
                    high_score = score
                    with open("high_score.txt", "w") as f:
                        f.write(str(high_score))
                score = 0
                grid = [[0] * grid_size for _ in range(grid_size)]
                add_new_tile()
                add_new_tile()
                game_started = False
                display_start_menu()

        pygame.display.update()

pygame.quit()