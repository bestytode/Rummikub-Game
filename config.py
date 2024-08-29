# Important global variables definitions, affecting any other .py file which reference any of them.

# Screen config
class ScreenConfig:
    WIDTH = 1200
    HEIGHT = 800

    # background color tuple
    BACKGROUND_COLOR = (173, 216, 230)

# UI button configs
class ButtonConfig:
    WIDTH = 150
    HEIGHT = 50

    # background and text color tuples
    BACKGROUND_COLOR = (0, 0, 0)
    TEXT_COLOR = (255, 255, 255)
    HOVER_COLOR = (100, 100, 100)
    
    # MainMenu button positions
    MAIN_PLAY_X = (ScreenConfig.WIDTH - WIDTH) / 2
    MAIN_PLAY_Y = (ScreenConfig.HEIGHT / 2) - (HEIGHT / 2)
    MAIN_SETTINGS_X = MAIN_PLAY_X
    MAIN_SETTINGS_Y = MAIN_PLAY_Y + HEIGHT + 20  # 20 is the spacing
    MAIN_QUIT_X = MAIN_PLAY_X
    MAIN_QUIT_Y = MAIN_SETTINGS_Y + HEIGHT + 20

    # Settings stage button positions
    SETTINGS_BACK_X = (ScreenConfig.WIDTH - WIDTH) / 2
    SETTINGS_BACK_Y = (ScreenConfig.HEIGHT - HEIGHT) / 2

    # GamePlay stage button positions
    BUTTON_START_Y = 20  # Starting y position for the buttons
    BUTTON_SPACING = 20  # Spacing between buttons

    # Calculate the x position once because all buttons have the same x position
    GAME_BUTTON_X = ScreenConfig.WIDTH - WIDTH - 50  # 50 pixels from the right edge of the screen

    # Define y positions for all buttons
    GAME_DISPLAY_Y = BUTTON_START_Y # display bot hand
    GAME_QUIT_Y = GAME_DISPLAY_Y + HEIGHT + BUTTON_SPACING# quit
    GAME_PAUSE_Y = GAME_QUIT_Y + HEIGHT + BUTTON_SPACING # pause/unpause
    GAME_START_Y = GAME_PAUSE_Y + HEIGHT + BUTTON_SPACING # start
    GAME_RESTART_Y = GAME_START_Y + HEIGHT + BUTTON_SPACING # restart
    GAME_POOL_Y = GAME_RESTART_Y + HEIGHT + BUTTON_SPACING  # show pool
    GAME_ORDER_COLOR_Y = GAME_POOL_Y + HEIGHT + BUTTON_SPACING  # 777
    GAME_ORDER_NUMBER_Y = GAME_ORDER_COLOR_Y + HEIGHT + BUTTON_SPACING  # 789
    GAME_DRAW_Y = GAME_ORDER_NUMBER_Y + HEIGHT + BUTTON_SPACING # draw tiles
    GAME_CONFIRM_Y = GAME_DRAW_Y + HEIGHT + BUTTON_SPACING # confirm play tile
    GAME_REGRET_Y = GAME_CONFIRM_Y + HEIGHT + BUTTON_SPACING # regret choice

# UI Tile configs
class TileConfig:
    WIDTH = 30 # important
    HEIGHT = 40 # important
    MARGIN = 10

    NUMBER = 5       # 5 sets of 1-15
    JOKER_COUNT = 4  # 4 jokers

# UI Board configs
class BoardConfig:
    WIDTH = 900
    HEIGHT = 150

    BORDER_COLOR = (255, 255, 0)            # border color for selected tile
    HUMAN_PLAYER_ORIGIN = (50, 650)        # player' board origin coords.
    BOT_PLAYER_1_ORIGIN = (200, 300)         # bot_player1's board origin coords.
    CHOICE_ORIGIN = (400, 600 - HEIGHT / 2) # TileChoiceBoard origin coords.

# UI Text config
class TextConfig:
    TEXT_COLOR = (255, 255, 255)
    FONT_SIZE = 24

    TIMER_X = 550
    TIMER_Y = 15
    TIMER_SIZE = 30
    TIMER_COLOR = (0, 0, 0)

class TimerConfig:
    PLAYER_TIME_LIMIT = 15
    BOT_PLAYER_1_TIME_LIMIT = 5


class MainBoardConfig:
    WIDTH = 900 # important
    HEIGHT = 600 # important

    ORIGIN = (100, 25)

class BorderConfig:
    WIDTH = 5
    COLOR = (20, 20, 20)

class SettingsConfig:
    # Define the initial vertical position and spacing of the control button
    START_Y = 100
    VERTICAL_SPACING = 20
    SLIDER_Y = START_Y + 50
    SELECT_TIME_BUTTON_Y = SLIDER_Y + 50 + VERTICAL_SPACING
    TIME_BUTTONS_Y = SELECT_TIME_BUTTON_Y + ButtonConfig.HEIGHT + VERTICAL_SPACING
    BACK_BUTTON_Y = TIME_BUTTONS_Y + 3 * ButtonConfig.HEIGHT + 2 * VERTICAL_SPACING

    # Calculate the horizontal center position of a control button
    CENTER_X = ScreenConfig.WIDTH // 2 - ButtonConfig.WIDTH // 2

class GameOverConfig:
    TITLE_X = ScreenConfig.WIDTH // 2
    TITLE_Y = 60

    TABLE_X = (ScreenConfig.WIDTH - 600) // 2  # Centered horizontally (600 is the table width)
    TABLE_Y = TITLE_Y + 50 + 20  # Below the title with some gap (50 is an assumed title height)
    TABLE_WIDTH = 600
    TABLE_HEIGHT = 450

    BUTTON_Y = 600
    RESTART_BUTTON_X = 430
    BACK_BUTTON_X = RESTART_BUTTON_X + 170

# Global state variables (use sparingly)
IS_PAUSED = False
SHOW_TILE_POOL = False