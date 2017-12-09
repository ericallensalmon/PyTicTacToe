"""Easy AI opponent AI module"""
from players.ai.base import AI
from constants.playertoken import PlayerToken


class EasyAI(AI):
    """The easy AI is a simple opponent that moves randomly"""
    def __init__(self, game, token: PlayerToken):
        super().__init__(game, token)
        pass

    def move(self):
        """On easy, the moves are completely random (handled below as a fallback for the other AI's)"""
        self.thinking = True
        target = -1
        # This falls through to the default behavior -- choose a random cell
        super().move(target)
