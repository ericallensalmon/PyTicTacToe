"""Normal AI opponent AI module"""
from players.ai.base import AI
from constants.playertoken import PlayerToken


class NormalAI(AI):
    """THe Normal AI is a standard opponent that should behave like an average human player"""
    def __init__(self, game, token: PlayerToken):
        super().__init__(game, token)

    def move(self):
        """On normal, the moves are mostly random, but the opponent will block you from completing 3"""
        self.thinking = True

        # first look for spaces that will get a win for AI
        target = self.get_winning_target()

        # next look for spaces to block opponent's imminent win
        if target == -1:
            target = self.get_blocking_target()

        # if a target isn't found, the base falls back to choosing randomly
        super().move(target)
