# Manages the game state, rules, and transitions between different phases of the game.

import pygame
import sys
import config
import copy

from game_timer import Timer
from ui_manager import Button, Text, Slider, Table, TimeSettingButton
from tile_set import TileSet, JokerTile
from player import Player, BotPlayer
from board import TileChoiceBoard, BotPlayerBoard, HumanPlayerBoard, MainBoard
from asset_manager import ImageManager

from config import SHOW_TILE_POOL
from config import ScreenConfig, ButtonConfig, BoardConfig, TileConfig, TimerConfig, MainBoardConfig, SettingsConfig, GameOverConfig, TextConfig

# Game manager overall, to handle events, switch state, etc.
class GameManager:
    def __init__(self, screen, image_manager, music_manager):
        self.screen = screen
        self.player_scores = {} # to display final scores
        self.image_manager: ImageManager = image_manager # manage images
        self.music_manager = music_manager               # manage music
        self.current_state: GameState = MainMenu(self)   # Pass reference to self for back reference
        self.back_ground_image = image_manager.get_image('BackGround')

    def switch_state(self, new_state_class):
        self.current_state = new_state_class(self) # Maintain the back reference

    def restart_game(self):
        # Cleanup the current instance resources
        if self.current_state:
            self.current_state.clean_up()

        # Create a new GamePlay instance
        self.current_state = GamePlay(self)

    def handle_events(self, events):
        self.current_state.handle_events(events)
    
    def update(self):
        self.current_state.update()

    def draw(self):
        self.current_state.draw()

class GameState:
    def __init__(self, game_manager):
        self.game_manager = game_manager # Back reference to the manager
    
    def handle_events(self, events):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError
    
    def draw(self):
        raise NotImplementedError

