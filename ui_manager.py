# Manages UI elements using Pygame, including drawing elements, handling inputs, and screen updates.

import pygame
from config import ButtonConfig, TextConfig

class Button:
    def __init__(self, text, x, y, width, height, callback, radius=10):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback  # Function to call when the button is clicked
        self.font = pygame.font.Font(None, 36)  # Initialize a font object
        self.hover = False  # Track whether the mouse is hovering over a button                                                #11       
        self.default_color = ButtonConfig.BACKGROUND_COLOR  # Default color of the button              
        self.hover_color = ButtonConfig.HOVER_COLOR  # Specify the color when hovering                                  
        self.current_color = self.default_color  # Current color of the button                        
        self.radius = radius  # Radius of the rounded corners   


    def draw(self, screen):
        # Draw the button rectangle and text
        color = self.hover_color if self.hover else self.default_color     
        rect = pygame.Rect(self.x, self.y, self.width, self.height)    
        pygame.draw.rect(screen, color, rect, border_radius=self.radius)    

        text_surface = self.font.render(self.text, True, ButtonConfig.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
        # Add code to draw the text

    def handle_event(self, event):
        # Detect mouse movement events to update hover status                                                     
        if event.type == pygame.MOUSEMOTION:                                               
            self.hover = self.x <= event.pos[0] <= self.x + self.width and \
                         self.y <= event.pos[1] <= self.y + self.height

            # Update button color                                                                    
            if self.hover:
                self.current_color = self.hover_color
            else:
                self.current_color = self.default_color                                     

        # Check if the button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                self.callback()  # Call the button's callback function

    def set_text(self, new_text):
        self.text = new_text

class TimeSettingButton:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback  # Function to call when the button is clicked
        self.font = pygame.font.Font(None, 36)  # Initialize a font object
        self.selected = False

    def draw(self, screen):
        # Choose the background color
        if self.selected:
            background_color = (255, 0, 0)  # Red color for selected
        else:
            background_color = ButtonConfig.BACKGROUND_COLOR  # Global default color for unselected

        # Draw the button rectangle
        pygame.draw.rect(screen, background_color, (self.x, self.y, self.width, self.height))

        # Draw the text
        text_surface = self.font.render(self.text, True, ButtonConfig.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        # Check if the button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                self.selected = True
                self.callback()  # Call the button's callback function

    def set_text(self, new_text):
        self.text = new_text

class Text:
    def __init__(self, text, x, y, font = None, font_size = TextConfig.FONT_SIZE, color = TextConfig.TEXT_COLOR):
        self.text = text
        self.position = (x, y)
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.rendered_text = None
        self.rect = None
        self.render()

    def render(self):
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect = self.rendered_text.get_rect(center=self.position)

    def draw(self, screen):
        screen.blit(self.rendered_text, self.rect)

    def set_position(self, x, y):
        self.position = (x, y)
        self.rect.center = self.position

    def set_text(self, text):
        self.text = text
        self.render()

class Slider:
    def __init__(self, x, y, w, h, min_value=0, max_value=1, initial_value=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value if initial_value is not None else min_value
        self.grabbed = False
        self.handle_width = 10

        # Calculate initial slider position
        initial_x = self.x + (self.value - self.min_value) / (self.max_value - self.min_value) * (self.w - self.handle_width)
        self.handle_rect = pygame.Rect(initial_x, self.y, self.handle_width, self.h)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION:
            if self.grabbed:
                # Update square location
                new_x = max(min(event.pos[0], self.x + self.w - self.handle_width), self.x)
                self.handle_rect.x = new_x
                # Calculate square location
                self.value = self.min_value + ((new_x - self.x) / (self.w - self.handle_width)) * (self.max_value - self.min_value)
                pygame.mixer.music.set_volume(self.value)

    def draw(self, screen):
        # Draw line
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y + self.h // 2 - 2, self.w, 4))
        # Draw square
        pygame.draw.rect(screen, (255, 255, 255), self.handle_rect)

class Table:
    def __init__(self, name, scores, origin, table_width, table_height):
        self.name = name
        self.scores = scores  # Dictionary with player names and scores
        self.origin = origin  # (x, y) tuple
        self.table_width = table_width
        self.table_height = table_height

        # Calculate rows and columns
        self.rows = len(scores) + 1  # +1 for the header row
        self.cols = 3  # Rank, Player Name, Score

        # Calculate the height of each row
        self.row_height = table_height / self.rows

    def draw(self, screen):
        # Sort the scores dictionary by value in descending order
        sorted_scores = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)

        # Draw the table
        for row in range(self.rows):
            for col in range(self.cols):
                # Calculate rectangle position and size
                x = self.origin[0] + col * (self.table_width / self.cols)
                y = self.origin[1] + row * self.row_height
                width = self.table_width / self.cols
                height = self.row_height

                # Draw rectangle for cell
                pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 1)

                # Define text for each cell
                if row == 0:
                    # Header row
                    headers = ["Rank", "Player", "Score"]
                    text = headers[col]
                else:
                    # Player data rows
                    player_name, player_score = sorted_scores[row - 1]
                    if col == 0:
                        text = str(row)  # Rank
                    elif col == 1:
                        text = player_name  # Player Name
                    else:
                        text = str(player_score)  # Score

                # Render the text and blit to screen
                font = pygame.font.Font(None, 36)
                text_surface = font.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
                screen.blit(text_surface, text_rect)