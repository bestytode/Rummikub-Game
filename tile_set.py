# Represent individual tiles and sets of tiles, respectively.
from config import TileConfig
from asset_manager import ImageManager

class Tile:
    def __init__(self, number, color: str, image_manager: ImageManager):
        self.number = number
        self.color = color
        self.image_manager = image_manager  # Save a reference to image_manager
        self.image = image_manager.get_image('tile')  # Use a common tile image


    def __deepcopy__(self, memo):
        # Create a new Tile object using the same number, color and image_manager
        new_tile = Tile(self.number, self.color, self.image_manager)
        # Copy image reference
        new_tile.image = self.image
        return new_tile


    def equals(self, other_tile):
        if not other_tile:
            return False
        return self.number == other_tile.number and self.color == other_tile.color
        
    def draw(self):
        # notice: draw logic for tile implementation in Board class
        pass

# important: define number as 0 for mapping.
class JokerTile(Tile):
    def __init__(self, image_manager: ImageManager):
        super().__init__(number = 0, color = 'joker', image_manager = image_manager)
        self.image = image_manager.get_image('joker')  # Unique image for the joker

class TileSet:
    def __init__(self, image_manager: ImageManager):
        self.image_manager = image_manager
        self.tiles = self.generate_tiles()
        self.shuffle()

    def generate_tiles(self):
        # 5 sets of 5 colors of 1-15, along with 4 joker tiles
        colors = ['red', 'green', 'blue', 'alpha', 'yellow']
        numbers = range(1, 16)
        tiles = [Tile(number, color, self.image_manager) for color in colors for number in numbers for _ in range(TileConfig.NUMBER)]
        tiles.extend([JokerTile(self.image_manager) for _ in range(TileConfig.JOKER_COUNT)])
        return tiles

    def add_tile(self, new_tile):
        self.tiles.append(new_tile)

    def shuffle(self):
        import random
        random.shuffle(self.tiles)

    def pop_two_for_selection(self) -> []:
        # Ensure there are at least two tiles to draw
        if len(self.tiles) >= 2:
            return [self.tiles.pop(), self.tiles.pop()]
        # If not enough tiles are available, return None or handle accordingly
        return None
    
    def show_current_pool(self):
        # Calculate the total count of tiles in the current pool
        total_tile_count = len(self.tiles)

        # Initialize counts
        tile_count = {color: {number: 0 for number in range(1, 16)} for color in ['red', 'green', 'blue', 'alpha', 'yellow']}
        tile_count['joker'] = 0

        # Count the tiles in the current pool
        for tile in self.tiles:
            if isinstance(tile, JokerTile):
                tile_count['joker'] += 1
            else:
                tile_count[tile.color][tile.number] += 1

        # Generate the display text
        pool_text = f"number of current tiles: {total_tile_count}\n"
        for number in range(1, 16):
            line = f"number{number}: "
            for color in ['red', 'green', 'blue', 'alpha', 'yellow']:
                if tile_count[color][number] > 0:
                    line += f"{color}({tile_count[color][number]}), "
            pool_text += line.rstrip(', ') + '\n'  # Remove the trailing comma and space

        # Add the joker count
        pool_text += f"joker: joker({tile_count['joker']})"

        return pool_text