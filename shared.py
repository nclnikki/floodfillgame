# For functions/lists that can be used in more than one file

import pygame

# Define list of colors
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (0, 255, 255),  # Cyan
    (255, 20, 147), # Pink
]

# Function for the flood fill algorithm
def flood_fill(grid, x, y, target_color, replacement_color):
    if target_color == replacement_color or grid[x][y] != target_color:
        return
    grid[x][y] = replacement_color
    if x > 0:
        flood_fill(grid, x - 1, y, target_color, replacement_color)
    if x < len(grid) - 1:
        flood_fill(grid, x + 1, y, target_color, replacement_color)
    if y > 0:
        flood_fill(grid, x, y - 1, target_color, replacement_color)
    if y < len(grid[0]) - 1:
        flood_fill(grid, x, y + 1, target_color, replacement_color)

# Sound effect for when a button is clicked
def btn_sfx():
    pygame.mixer.Sound("assets/pop-sound-effect-197846.mp3").play()

# Sound effect for when a cell in the grid is clicked
def grid_sfx():
    pygame.mixer.Sound("assets/90s-game-ui-2-185095.mp3").play()

# Sound effect when a player wins
def grid_win():
    pygame.mixer.Sound("assets/achievement-video-game-type-1-230515.mp3").play()

# Sound effect when a player loses
def grid_lose():
    pygame.mixer.Sound("assets/game-over-arcade-6435.mp3").play()


