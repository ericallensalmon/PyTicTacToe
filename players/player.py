"""Base Player module (for human and AI players)"""
from constants.playertoken import PlayerToken


class Player:
    """Base class for data and behavior common between all players"""
    def __init__(self, game, token: PlayerToken):
        self.thinking = False
        self.game = game
        self.token = token

    def select_target(self, position: int):
        """selects a cell on the game board using the player's token"""
        self.game.fill_cell(position, self.token)

    def move(self):
        """"""
        pass
