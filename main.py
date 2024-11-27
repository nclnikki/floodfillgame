# Busa, Merza, Ty                   CSC 108 - Project 2             Flood Fill Game

import pygame, sys
from button import Button  
from fillMasterGame import FloodFillGame
from multiplayer import FloodFillGameMP
from pygame import mixer
import shared

# Initialize Modules
pygame.init()
mixer.init()

# Screen setup
SCREEN = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Fill Master")

# Background setup
BG = pygame.image.load("assets/background.png")

# Preload music tracks
MAIN_MENU_MUSIC =  "assets/game-music-loop-3-144252.mp3"
GAME_MUSIC_CLASSIC = "assets/gamemusic-6082.mp3"
GAME_MUSIC_MP = "assets/game-music-loop-5-144569.mp3"

# Function to play music
def play_music(track, loops=-1):
    mixer.music.fadeout(1000)
    mixer.music.load(track)
    mixer.music.play(loops)

# Font setup
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# Classic Function
def classic():
    while True:
        CLASSIC_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("#653780")
        
        CLASSIC_TEXT = get_font(27).render("CHOOSE GRID SIZE", True, "#4bc3b5")
        CLASSIC_RECT = CLASSIC_TEXT.get_rect(center=(250, 100))
        SCREEN.blit(CLASSIC_TEXT, CLASSIC_RECT)

        # Define grid size buttons
        grid_buttons = {
            '4x4': Button(image= None , pos=(120, 210), text_input="4x4", font=get_font(25), base_color="White", hovering_color="Green"),
            '8x8': Button(image=None, pos=(380, 210), text_input="8x8", font=get_font(25), base_color="White", hovering_color="Green"),
            '12x12': Button(image=None, pos=(120, 300), text_input="12x12", font=get_font(25), base_color="White", hovering_color="Green"),
            '16x16': Button(image=None, pos=(380, 300), text_input="16x16", font=get_font(25), base_color="White", hovering_color="Green"),
            '20x20': Button(image=None, pos=(120, 390), text_input="20x20", font=get_font(25), base_color="White", hovering_color="Green"),
            '24x24': Button(image=None, pos=(380, 390), text_input="24x24", font=get_font(25), base_color="White", hovering_color="Green")
        }

        # Back button
        CLASSIC_BACK = Button(image=pygame.image.load("assets/others_button.png"), pos=(250, 510), text_input="BACK", font=get_font(20), base_color="#9b0426", hovering_color="white")
        CLASSIC_BACK.changeColor(CLASSIC_MOUSE_POS)
        CLASSIC_BACK.update(SCREEN)

        # Draw grid size buttons
        for grid_size, button in grid_buttons.items():
            button.changeColor(CLASSIC_MOUSE_POS)
            button.update(SCREEN)

        # Handle events in the game loop
        for event in pygame.event.get():
            # Exit the game if the close button is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Return to the main menu if the "Back" button is clicked
                if CLASSIC_BACK.checkForInput(CLASSIC_MOUSE_POS):
                    shared.btn_sfx()
                    main_menu()
                # Check if a grid size button was clicked
                for grid_size, button in grid_buttons.items():
                    if button.checkForInput(CLASSIC_MOUSE_POS):
                        shared.btn_sfx()
                        # Set game parameters based on the selected grid size
                        size = int(grid_size.split('x')[0])
                        if size == 4:
                            cell_size, num_colors, move_limit = 90, 4, 8
                        elif size == 8:
                            cell_size, num_colors, move_limit = 45, 5, 16
                        elif size == 12:
                            cell_size, num_colors, move_limit = 30, 6, 24
                        elif size == 16:
                            cell_size, num_colors, move_limit = 22, 7, 32
                        elif size == 20:
                            cell_size, num_colors, move_limit = 18, 8, 40  
                        elif size == 24:
                            cell_size, num_colors, move_limit = 15, 8, 48  
                        
                        # Start the game with the selected settings
                        play_music(GAME_MUSIC_CLASSIC)  
                        game = FloodFillGame(size, cell_size, num_colors, move_limit, SCREEN)
                        game.run()
                        
        # Update the display after processing events
        pygame.display.update()