class MainMenu(GameState):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        # init text
        self.title = Text("RUMMIKUB", ScreenConfig.WIDTH // 2, 100, font_size = 48)
        self.info = Text("Developed by Zhenhuan, Yichun, Yiheng, Zhuojun, Qi - version 1.0", ScreenConfig.WIDTH // 2, ScreenConfig.HEIGHT - 30)

        # init buttons 
        self.play_button = Button("Play", ButtonConfig.MAIN_PLAY_X, ButtonConfig.MAIN_PLAY_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.start_game)
        self.settings_button = Button("Settings", ButtonConfig.MAIN_SETTINGS_X, ButtonConfig.MAIN_SETTINGS_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.open_settings)
        self.quit_button = Button("Quit", ButtonConfig.MAIN_QUIT_X, ButtonConfig.MAIN_QUIT_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.quit_game)

        # bgm
        self.game_manager.music_manager.play_music('MainPageBGM', -1)

    def start_game(self):
        # Use back reference to switch state
        self.game_manager.music_manager.stop_music()
        self.game_manager.switch_state(GamePlay)

    def open_settings(self):
        # Logic to open the settings menu
        self.game_manager.switch_state(Settings)
    
    def quit_game(self):
        # Logic to quit the game
        pygame.quit()
        sys.exit()

    def handle_events(self, events):
        for event in events:
            self.play_button.handle_event(event)
            self.settings_button.handle_event(event)
            self.quit_button.handle_event(event)

    def update(self):
        pass

    def draw(self):
        self.game_manager.screen.blit(self.game_manager.back_ground_image, (0, 0))

        self.title.draw(self.game_manager.screen)
        self.info.draw(self.game_manager.screen)

        # Draw buttons
        self.play_button.draw(self.game_manager.screen)
        self.settings_button.draw(self.game_manager.screen)
        self.quit_button.draw(self.game_manager.screen)

class Settings(GameState):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.title = Text("Volume Setting", ScreenConfig.WIDTH // 2, SettingsConfig.START_Y, font_size=48)
        self.back_button = Button("Back to Menu", ButtonConfig.SETTINGS_BACK_X, ButtonConfig.SETTINGS_BACK_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.back_to_menu)
        self.volume_slider = Slider(ScreenConfig.WIDTH // 2 - 100, SettingsConfig.SLIDER_Y, 200, 20, 0, 1, pygame.mixer.music.get_volume())
        
        self.time_setting_text = Text("Time Setting", ScreenConfig.WIDTH // 2, SettingsConfig.SELECT_TIME_BUTTON_Y, font_size=48)
        self.time_30_button = TimeSettingButton("30s", SettingsConfig.CENTER_X - ButtonConfig.WIDTH - 10, SettingsConfig.TIME_BUTTONS_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, lambda: self.select_time_option(30))
        self.time_60_button = TimeSettingButton("60s", SettingsConfig.CENTER_X, SettingsConfig.TIME_BUTTONS_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, lambda: self.select_time_option(60))
        self.time_90_button = TimeSettingButton("90s", SettingsConfig.CENTER_X + ButtonConfig.WIDTH + 10, SettingsConfig.TIME_BUTTONS_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, lambda: self.select_time_option(90))

    def back_to_menu(self):
        # Logic to return to the main menu
        self.game_manager.switch_state(MainMenu)

    def select_time_option(self, selected_time):
        TimerConfig.PLAYER_TIME_LIMIT = selected_time

        # Reset all buttons to unselected
        self.time_30_button.selected = False
        self.time_60_button.selected = False
        self.time_90_button.selected = False

        # Set the clicked button to selected
        if selected_time == 30:
            self.time_30_button.selected = True
        elif selected_time == 60:
            self.time_60_button.selected = True
        elif selected_time == 90:
            self.time_90_button.selected = True

    def handle_events(self, events):
        for event in events:
            self.back_button.handle_event(event)
            self.volume_slider.handle_event(event)
            self.time_30_button.handle_event(event)
            self.time_60_button.handle_event(event)
            self.time_90_button.handle_event(event)

    def update(self):
        pass

    def draw(self):
        # Draw the settings background
        self.game_manager.screen.blit(self.game_manager.back_ground_image, (0, 0))

        # Draw 'Back to Menu' button
        self.back_button.draw(self.game_manager.screen)
        self.volume_slider.draw(self.game_manager.screen)
        self.title.draw(self.game_manager.screen)
        self.time_setting_text.draw(self.game_manager.screen)
        self.time_30_button.draw(self.game_manager.screen)
        self.time_60_button.draw(self.game_manager.screen)
        self.time_90_button.draw(self.game_manager.screen)

        

class GamePlay(GameState):
    def __init__(self, game_manager: GameManager):
        super().__init__(game_manager)
        self.tile_set = TileSet(game_manager.image_manager)  # Current tile set in pool

        # buttons UI
        self.display_button = Button("Display Bot", ButtonConfig.GAME_BUTTON_X, ButtonConfig.GAME_DISPLAY_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.toggle_display)
        self.quit_button = Button("Quit", ButtonConfig.GAME_BUTTON_X, ButtonConfig.GAME_QUIT_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.quit)
        self.pause_button = Button("Pause", ButtonConfig.GAME_BUTTON_X, ButtonConfig.GAME_PAUSE_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.toggle_pause)
        self.start_button = Button("Start", ButtonConfig.GAME_BUTTON_X, ButtonConfig.GAME_START_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.start)
        self.restart_button = Button("Restart", ButtonConfig.GAME_BUTTON_X, ButtonConfig.GAME_RESTART_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.restart)
        self.pool_button = Button("Show Pool", ButtonConfig.GAME_BUTTON_X, ButtonConfig.GAME_POOL_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.toggle_pool)
        self.order_color_button = Button("777", ButtonConfig.GAME_BUTTON_X, ButtonConfig.GAME_ORDER_COLOR_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.order_by_color)
        self.order_number_button = Button("789", ButtonConfig.GAME_BUTTON_X, ButtonConfig.GAME_ORDER_NUMBER_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.order_by_number)
        self.draw_button = Button("Draw Tiles", ButtonConfig.GAME_BUTTON_X, ButtonConfig.GAME_DRAW_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.draw_two_choose_one)
        self.confirm_button = Button("Confirm", ButtonConfig.GAME_BUTTON_X, ButtonConfig.GAME_CONFIRM_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.confirm_player_action)
        self.regret_button = Button("Regret", ButtonConfig.GAME_BUTTON_X, ButtonConfig.GAME_REGRET_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.toggle_regret)

        # players UI 
        self.human_player = Player("Human Player")  # Human player
        self.bot_player_1 = BotPlayer("Bot Player1")  # the first bot player
        self.current_player: Player = None  # Could be self.player or an AI player

        # boards UI
        self.player_board = HumanPlayerBoard("human player board", self.human_player, BoardConfig.HUMAN_PLAYER_ORIGIN, BoardConfig.WIDTH, BoardConfig.HEIGHT, self.on_tile_selected)
        self.bot_board_1 = BotPlayerBoard("bot player1 board", self.bot_player_1, BoardConfig.BOT_PLAYER_1_ORIGIN, BoardConfig.WIDTH, BoardConfig.HEIGHT, None)
        self.choice_board: TileChoiceBoard = None  # will be allocated with 2 tiles for player to pick
        self.main_board = MainBoard("Main Board", MainBoardConfig.ORIGIN, MainBoardConfig.WIDTH, MainBoardConfig.HEIGHT, TileConfig.WIDTH, TileConfig.HEIGHT, None)

        # flags
        self.is_start = False # this is for start button, ban some button callback functions if this is true
        self.is_displaying = False # this will decide bot board whether display
        self.is_choosing = False  # Flag to indicate if the player is currently choosing tiles (for displaying TileChoiceBoard)
        self.player_turn_completed = False # this will end current player's turn if set to true
        self.is_confirm = False # if player click confirm button, perform check logic
        self.bot_turn_completed = False
        self.player_click_draw_button = False
        self.player_clicked_regret_button = False
        self.first_time_check_main_board = True

        # timer and current player
        self.player_timer = Timer(TimerConfig.PLAYER_TIME_LIMIT)
        self.bot_player_1_timer = Timer(TimerConfig.BOT_PLAYER_1_TIME_LIMIT)
        self.timer_text = Text("Time Left", TextConfig.TIMER_X, TextConfig.TIMER_Y, font_size = TextConfig.TIMER_SIZE, color = TextConfig.TIMER_COLOR)

        # list of text
        self.pool_text_lines: list = self.create_pool_text_lines()

        # debug only
        self.last_printed_time = None

        # to record tile situation for recovering
        self.player_tile_at_turn_beginning = None
        self.main_board_tile_at_turn_beginning = None

        # background music
        self.game_manager.music_manager.play_music('GamePlayBGM',-1)

    def toggle_regret(self):
        self.player_clicked_regret_button = True

    def confirm_player_action(self):
        self.is_confirm = True

    def on_tile_selected(self, selected_tile):
        if self.current_player != self.human_player:
            return
            # Logic to be executed when a tile is selected on the human player's board
        if selected_tile is not None:
            print(f"Callback function: Tile selected: Color - {selected_tile.color}, Number - {selected_tile.number}")


    def are_tile_lists_equal(self, tiles1, tiles2):
        if len(tiles1) != len(tiles2):
            return False
        for tile1, tile2 in zip(tiles1, tiles2):
            if (tile1 is None and tile2 is not None) or (tile1 is not None and tile2 is None):
                return False
            if tile1 is not None and tile2 is not None and not tile1.equals(tile2):
                return False
        return True

    def draw_two_choose_one(self):
        # Check if the player has already taken an action or is in the process of choosing tiles
        if self.player_turn_completed or self.current_player != self.human_player or self.is_choosing:
            return
        if not self.are_tile_lists_equal(self.main_board_tile_at_turn_beginning, self.main_board.tiles):
            return

        tiles_for_selection = self.tile_set.pop_two_for_selection()

        if tiles_for_selection:
            self.is_choosing = True  # Set the flag to True when tiles are being chosen
            self.choice_board = TileChoiceBoard("choice board", tiles_for_selection, BoardConfig.CHOICE_ORIGIN, self.confirm_tile_choice)

        self.refresh_pool_text_lines()

    # helper function for draw_two_choose_one
    def confirm_tile_choice(self, chosen_tile):
        # Add the chosen tile to the player's hand
        self.human_player.hand.append(chosen_tile)
        
        # Remove the chosen tile from the TileChoiceBoard
        self.choice_board.tiles.remove(chosen_tile)
        
        # Return the other tile to the pool
        remaining_tile = self.choice_board.tiles.pop()
        self.tile_set.add_tile(remaining_tile)
        
        self.player_board.update_tile_positions()
        # Hide the TileChoiceBoard and update the display
        self.choice_board = None
        #self.player_turn_completed = True
        self.player_click_draw_button = True
        self.is_choosing = False  # Reset the flag once a choice is made

    def create_pool_text_lines(self): 
        pool_text = self.tile_set.show_current_pool()
        y_offset = 50
        text_lines = []
        for line in pool_text.split('\n'):
            text_line = Text(line, 250, y_offset, font_size = 24, color = (0, 0, 0))
            text_lines.append(text_line)
            y_offset += 30
        return text_lines
    
    def refresh_pool_text_lines(self):
        self.pool_text_lines = self.create_pool_text_lines()

    def toggle_pool(self):
        global SHOW_TILE_POOL

        # debug only
        print("hide tile pool") if SHOW_TILE_POOL else print("show tile pool")
        SHOW_TILE_POOL = not SHOW_TILE_POOL
        button_label = "Show Pool" if SHOW_TILE_POOL else "Hide Pool"
        self.pool_button.set_text(button_label)

    def toggle_pause(self):
        # debug only
        print("continue") if config.IS_PAUSED else print("pausing")

        config.IS_PAUSED = not config.IS_PAUSED
        self.game_manager.music_manager.pause_music() if config.IS_PAUSED else self.game_manager.music_manager.resume_music()
        button_label = "Unpause" if config.IS_PAUSED else "Pause"
        self.pause_button.set_text(button_label)

    def display_pool(self, screen):
        for text_line in self.pool_text_lines:
            text_line.draw(screen)

    def distribute_initial_tiles(self, nr_init_tile):
        # Distribute 14 tiles to each human_player
        for _ in range(nr_init_tile):
            self.human_player.draw_tile(self.tile_set)
            self.bot_player_1.draw_tile(self.tile_set)

        self.player_board.update_tile_positions()
        self.refresh_pool_text_lines()  # Update the tile pool text lines

    def end_game(self, winner = None):
        self.calculate_scores()
        self.game_manager.switch_state(GameOver)

    def calculate_scores(self):
        # Calculate the total score of all players' tiles
        total_hand_score = sum(self.calculate_hand_score(player) for player in [self.human_player, self.bot_player_1])

        # Check if any player's tiles has 0 cards and set the corresponding score
        for player in [self.human_player, self.bot_player_1]:
            if len(player.hand) == 0:
                # The score of the player whose tiles is 0 is the sum of the scores of other players' tiles.
                self.game_manager.player_scores[player.name] = total_hand_score
            else:
                # The remaining player's score is the negative of his or her tiles score.
                self.game_manager.player_scores[player.name] = -self.calculate_hand_score(player)

    def calculate_hand_score(self, player: Player):
        # Calculate the score of a player's tiles
        score = 0
        for tile in player.hand:
            if isinstance(tile, JokerTile):
                score += 30
            else:
                score += tile.number
        return score
    
    def checkWinCondition(self):
        # Check if any player has won
        if len(self.human_player.hand) == 0:
            self.end_game(self.human_player.name)
        elif len(self.bot_player_1.hand) == 0:
            self.end_game(self.bot_player_1.name)

    def clean_up(self):
        # TODO: explicitly set all attributes to None and collect them
        # for now, we simply do nothing let python automatically manage memory.
        global SHOW_TILE_POOL
        SHOW_TILE_POOL = False

    def start(self):
        if not self.is_start:
            self.distribute_initial_tiles(14)
            self.is_start = True
            
            self.start_player_turn() # Start the first turn

    # notice: it's not actually restart, it's refresh(creating a new GamePlay class instance)
    def restart(self):
        self.game_manager.restart_game()

    def start_player_turn(self):
        self.current_player = self.human_player
        self.player_turn_completed = False
        self.main_board.tile_placed_this_turn = False
        self.is_confirm = False
        self.player_click_draw_button = False

        #record at the beginning
        self.player_tile_at_turn_beginning = copy.deepcopy(self.human_player.hand)
        self.main_board_tile_at_turn_beginning = copy.deepcopy(self.main_board.tiles)
        self.player_timer.start()

    def player_put_tile_on_board(self):
        # Placeholder function for player action to put a tile on the board
        self.player_turn_completed = True
        self.player_board.update_tile_positions()
    
    def start_bot_turn(self, bot_player):
        self.current_player = bot_player
        self.bot_turn_completed = False
        self.bot_perform_actions(bot_player)


    def bot_perform_actions(self, bot_player):
        if self.current_player != bot_player:
            print("not bot_player turn")
            return

        played = False
        for tile in bot_player.hand[:]:  # Use a copy of the list to avoid modifying the list during iteration
            if self.try_bot_play_tile(tile, bot_player, self.main_board):
                played = True
                print("Bot_player drew a tile")
                break

        if not played:
            print("Bot_player failed to play a tile and tried to draw a card")
            self.bot_draw_tile(bot_player)

        self.checkWinCondition()  # check the conditions of win
        self.end_bot_turn()

    def bot_draw_tile(self, bot_player):
        if self.tile_set.tiles:
            drawn_tile = self.tile_set.tiles.pop()
            bot_player.hand.append(drawn_tile)
            print(f"Bot_player draws a card: {drawn_tile.color} {drawn_tile.number}")
        else:
            print("There are no more tile in the pool")

    def try_bot_play_tile(self, tile, bot_player, main_board):
        # Identify existing combinations
        existing_combinations = self.identify_existing_combinations(main_board)

        # Try adding cards to both ends of an existing combination
        for combination in existing_combinations:
            if self.try_add_tile_to_combination(tile, bot_player, main_board, combination):
                return True

        return False

    def identify_existing_combinations(self, main_board):
        # Implement the logic to identify existing combinations on the mainboard
        combinations = []
        for row in range(main_board.board_height // main_board.tile_height):
            row_start = row * (main_board.board_width // main_board.tile_width)
            row_end = row_start + (main_board.board_width // main_board.tile_width)
            tiles_in_row = main_board.tiles[row_start:row_end]

            current_set = []
            for tile in tiles_in_row:
                if tile:
                    current_set.append(tile)
                elif current_set:
                    if main_board.check_specific_combination_valid(current_set):
                        combinations.append((current_set.copy(), row_start + tiles_in_row.index(current_set[0])))
                    current_set.clear()

        return combinations

    def try_add_tile_to_combination(self, tile, bot_player, main_board, combination):
        # Implement the logic of trying to add tiles to both ends of a combination
        combination_tiles, start_index = combination
        for offset in [-1, len(combination_tiles)]:
            index = start_index + offset
            if 0 <= index < len(main_board.tiles) and main_board.tiles[index] is None:
                if self.try_place_tile_at_index(tile, bot_player, main_board, index):
                    return True

        return False

    def try_place_tile_at_index(self, tile, bot_player, main_board, index):
        # Attempts to place a tile at the specified index
        original_tiles = main_board.tiles.copy()
        main_board.tiles[index] = tile
        if main_board.is_valid_board_state(self.first_time_check_main_board):
            bot_player.hand.remove(tile)
            main_board.tile_placed_this_turn = True
            return True
        else:
            main_board.tiles = original_tiles
            return False

    # end of the human player's turn, perform check
    def end_player_turn(self):
        # Logic to end the player's turn
        # Transition to AI turn or next player, and check win condition at the end stage of each player
        self.player_timer.reset()
        self.is_confirm = False
        self.player_clicked_regret_button = False

        if self.player_board.selected_tile is not None:
            self.player_board.selected_tile = None
            self.player_board.update_tile_positions()

        if self.main_board.selected_tile is not None:
            self.main_board.selected_tile = None

        if not self.is_choosing:
            self.start_next_player_turn()
            self.player_turn_completed = False

    # end of the bot player's turn, perform check
    def end_bot_turn(self):
        # Transition to the next player's turn, and check win condition at the end stage of each player
        self.checkWinCondition()
        self.bot_player_1_timer.reset()
        self.start_next_player_turn()    

    # start next player turn logic, may change if add more bot player
    def start_next_player_turn(self):
        # Logic to determine the next player (AI or human) and start their turn
        # ... logic for cycling through players ...
        if self.current_player == self.human_player:
            self.start_bot_turn(self.bot_player_1)
        elif self.current_player == self.bot_player_1:
            self.start_player_turn()
        # if has bot_player_2, round like human->bot1->bot2->human, etc.

    # callback function for button quit
    def quit(self):
        global SHOW_TILE_POOL
        SHOW_TILE_POOL = False
        self.game_manager.music_manager.stop_music()
        self.game_manager.switch_state(MainMenu)

    # callback function for button 777
    def order_by_color(self):
        self.human_player.sort_hand_by_color()
        self.player_board.update_tile_positions()

    # callback function for button 789
    def order_by_number(self):
        self.human_player.sort_hand_by_number()
        self.player_board.update_tile_positions()

    # callback function for button Display bot
    def toggle_display(self):
        self.is_displaying = not self.is_displaying

    def handle_events(self, events):
        for event in events:
            self.pause_button.handle_event(event)

            # when is not paused, process other events
            if not config.IS_PAUSED:
                self.display_button.handle_event(event)
                self.quit_button.handle_event(event)
                self.start_button.handle_event(event)
                self.pool_button.handle_event(event)

                if self.is_start:
                    # only if current player is human, player board can perform handle event
                    if self.current_player == self.human_player:
                        self.confirm_button.handle_event(event)
                        self.regret_button.handle_event(event)
                        self.player_board.handle_event(event, self.main_board)
                        
                        # First, check if we're clicking on the main board to select a tile
                        if not self.player_board.selected_tile:
                            # We don't have a selected tile from the player's hand, so we try to select from the main board
                            if self.main_board.handle_event(event, self.player_board, select_only = True):
                                # If a tile was selected from the board, skip the rest of the logic for this click
                                return

                        # If we have a selected tile from the player's hand, handle placing it on the main board
                        if self.player_board.selected_tile:
                            self.main_board.handle_event(event, self.player_board, select_only=False)

                    if self.current_player == self.bot_player_1:
                        pass
                    self.order_color_button.handle_event(event)
                    self.order_number_button.handle_event(event)
                    self.draw_button.handle_event(event)
                    self.restart_button.handle_event(event)
                if self.choice_board:  # If the tile choice board exists, pass events to it
                    self.choice_board.handle_event(event)

    def draw(self):
        self.game_manager.screen.blit(self.game_manager.back_ground_image, (0, 0))
        
        # Draw buttons
        self.display_button.draw(self.game_manager.screen)
        self.quit_button.draw(self.game_manager.screen)
        self.pause_button.draw(self.game_manager.screen)
        self.start_button.draw(self.game_manager.screen)
        self.restart_button.draw(self.game_manager.screen)
        self.pool_button.draw(self.game_manager.screen)
        self.order_color_button.draw(self.game_manager.screen)
        self.order_number_button.draw(self.game_manager.screen)
        self.draw_button.draw(self.game_manager.screen)
        self.main_board.draw(self.game_manager.screen)
        self.confirm_button.draw(self.game_manager.screen)
        self.regret_button.draw(self.game_manager.screen)
        self.timer_text.draw(self.game_manager.screen)

        # Draw the board with the current tiles
        self.player_board.draw(self.game_manager.screen)

        if self.is_displaying:
            self.bot_board_1.draw(self.game_manager.screen)

        if self.choice_board:
            self.choice_board.draw(self.game_manager.screen)

        if SHOW_TILE_POOL:
            self.display_pool(self.game_manager.screen)

    def update(self):
        if config.IS_PAUSED:
            return
        
        # Check if the tileset has run out
        if not self.tile_set.tiles:
            self.end_game(None)
        
        # if current player is human
        if self.current_player == self.human_player:
            time_left = int(self.player_timer.get_time_left())
            self.timer_text.set_text(f"Player Time Left: {time_left} Second(s)") # display timer dynamically
            if time_left != self.last_printed_time:  # Only print when time changes
                # debug only
                print(f"human_player: {time_left}")
                self.last_printed_time = time_left

            # if click regret button and timer not expired
            if self.player_clicked_regret_button and not self.player_timer.is_expired():
                # Reset the main board and player's hand to their state at the beginning of the turn
                self.main_board.tiles = copy.deepcopy(self.main_board_tile_at_turn_beginning)
                self.human_player.hand = copy.deepcopy(self.player_tile_at_turn_beginning)
                # Reset the player's selected tile and update tile positions
                self.player_board.selected_tile = None
                self.player_board.update_tile_positions()
                self.main_board.selected_tile = None
                self.main_board.tile_placed_this_turn = False
                # Clear the flag for regret button click
                self.player_clicked_regret_button = False
                self.player_turn_completed == False
    
            # When time is not running out and player hasn't drawn tile from pool
            if not self.player_timer.is_expired() and self.player_turn_completed == False:
                # if click confirm button, enter the time running out check if-else condition immediately
                if self.is_confirm:
                    self.player_timer.expire_now()
                    self.player_turn_completed == False
                    
            # if player's time is expired and turn not completed
            if self.player_timer.is_expired() and self.player_turn_completed == False:
                # check if player has placed tile to main board
                if self.main_board.tile_placed_this_turn:
                    # check game rules, if meet, simply go next turn
                    if self.main_board.is_valid_board_state(self.first_time_check_main_board):
                        # debug only
                        if self.first_time_check_main_board:
                            print("got 30 marks or more for the first time!")
                        else:
                            print("no need to check 30 limit again, meet condition now!")
                        # if valid board state, check win and end player turn, no need to draw tile
                        self.first_time_check_main_board = False
                        self.checkWinCondition()
                        self.end_player_turn()
                    else:
                        # if not valid, force player to draw, then end turn
                        self.main_board.tiles = copy.deepcopy(self.main_board_tile_at_turn_beginning)
                        self.human_player.hand = copy.deepcopy(self.player_tile_at_turn_beginning)
                        self.draw_two_choose_one()
                        self.player_turn_completed = True
                # force player draw tile if not place, when time is running out
                else:
                    # if not place tile, not draw tile, time is running out, force to draw tile
                    self.draw_two_choose_one()
                    self.player_turn_completed = True

            # anytime if this bool is true, we end player's turn immediately
            if self.player_turn_completed == True or self.player_click_draw_button == True:
                self.end_player_turn()

        # if current player is not human
        elif isinstance(self.current_player, BotPlayer):
            time_left = int(self.bot_player_1_timer.get_time_left())
            self.timer_text.set_text(f"Bot1 Time Left: {time_left} Second(s)") # display timer dynamically
            if time_left != self.last_printed_time:  # Only print when time changes
                # debug only
                print(f"bot_player_1: {time_left}")
                self.last_printed_time = time_left

            if not self.bot_player_1_timer.is_expired():
                self.bot_perform_actions()

            if self.bot_player_1_timer.is_expired() or self.bot_turn_completed == True:
                self.end_bot_turn()

class GameOver(GameState):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.score_table = Table("Score Table", self.game_manager.player_scores,(GameOverConfig.TABLE_X, GameOverConfig.TABLE_Y), GameOverConfig.TABLE_WIDTH, GameOverConfig.TABLE_HEIGHT)
        self.title = Text("Score Table", GameOverConfig.TITLE_X, GameOverConfig.TITLE_Y, None, 48)
        self.restart_button = Button("Restart", GameOverConfig.RESTART_BUTTON_X, GameOverConfig.BUTTON_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.restart)
        self.back_to_menu_button = Button("Back to Menu", GameOverConfig.BACK_BUTTON_X, GameOverConfig.BUTTON_Y, ButtonConfig.WIDTH, ButtonConfig.HEIGHT, self.back_to_menu)

    def restart(self):
        self.game_manager.switch_state(GamePlay)

    def back_to_menu(self):
        self.game_manager.switch_state(MainMenu)

    def handle_events(self, events):
        for event in events:
            self.restart_button.handle_event(event)
            self.back_to_menu_button.handle_event(event)
    
    def update(self):
        pass

    def draw(self):
        self.game_manager.screen.blit(self.game_manager.back_ground_image, (0, 0))
        self.score_table.draw(self.game_manager.screen)
        self.title.draw(self.game_manager.screen)
        self.restart_button.draw(self.game_manager.screen)
        self.back_to_menu_button.draw(self.game_manager.screen)