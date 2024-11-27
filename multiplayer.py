import pygame
import random
from button import Button
import shared


# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 620  # Increased height to accommodate vertical grids


class FloodFillGameMP:
    def __init__(self, grid_size, cell_size, num_colors, screen):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.num_colors = num_colors
        self.screen = screen
        # Generate the player's grid with random colors
        self.player_grids = [
            [[random.choice(shared.COLORS[:self.num_colors]) for _ in range(self.grid_size)] for _ in range(self.grid_size)],
            [[random.choice(shared.COLORS[:self.num_colors]) for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        ]
        self.current_player = 0  
        self.winner = None

        # Fonts
        self.font = pygame.font.Font("assets/font.ttf", 20)
        self.largerfont = pygame.font.Font("assets/font.ttf", 45)
        self.smallerfont = pygame.font.Font("assets/font.ttf", 15)

        # Flags for sound effects and pop-ups
        self.win_sfx_played = False
        self.show_instructions = False  

    def perform_flood_fill(self, grid, x, y, target_color, replacement_color):
        shared.flood_fill(grid, x, y, target_color, replacement_color)

    def draw_grid(self, player, x_offset, y_offset):
        grid = self.player_grids[player]
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                cell_rect = (
                    x_offset + y * self.cell_size,
                    y_offset + x * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, grid[x][y], cell_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), cell_rect, 1)

        # Display player info
        player_text = self.font.render(f"Player {player + 1}", True, (0, 0, 0))
        self.screen.blit(player_text, (x_offset, y_offset - 30))
        if self.current_player == player and self.winner is None:
            
            turn_text = self.font.render(f"Player {player + 1}'s Turn", True, (0, 0, 0))
            turn_rect = turn_text.get_rect(center=(SCREEN_WIDTH // 2, 590))
            
            self.screen.blit(turn_text, turn_rect)

    def check_win(self, player):
        first_color = self.player_grids[player][0][0]
        return all(
            self.player_grids[player][x][y] == first_color
            for x in range(self.grid_size)
            for y in range(self.grid_size)
        )

    def handle_mouse_click(self, click_x, click_y):
        if self.winner is not None:
            return  # Game already won

        player = self.current_player
        # Determine which grid was clicked
        grid1_rect = pygame.Rect(125, 50, self.grid_size * self.cell_size, self.grid_size * self.cell_size)
        grid2_rect = pygame.Rect(125, 50 + self.grid_size * self.cell_size + 50, self.grid_size * self.cell_size, self.grid_size * self.cell_size)

        if grid1_rect.collidepoint(click_x, click_y):
            clicked_player = 0
            x_offset = 125
            y_offset = 50
        elif grid2_rect.collidepoint(click_x, click_y):
            clicked_player = 1
            x_offset = 125
            y_offset = 50 + self.grid_size * self.cell_size + 50
        else:
            return  # Click was outside the grids

        if clicked_player != player:
            return  # Not the current player's grid

        # Calculate clicked cell
        clicked_row = (click_y - y_offset) // self.cell_size
        clicked_col = (click_x - x_offset) // self.cell_size

        if 0 <= clicked_row < self.grid_size and 0 <= clicked_col < self.grid_size:
            selected_color = self.player_grids[player][clicked_row][clicked_col]
            top_left_color = self.player_grids[player][0][0]

            if selected_color != top_left_color:
                self.perform_flood_fill(self.player_grids[player], 0, 0, top_left_color, selected_color)
                shared.grid_sfx()
                if self.check_win(player):
                    self.winner = player
                else:
                    self.current_player = 1 - self.current_player  # Switch turns
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        # Initialize buttons for navigation
        back_button = Button(image=None, pos=(40, 40), text_input="←", font=self.largerfont, base_color="White", hovering_color="Green")
        help_button = Button(image=None, pos=(460, 40), text_input="?", font=self.largerfont, base_color="White", hovering_color="Green")

        while running:
            if self.show_instructions:
                self.draw_instructions()
            else:
                self.screen.fill(("#4bc3b5"))  # Background color

                # Define grid positions for vertical alignment
                grid1_x = 125
                grid1_y = 50
                grid2_x = 125
                grid2_y = 50 + self.grid_size * self.cell_size + 50

                # Draw both grids
                self.draw_grid(0, grid1_x, grid1_y)
                self.draw_grid(1, grid2_x, grid2_y)

                # Update and draw navigation buttons
                mouse_pos = pygame.mouse.get_pos()
                back_button.changeColor(mouse_pos)
                back_button.update(self.screen)
                help_button.changeColor(mouse_pos)
                help_button.update(self.screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        click_x, click_y = pygame.mouse.get_pos()
                        if back_button.checkForInput(mouse_pos):
                            shared.btn_sfx()
                            running = False
                            import main  # Import the main page to call the main menu
                            main.main_menu()  # Go back to the main menu
                        if help_button.checkForInput(mouse_pos):
                            shared.btn_sfx()
                            self.show_instructions = True
                        
                        else:
                            self.handle_mouse_click(click_x, click_y)
                

                # Display winner if any
                if self.winner is not None:
                    # Play win sound only once
                    if not self.win_sfx_played:
                        shared.grid_win()
                        self.win_sfx_played = True  # Set flag to True
                    win_text = self.font.render(f"Player {self.winner + 1} Wins!", True, (255, 255, 255))
                    win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    pygame.draw.rect(self.screen, (0, 0, 0), win_rect.inflate(20, 20))  # Background for text
                    self.screen.blit(win_text, win_rect)

            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS
    def draw_instructions(self):
                self.screen.fill("#653780")  # Set the background color for the instructions screen
                instructions_text = self.largerfont.render("Game Rules", True, ("#4bc3b5"))
                self.screen.blit(instructions_text, (30, 60))

                # Text for the game rules
                rules = [
                    "1. Fill the entire board with",
                    "   one color before your",
                    "   opponent",
                    "2. Click a cell to start",
                    "   flooding.",
                    "3. Flooding begins from the",
                    "   top left corner.",
                    "4. The player who fills the",
                    "   grid first wins."
                ]

                y_offset = 150  # Starting y position for the first line
                for rule in rules:
                    rule_text = self.smallerfont.render(rule, True, ("white"))
                    self.screen.blit(rule_text, (30, y_offset))
                    y_offset += 40  # Adjust y position for the next line

                # Add a "OKAY" button to return to the game
                okay_button = Button(
                    image=pygame.image.load("assets/others_button.png"),
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
                        click_x, click_y = pygame.mouse.get_pos()
                        if okay_button.checkForInput(mouse_pos):
                            shared.btn_sfx()
                            self.show_instructions = False