def multiplayer():
    while True:
        MP_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("#653780")
        
        MP_TEXT = get_font(27).render("CHOOSE GRID SIZE", True, "#4bc3b5")
        MP_RECT = MP_TEXT.get_rect(center=(250, 100))
        SCREEN.blit(MP_TEXT, MP_RECT)

        # Define grid size buttons
        grid_buttons = {
            '4x4': Button(image=None, pos=(120, 210), text_input="4x4", font=get_font(35), base_color="White", hovering_color="Green"),
            '5x5': Button(image=None, pos=(380, 210), text_input="5x5", font=get_font(35), base_color="White", hovering_color="Green"),
            '6x6': Button(image=None, pos=(120, 300), text_input="6x6", font=get_font(35), base_color="White", hovering_color="Green"),
            '7x7': Button(image=None, pos=(380, 300), text_input="7x7", font=get_font(35), base_color="White", hovering_color="Green"),
            '8x8': Button(image=None, pos=(120, 390), text_input="8x8", font=get_font(35), base_color="White", hovering_color="Green"),
            '9x9': Button(image=None, pos=(380, 390), text_input="9x9", font=get_font(35), base_color="White", hovering_color="Green")
        }

        # Back button
        MP_BACK = Button(image= pygame.image.load("assets/others_button.png"), pos=(250, 510), text_input="BACK", font=get_font(20), base_color="#9b0426", hovering_color="white")
        MP_BACK.changeColor(MP_MOUSE_POS)
        MP_BACK.update(SCREEN)

        # Draw grid size buttons
        for grid_size, button in grid_buttons.items():
            button.changeColor(MP_MOUSE_POS)
            button.update(SCREEN)
        # Handle events in the game loop
        for event in pygame.event.get():
            # Exit the game if the close button is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Return to the main menu if the "Back" button is clicked
                if MP_BACK.checkForInput(MP_MOUSE_POS):
                    shared.btn_sfx()
                    main_menu()
                # Check if a grid size button was clicked
                for grid_size, button in grid_buttons.items():
                    if button.checkForInput(MP_MOUSE_POS):
                        shared.btn_sfx()
                        # Set game parameters based on the selected grid size
                        size = int(grid_size.split('x')[0])
                        if size == 4:
                            cell_size, num_colors = 56, 6
                        elif size == 5:
                            cell_size, num_colors = 45, 7
                        elif size == 6:
                            cell_size, num_colors = 38, 8
                        elif size == 7:
                            cell_size, num_colors = 32, 10
                        elif size == 8:
                            cell_size, num_colors = 28, 14  
                        elif size == 9:
                            cell_size, num_colors = 25, 14 

                        # Start the game with the selected settings
                        play_music(GAME_MUSIC_MP)
                        game = FloodFillGameMP(size, cell_size, num_colors, SCREEN)
                        game.run()                        

        # Update the display after processing events
        pygame.display.update()


def main_menu(): 
    # Play main menu music
    play_music(MAIN_MENU_MUSIC)
    
    CLASSIC_BUTTON = Button(image=pygame.image.load("assets/main_button.png"), 
                        pos=(250, 280), text_input="CLASSIC", font=get_font(20), base_color="#9b0426", hovering_color="White")
    
    MULTIPLAYER_BUTTON = Button(image=pygame.image.load("assets/main_button.png"), 
                            pos=(250, 400), text_input="MULTIPLAYER", font=get_font(20), base_color="#9b0426", hovering_color="White")

    QUIT_BUTTON = Button(image=pygame.image.load("assets/main_button.png"), 
                        pos=(250, 520), text_input="QUIT", font=get_font(20), base_color="#9b0426", hovering_color="White")

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        MENU_TEXT = get_font(41).render("FILL MASTER", True, "White")
        MENU_RECT = MENU_TEXT.get_rect(center=(250, 100))

        # Create a rectangle behind the text
        rect_width = MENU_TEXT.get_width() + 90
        rect_height = MENU_TEXT.get_height() + 60
        rect_x = MENU_RECT.left -30
        rect_y = MENU_RECT.top -30
        pygame.draw.rect(SCREEN, "black", (rect_x, rect_y, rect_width, rect_height))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Update the buttons on the screen
        for button in [CLASSIC_BUTTON, MULTIPLAYER_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Handle user input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CLASSIC_BUTTON.checkForInput(MENU_MOUSE_POS):
                    shared.btn_sfx()
                    classic()
                if MULTIPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    shared.btn_sfx()
                    multiplayer()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    shared.btn_sfx()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        
# Call the main menu function to display the menu screen
main_menu()



