# Abstracts a player, containing attributes and methods common to both human and AI players.

class Player:
    def __init__(self, name):
        self.hand = [] # The tiles currently in the player's hand
        self.name = name

    # notice: this function only collect 1 tile each time
    def draw_tile(self, tile_set):
        if tile_set.tiles:
            tile = tile_set.tiles.pop()
            self.hand.append(tile)

    def sort_hand_by_number(self):
        # Sort tiles by their number, placing Joker tiles (number = 0) at the beginning
        self.hand.sort(key = lambda tile: tile.number)

    def sort_hand_by_color(self):
        # Sort tiles by their color, placing Joker tiles at the beginning
        self.hand.sort(key=lambda tile: ('0' if tile.color == 'joker' else tile.color, tile.number))

class BotPlayer(Player):
    def __init__(self, name):
        super().__init__(name)