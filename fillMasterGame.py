import pygame
import random
from button import Button
import shared

# For Classic Mode

class FloodFillGame:
    def __init__(self, grid_size, cell_size, num_colors, move_limit, screen):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.num_colors = num_colors
        self.move_limit = move_limit
        self.nclick = 0  # Tracks the number of clicks the player has made
        self.screen = screen  # Use the passed screen
        self.font = pygame.font.Font("assets/font.ttf", 20)
        self.smallerfont = pygame.font.Font("assets/font.ttf", 15)
        self.largerfont = pygame.font.Font("assets/font.ttf", 45)
        # Generate the game grid with random colors
        self.grid = [[random.choice(shared.COLORS[:self.num_colors]) for _ in range(self.grid_size)]
                     for _ in range(self.grid_size)]
        # Flags for sound effects and pop-ups
        self.win_sfx_played = False
        self.lose_sfx_played = False    
        self.show_instructions = False  
    

    def perform_flood_fill(self, x, y, target_color, replacement_color):
        target_color = self.grid[x][y]
        shared.flood_fill(self.grid, x, y, target_color, replacement_color)


    def draw_grid(self):
        # Draw the grid on the provided screen, centered horizontally and vertically.
        grid_width = self.grid_size * self.cell_size
        grid_height = self.grid_size * self.cell_size

        # Calculate the offset to center the grid
        x_offset = (self.screen.get_width() - grid_width) // 2
        y_offset = ((self.screen.get_height() - grid_height) // 2) - 50

        # Draw each cell and its border
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                # Use the offset to position the cell rectangles
                cell_rect = (x_offset + y * self.cell_size, y_offset + x * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.grid[x][y], cell_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), cell_rect, 1)

        # Update the position of the moves text to stay below the grid (optional)
        moves_text = self.font.render(f"Moves Left: {self.move_limit - self.nclick}", True, (0, 0, 0))
        self.screen.blit(moves_text, (10 + x_offset, grid_height + y_offset + 10))
    
    def check_win(self):
        # Check if all cells are of the same color
        first_color = self.grid[0][0]
        return all(self.grid[x][y] == first_color for x in range(self.grid_size) for y in range(self.grid_size))
    
    def handle_mouse_click(self, click_x, click_y):
        if self.nclick < self.move_limit and not self.check_win():
            ## Calculate grid coordinates of the clicked cell
            grid_x = (self.screen.get_width() - self.grid_size * self.cell_size) // 2
            grid_y = ((self.screen.get_height() - self.grid_size * self.cell_size) // 2) - 50
            clicked_row = (click_y - grid_y) // self.cell_size
            clicked_col = (click_x - grid_x) // self.cell_size

            # Check if the clicked coordinates are within the grid bounds
            if 0 <= clicked_row < self.grid_size and 0 <= clicked_col < self.grid_size:
                selected_color = self.grid[clicked_row][clicked_col]  # Color of clicked cell
                top_left_color = self.grid[0][0]  # Color of the top-left cell

                # Perform flood fill if the selected color is different
                if selected_color != top_left_color:
                    self.perform_flood_fill(0, 0, top_left_color, selected_color)
                    shared.grid_sfx()
                    self.nclick += 1
   
    def run(self):
        # Main game loop
        running = True

        # Initialize buttons for navigation
        back_button = Button(image=None, pos=(40, 40), text_input="←", font=self.largerfont, base_color="White", hovering_color="Green")
        help_button = Button(image=None, pos=(460, 40), text_input="?", font=self.largerfont, base_color="White", hovering_color="Green")

        while running:

            if self.show_instructions:
                self.draw_instructions()    # Show instructions screen
            else:
                self.screen.fill(("#4bc3b5"))  # Background color for the game screen
                self.draw_grid()  # Draw the grid and moves left    

                # Update and draw navigation buttons
                mouse_pos = pygame.mouse.get_pos()
                back_button.changeColor(mouse_pos)
                back_button.update(self.screen)
                help_button.changeColor(mouse_pos)
                help_button.update(self.screen)

                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:       # Exit game
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        click_x, click_y = pygame.mouse.get_pos()
                        if back_button.checkForInput(mouse_pos):      # Go back to main menu
                            shared.btn_sfx()
                            running = False
                            import main  # Import the main page to call the main menu
                            main.main_menu()  # Go back to the main menu
                        elif help_button.checkForInput(mouse_pos):      # Show instructions
                            shared.btn_sfx()
                            self.show_instructions = True                
                        else:                                       # Handle grid interactions
                            self.handle_mouse_click(click_x, click_y)

                # Check win/loss conditions
                if self.check_win():
                    win_text = self.largerfont.render("You Win!", True, ("white"))
                    text_rect = win_text.get_rect(center=(500 // 2, 1070 // 2))
                    self.screen.blit(win_text, text_rect)

                    # Play win sound only once
                    if not self.win_sfx_played:
                        shared.grid_win()
                        self.win_sfx_played = True  # Set flag to True
                elif self.nclick >= self.move_limit:
                    lose_text = self.largerfont.render("You Lose!", True, ("white"))
                    text_rect = lose_text.get_rect(center=(500 // 2, 1070 // 2))
                    self.screen.blit(lose_text, text_rect)

                    # Play lose sound only once
                    if not self.lose_sfx_played:
                        shared.grid_lose()
                        self.lose_sfx_played = True  # Set flag to True
            pygame.display.flip()

    def draw_instructions(self):
            self.screen.fill("#653780")  
            instructions_text = self.largerfont.render("Game Rules", True, ("#4bc3b5"))
            self.screen.blit(instructions_text, (30, 60))
            # Text for the game rules
            rules = [
                "1. Fill the entire board with",
                "   one color within a limited",
                "   number of moves.",
                "2. Click a cell to start",
                "   flooding.",
                "3. Flooding begins from the",
                "   top left corner."
            ]

            # Render and display each rule
            y_offset = 150  
            for rule in rules:
                rule_text = self.smallerfont.render(rule, True, ("white"))
                self.screen.blit(rule_text, (30, y_offset))
                y_offset += 40  

            # Add a "OKAY" button to return to the game
            okay_button = Button(
                image= pygame.image.load("assets/others_button.png"),
                pos=(245, 540),
                text_input="OKAY",
                font=self.font,
                base_color="#9b0426",
                hovering_color="white"
            )

            # Update and draw the Back button
            mouse_pos = pygame.mouse.get_pos()
            okay_button.changeColor(mouse_pos)
            okay_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if okay_button.checkForInput(mouse_pos):
                        shared.btn_sfx()
                        self.show_instructions = False