"""Base AI opponent AI module"""
import random
from constants.playertoken import PlayerToken
from constants.position import Position
from players.player import Player


class AI(Player):
    """Base class for AIs with common functionality"""
    def __init__(self, game, token: PlayerToken):
        super().__init__(game, token)

    def move(self, target: int = -1):
        """Chooses a random move if one was not given by a subclass"""
        self.thinking = False
        if target == -1 or self.game.state[target] != '':
            target = self.get_random_target()
        self.select_target(target)
        super().move()

    def get_winning_target(self):
        """Finds any winning targets for the AI"""
        return self.get_completing_target(self.token)

    def get_blocking_target(self):
        """Finds any targets that would block AI's opponent from an imminent win"""
        if self.token == PlayerToken.X:
            return self.get_completing_target(PlayerToken.O)
        else:
            return self.get_completing_target(PlayerToken.X)

    def get_completing_target(self, token: PlayerToken) -> int:
        """Checks to see if any cell could lead to a win for the given token, and returns it (or -1 otherwise)"""
        tokenstr = token.value
        cell = -1

        # some quick aliases to make these a bit more readable
        state = self.game.state
        top_left = Position.TOP_LEFT
        top = Position.TOP_EDGE
        top_right = Position.TOP_RIGHT
        left = Position.LEFT_EDGE
        center = Position.CENTER
        right = Position.RIGHT_EDGE
        bottom_left = Position.BOTTOM_LEFT
        bottom = Position.BOTTOM_EDGE
        bottom_right = Position.BOTTOM_RIGHT

        # Top Row
        if state[top_left] == tokenstr and state[top] == tokenstr and state[top_right] == '':
            cell = top_right
        elif state[top_left] == tokenstr and state[top_right] == tokenstr and state[top] == '':
            cell = top
        elif state[top] == tokenstr and state[top_right] == tokenstr and state[top_left] == '':
            cell = top_left

        # Middle Row
        elif state[left] == tokenstr and state[center] == tokenstr and state[right] == '':
            cell = right
        elif state[left] == tokenstr and state[right] == tokenstr and state[center] == '':
            cell = center
        elif state[center] == tokenstr and state[right] == tokenstr and state[left] == '':
            cell = left

        # Bottom Row
        elif state[bottom_left] == tokenstr and state[bottom] == tokenstr and state[8] == '':
            cell = bottom_right
        elif state[bottom_left] == tokenstr and state[bottom_right] == tokenstr and state[bottom] == '':
            cell = bottom
        elif state[bottom] == tokenstr and state[bottom_right] == tokenstr and state[bottom_left] == '':
            cell = bottom_left

        # Left Column
        elif state[top_left] == tokenstr and state[left] == tokenstr and state[bottom_left] == '':
            cell = bottom_left
        elif state[top_left] == tokenstr and state[bottom_left] == tokenstr and state[left] == '':
            cell = left
        elif state[left] == tokenstr and state[bottom_left] == tokenstr and state[top_left] == '':
            cell = top_left

        # Center Column
        elif state[top] == tokenstr and state[center] == tokenstr and state[bottom] == '':
            cell = bottom
        elif state[top] == tokenstr and state[bottom] == tokenstr and state[center] == '':
            cell = center
        elif state[center] == tokenstr and state[bottom] == tokenstr and state[top] == '':
            cell = top

        # Right Column
        elif state[top_right] == tokenstr and state[right] == tokenstr and state[bottom_right] == '':
            cell = bottom_right
        elif state[top_right] == tokenstr and state[bottom_right] == tokenstr and state[right] == '':
            cell = right
        elif state[right] == tokenstr and state[bottom_right] == tokenstr and state[top_right] == '':
            cell = top_right

        # Dia 1
        elif state[top_left] == tokenstr and state[center] == tokenstr and state[bottom_right] == '':
            cell = bottom_right
        elif state[top_left] == tokenstr and state[bottom_right] == tokenstr and state[center] == '':
            cell = center
        elif state[center] == tokenstr and state[bottom_right] == tokenstr and state[top_left] == '':
            cell = top_left

        # Dia 2
        elif state[bottom_left] == tokenstr and state[center] == tokenstr and state[top_right] == '':
            cell = top_right
        elif state[bottom_left] == tokenstr and state[top_right] == tokenstr and state[center] == '':
            cell = center
        elif state[center] == tokenstr and state[top_right] == tokenstr and state[bottom_left] == '':
            cell = bottom_left

        return cell

    def get_random_target(self) -> int:
        """Gets a random cell on the game board"""
        cell = -1
        while cell == -1:
            rand = random.randrange(0, self.game.grid_size) \
                   * self.game.grid_size \
                   + random.randrange(0, self.game.grid_size)

            if self.game.state[rand] == '':
                cell = rand

        return cell
