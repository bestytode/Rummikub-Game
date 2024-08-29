# Board class for AI and human player, where most interactions happen.

import pygame
from config import TileConfig, BoardConfig, BorderConfig
from tile_set import Tile

# Define a mapping from color names to RGB values
color_mapping = {
    'red': (255, 80, 80),
    'green': (80, 255, 80),
    'blue': (80, 80, 255),
    'alpha': (150, 150, 150),  # color for 'alpha'
    'yellow': (255, 255, 80),
    # no color for joker, use image only
}

class Board:
    def __init__(self, name, player, origin: tuple, board_width, board_height, callback):
        self.player = player
        self.name = name
        self.origin = origin  # (x, y) tuple
        self.board_width = board_width
        self.board_height = board_height
        self.callback = callback

    def draw(self, screen):
        # Draw the board background
        pygame.draw.rect(screen, (255, 255, 255), (*self.origin, self.board_width, self.board_height))
        pygame.draw.rect(screen, BorderConfig.COLOR, (*self.origin, self.board_width, self.board_height), BorderConfig.WIDTH)

        # Initialize starting position
        x, y = self.origin
        row_height = 0  # Keep track of the tallest tile in the current row

        # Draw the tiles
        for tile in self.player.hand:
            # If the next tile will go beyond the board's width, wrap to the next line
            if x + TileConfig.WIDTH > self.origin[0] + self.board_width:
                x = self.origin[0]  # Reset x to the first column
                y += row_height + TileConfig.MARGIN  # Move y to the next row and reset row height
                row_height = 0
            
            # Draw the tile background color using the color mapping
            tile_color = color_mapping.get(tile.color, (200, 200, 200))  # Default color if not found
            pygame.draw.rect(screen, tile_color, (x, y, TileConfig.WIDTH, TileConfig.HEIGHT))

            # Blit the tile image
            screen.blit(tile.image, (x, y))

            # Draw the numbers if it's not a joker
            if tile.color != 'joker':
                font = pygame.font.Font(None, 24)  # Small font for numbers
                number_surface = font.render(str(tile.number), True, (0, 0, 0))
                
                # Get the rectangle of the number surface to position it in the center
                number_rect = number_surface.get_rect(center=(x + TileConfig.WIDTH // 2, y + TileConfig.HEIGHT // 2))
                screen.blit(number_surface, number_rect)

            # Update x to the next tile position, and update row_height if current tile is taller
            x += TileConfig.WIDTH + TileConfig.MARGIN
            row_height = max(row_height, TileConfig.HEIGHT)
    
    def handle_event(self, event):
        pass

class BotPlayerBoard(Board):
    pass

class HumanPlayerBoard(Board):
    def __init__(self, name, player, origin, board_width, board_height, callback):
        super().__init__(name, player, origin, board_width, board_height, callback)
        self.selected_tile: Tile = None  # To keep track of the selected tile
        self.tile_positions = []  # List to store positions of each tile
        self.update_tile_positions()
    
    def update_tile_positions(self):
        self.tile_positions.clear()
        x, y = self.origin

        for index, tile in enumerate(self.player.hand):
            if x + TileConfig.WIDTH > self.origin[0] + self.board_width:
                # Move to the next row
                x = self.origin[0]
                y += TileConfig.HEIGHT + TileConfig.MARGIN

            tile_x = x
            tile_y = y
            self.tile_positions.append((tile_x, tile_y, tile))  # Store the tile object or index along with its position

            x += TileConfig.WIDTH + TileConfig.MARGIN

    def is_click_on_tile(self, click_position, tile_position):
        x, y = tile_position
        tile_area = pygame.Rect(x, y, TileConfig.WIDTH, TileConfig.HEIGHT)
        return tile_area.collidepoint(click_position)

    def is_click_within_player_board_area(self, click_position):
        # Define the area of the player board
        x, y = self.origin
        width, height = self.board_width, self.board_height
        player_board_area = pygame.Rect(x, y, width, height)
        return player_board_area.collidepoint(click_position)
    
    def draw(self, screen):
        super().draw(screen)
        if self.selected_tile:
            for tile_position in self.tile_positions:
                x, y, tile = tile_position
                if tile == self.selected_tile:
                    pygame.draw.rect(screen, BoardConfig.BORDER_COLOR, (x, y, TileConfig.WIDTH, TileConfig.HEIGHT), 2)  # Yellow border for highlight
                    break
                
    def handle_event(self, event, main_board):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for tile_pos in self.tile_positions:
                position, tile = tile_pos[:2], tile_pos[2]
                if self.is_click_on_tile(event.pos, position):
                    if self.selected_tile == tile:
                        self.selected_tile = None
                    else:
                        self.selected_tile = tile
                        if main_board.selected_tile:
                            main_board.selected_tile = None
                    if self.callback:
                        self.callback(self.selected_tile)
                    break

class TileChoiceBoard:
    def __init__(self, name, tiles: list, origin: tuple, callback):
        self.name = name
        self.tiles = tiles # a list of two tile objects
        self.origin = origin  # (x, y) tuple for the top-left corner of the choice board

        self.width = 2 * TileConfig.WIDTH + TileConfig.MARGIN
        self.height = TileConfig.HEIGHT  
        self.callback = callback  
        
    def draw(self, screen):
        # Draw the background for the tile choice area
        pygame.draw.rect(screen, (255, 255, 255), (*self.origin, self.width, self.height))
        pygame.draw.rect(screen, BorderConfig.COLOR, (*self.origin, self.width, self.height), BorderConfig.WIDTH)

        # Draw the two tile choices
        for i, tile in enumerate(self.tiles):
            tile_x = self.origin[0] + i * (TileConfig.WIDTH + TileConfig.MARGIN)
            tile_y = self.origin[1]

            # Draw the tile background color using the color mapping
            tile_color = color_mapping.get(tile.color, (200, 200, 200))  # Default color
            pygame.draw.rect(screen, tile_color, (tile_x, tile_y, TileConfig.WIDTH, TileConfig.HEIGHT))

            # Blit the tile image
            screen.blit(tile.image, (tile_x, tile_y))

            # Draw the number on the tile if it's not a joker
            if tile.number:  # important: correspondes to previous 'joker' number 0
                font = pygame.font.Font(None, 36)  # Use an appropriate font size
                text_surface = font.render(str(tile.number), True, (0, 0, 0))
                # Center the text on the tile
                text_rect = text_surface.get_rect(center = (tile_x + TileConfig.WIDTH // 2, tile_y + TileConfig.HEIGHT // 2))
                screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Define the rectangles for the left and right tile areas
            left_tile_rect = pygame.Rect(self.origin[0], self.origin[1], TileConfig.WIDTH, TileConfig.HEIGHT)
            right_tile_rect = pygame.Rect(self.origin[0] + TileConfig.WIDTH + TileConfig.MARGIN, self.origin[1], TileConfig.WIDTH, TileConfig.HEIGHT)

            # Check if the click was on the left tile
            if left_tile_rect.collidepoint(mouse_x, mouse_y):
                self.callback(self.tiles[0])  # Invoke the callback with the left tile
                return

            # Check if the click was on the right tile
            if right_tile_rect.collidepoint(mouse_x, mouse_y):
                self.callback(self.tiles[1])  # Invoke the callback with the right tile
                return
            
class MainBoard:
    def __init__(self, name, origin, board_width, board_height, tile_width, tile_height, callback):
        self.name = name
        self.origin = origin
        self.board_width = board_width
        self.board_height = board_height
        self.tile_width = tile_width
        self.tile_height = tile_height

        self.slots = self.calculate_slots(self.origin) # Initialize slots (450 slots currently)
        self.tiles = [None] * len(self.slots) # Keep track of tiles in each slot
        self.tile_placed_this_turn = False
        self.selected_tile = None
        self.callback = callback

    def calculate_slots(self, start_pos):
        slots = []
        x, y = start_pos

        for line in range(self.board_height // self.tile_height):  # 15 lines currently
            for slot in range(self.board_width // self.tile_width):  # 30 slots per line currently
                slots.append((x, y))
                x += self.tile_width
            x = start_pos[0]
            y += self.tile_height

        return slots

    def draw(self, screen):
        # Draw the outer rectangle for the board
        pygame.draw.rect(screen, (255, 255, 255), (*self.origin, self.board_width, self.board_height))
        pygame.draw.rect(screen, BorderConfig.COLOR, (*self.origin, self.board_width, self.board_height), BorderConfig.WIDTH)

        # Draw the tiles
        for i, tile in enumerate(self.tiles):
            if tile:
                position = self.slots[i]
                self.draw_tile(screen, tile, position)

    def draw_tile(self, screen, tile, position):
        # Map the tile color to an RGB value
        color_rgb = color_mapping.get(tile.color, (200, 200, 200))

        # Draw the tile background
        pygame.draw.rect(screen, color_rgb, (position[0], position[1], self.tile_width, self.tile_height))

        if tile.color == 'joker':
            # For joker, blit the image only
            screen.blit(tile.image, position)
        else:
            # For regular tiles, render the number and then the tile image
            # Render the tile number
            font = pygame.font.Font(None, 36)  # Choose an appropriate font and size
            text = font.render(str(tile.number), True, (0, 0, 0))  # Black color for the text
            text_rect = text.get_rect(center=(position[0] + self.tile_width // 2, position[1] + self.tile_height // 2))
            screen.blit(text, text_rect)
        
            # Blit the tile image
            screen.blit(tile.image, position)
        
        # If this tile is the selected one, draw a yellow border around it
        if self.selected_tile == tile:
            highlight_color = (255, 255, 0)  # Yellow color for the highlight
            pygame.draw.rect(screen, highlight_color, (position[0], position[1], self.tile_width, self.tile_height), 3)  # Draw a yellow border
            #print(f"Highlighting selected tile at position {position}")

    def get_clicked_slot_index(self, mouse_position):
        # Check slots
        for i, slot in enumerate(self.slots):
            if self.is_position_within_tile(mouse_position, slot):
                return i  # Return the index of the clicked slot

        return None  # Return None if no slot was clicked

    def is_position_within_tile(self, pos, tile_pos):
        x, y = pos
        tile_x, tile_y = tile_pos
        within_x = tile_x <= x < tile_x + self.tile_width
        within_y = tile_y <= y < tile_y + self.tile_height

        return within_x and within_y
    
    def handle_event(self, event, player_board, select_only=False):
        tile_placed = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            slot_index = self.get_clicked_slot_index(event.pos)

            # Select or unselect a tile from the main board
            if select_only and slot_index is not None and self.tiles[slot_index] is not None:
                if self.tiles[slot_index] == self.selected_tile:
                    # Unselect the already selected tile
                    self.selected_tile = None
                    print(f"Tile unselected from main board.")
                    player_board.selected_tile = None
                    return False
                else:
                    # Select a new tile
                    self.selected_tile = self.tiles[slot_index]
                    print(f"Tile selected from board: Color - {self.selected_tile.color}, Number - {self.selected_tile.number}, Slot Index - {slot_index}")
                    player_board.selected_tile = None
                    return True

            # Move the selected tile within the main board to a new empty slot
            if self.selected_tile and slot_index is not None and self.tiles[slot_index] is None:
                old_slot_index = self.tiles.index(self.selected_tile)
                self.tiles[old_slot_index] = None
                self.tiles[slot_index] = self.selected_tile
                self.selected_tile = None
                print(f"Moved tile from slot {old_slot_index} to slot {slot_index}")
                return True

            # Place a tile from the player's hand to the main board
            if slot_index is not None and self.tiles[slot_index] is None and player_board.selected_tile is not None:
                self.tiles[slot_index] = player_board.selected_tile
                tile_placed = True
                print(f"Placing tile from hand to board: Color - {player_board.selected_tile.color}, Number - {player_board.selected_tile.number}, Slot Index - {slot_index}")

        if tile_placed:
            player_board.player.hand.remove(player_board.selected_tile)
            self.tile_placed_this_turn = True
            player_board.selected_tile = None
            player_board.update_tile_positions()
            print(f"Tile placed and removed from hand. Hand size now: {len(player_board.player.hand)}")
            return True

        return False
    
    def is_valid_set(self, tile_set, color, parity):
        if len(tile_set) < 3:
            return False

        jokers = [tile for tile in tile_set if tile.color == 'joker']
        regular_tiles = [tile for tile in tile_set if tile.color != 'joker']

        # If they were all joker, at least 3 would be needed
        if not regular_tiles:
            return len(jokers) >= 3

        # Check color consistency
        first_tile_color = regular_tiles[0].color
        if any(tile.color != first_tile_color for tile in regular_tiles):
            return False

        # Make sure base numbers and parity
        base_number = regular_tiles[0].number
        parity = base_number % 2

        # Traverse tiles, checking continuity
        expected_number = base_number
        for tile in tile_set:
            if tile.color == 'joker':
                expected_number += 2
                continue

            if tile.number != expected_number or tile.number % 2 != parity:
                return False
            expected_number += 2

        return True
    
    def is_valid_row(self, row):
        # Extract the tiles in the row
        row_start = row * (self.board_width // self.tile_width)
        row_end = row_start + (self.board_width // self.tile_width)
        tiles_in_row = self.tiles[row_start:row_end]

        # Print the entire row for debugging
        print(f"Checking row {row} for validity.")
        print(f"Row {row} tiles: {[(tile.color, tile.number) if tile else ('None', 'None') for tile in tiles_in_row]}")

        # Initialize variables to track the current set
        current_set = []
        current_color = None
        current_parity = None

        # Iterate over each tile in the row
        for tile in tiles_in_row:
            if tile is None:
                # Empty slot, check if current set is valid before resetting
                if current_set and not self.is_valid_set(current_set, current_color, current_parity):
                    print(f"Current set before empty slot is invalid: {[(t.color, t.number) for t in current_set if t]}")
                    return False
                # Reset for the next set
                current_set = []
                current_color = None
                current_parity = None
            else:
                # If current set is empty, initialize it
                if not current_set:
                    current_color = tile.color
                    current_parity = tile.number % 2 if tile.color != 'joker' else None
                # Add tile to the current set
                current_set.append(tile)

        # Check the last set in the row
        if current_set and not self.is_valid_set(current_set, current_color, current_parity):
            print(f"Current set at end of row is invalid: {[(t.color, t.number) for t in current_set if t]}")
            return False

        print(f"Row {row} is valid.")
        return True
    
    def check_specific_combination_valid(self, tiles):
        if not tiles:
            return False

        # Make sure color and parity of combinations
        color = tiles[0].color
        parity = tiles[0].number % 2 if tiles[0].color != 'joker' else None

        return self.is_valid_set(tiles, color, parity)
    
    def is_valid_board_state(self, first_time_check_main_board):
        print("Checking the entire board state for validity.")

        total_value = 0  # Initialize total value counter

        # Iterate through each row
        for row in range(self.board_height // self.tile_height):
            row_start = row * (self.board_width // self.tile_width)
            row_end = row_start + (self.board_width // self.tile_width)
            tiles_in_row = self.tiles[row_start:row_end]

            # Accumulate the total value of the cards in this row
            for tile in tiles_in_row:
                if tile is not None and tile.color != 'joker':
                    total_value += tile.number
                if tile is not None and tile.color == 'joker':
                    total_value += 30

            # Check if the line complies with the rules
            if not self.is_valid_row(row):
                print(f"Row {row} is invalid.")
                return False

        # Check whether the total value of the cards is greater than or equal to 30
        if total_value < 30 and first_time_check_main_board:
            print(f"Total value of tiles on board ({total_value}) is less than 30.")
            return False

        print("All rows are valid. The board state is valid.")
        return True