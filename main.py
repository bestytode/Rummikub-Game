# Rummikub Game group project
# The entry point of the game. Initializes the game and contains the main game loop.

# changes compared to the origin Rummikub game:
# 1. numbered as 1-15 but not 1-13
# 2. five colors of tile, not four (and therefore a “group” can consist of 3-5 tiles)
# 3. Runs are redefined as sequences of successive odd or even tiles of the same color. (important!)
#    So, for example, blue 3,5,7,9 and red 6,8,10 are runs, but green 2,3,4,5 is not a run
# 4. When drawing a tile from the pool, choosing two, one to add to your rack, return another one

import pygame

from config import ScreenConfig, TileConfig
from game_manager import GameManager
from asset_manager import ImageManager, MusicManager

# init
pygame.init()

screen = pygame.display.set_mode((ScreenConfig.WIDTH, ScreenConfig.HEIGHT), 0) 
pygame.display.set_caption("Rummikub Game") 
image_manager = ImageManager()
image_manager.load_image('tile', 'assets/images/logo.png') 
image_manager.load_image('joker', 'assets/images/joker.jpg') 
image_manager.load_image("BackGround", 'assets/images/BackGround.png')
image_manager.scale_image("BackGround", (ScreenConfig.WIDTH, ScreenConfig.HEIGHT))
image_manager.scale_image('tile', (TileConfig.WIDTH, TileConfig.HEIGHT))
image_manager.scale_image('joker', (TileConfig.WIDTH, TileConfig.HEIGHT))
music_manager = MusicManager()
music_manager.load_music('MainPageBGM','assets/images/FA.mp3')
music_manager.load_music('GamePlayBGM','assets/images/FF.mp3')
clock = pygame.time.Clock()

game_manager = GameManager(screen, image_manager, music_manager) 

# main loop
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
        game_manager.handle_events(events)
        
        # debug only
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game_manager.current_state.human_player.hand.clear()
            elif event.key == pygame.K_w:
                game_manager.current_state.bot_player_1.hand.clear()

    game_manager.update()    
    game_manager.draw()
    pygame.display.flip()

    # fix to 60 fps
    clock.tick(60) 

# quit when running is false
pygame.quit()