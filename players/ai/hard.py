"""Hard AI opponent AI module"""
from players.ai.base import AI
from constants.playertoken import PlayerToken
from constants.position import Position
import random


class HardAI(AI):
    """The Hard AI takes near-optimum moves and should always at least tie the player (unbeatable)"""
    def __init__(self, game, token: PlayerToken):
        self._current_strategy = ''
        super().__init__(game, token)

    def move(self):
        """On hard, the opponent will choose the best possible move. The house always wins."""
        self.thinking = True
        
        opponent_token = PlayerToken.O.value if self.token == PlayerToken.X else PlayerToken.X.value
        target = self.get_winning_target()
        if target == -1:
            target = self.get_blocking_target()

        if target == -1:
            player_moves = []
            move_number = 1
            # TODO: there's most likely a more clever way to handle iterations in Python, KISS for now
            for i in range(len(self.game.state)):
                state = self.game.state[i]
                if state != '':
                    move_number += 1
                    if state == opponent_token:
                        player_moves.append(i)
            # noinspection PyBroadException
            try:
                if move_number == 1:
                    target = self.first_move()

                elif move_number == 2:
                    target = self.second_move(player_moves[0])

                elif move_number == 3:
                    target = self.third_move(player_moves[0])

                elif move_number == 4:
                    target = self.fourth_move(player_moves[0], player_moves[1])

                elif move_number == 5:
                    target = self.fifth_move()
            except Exception:
                target = -1

        super().move(target)

    def first_move(self) -> int:
        """ First move - choose randomly between corner and center.
            Corner is actually a stronger play, but -- for fun -- let the AI choose center sometimes
            """
        strategy = random.randint(1, 5)

        # center
        if strategy == 1:
            self._current_strategy = '1'
            return Position.CENTER

        # top-left
        elif strategy == 2:
            self._current_strategy = '2a'
            return Position.TOP_LEFT

        # top-right
        elif strategy == 3:
            self._current_strategy = '2b'
            return Position.TOP_RIGHT

        # bottom-left
        elif strategy == 4:
            self._current_strategy = '2c'
            return Position.BOTTOM_LEFT

        # bottom-right
        elif strategy == 5:
            self._current_strategy = '2d'
            return Position.BOTTOM_RIGHT

        return -1

    def second_move(self, player_move: int) -> int:
        """ Second move - this is the AI's first move, and it's reacting to the player's move"""
        ########################################################################################################
        # if the Player's first move is the center, AI moves to any corner
        if player_move == Position.CENTER:
            strategy = random.randint(1, 4)

            # top-left
            if strategy == 1:
                self._current_strategy = '3a'
                return Position.TOP_LEFT

            # top-right
            elif strategy == 2:
                self._current_strategy = '3b'
                return Position.TOP_RIGHT

            # bottom-left
            elif strategy == 3:
                self._current_strategy = '3c'
                return Position.BOTTOM_LEFT

            # bottom-right
            elif strategy == 4:
                self._current_strategy = '3d'
                return Position.BOTTOM_RIGHT

        ########################################################################################################

        ########################################################################################################
        # if the Player's first move is a corner, AI moves to center
        elif player_move == Position.TOP_LEFT:
            self._current_strategy = '4a'
            return Position.CENTER

        elif player_move == Position.TOP_RIGHT:
            self._current_strategy = '4b'
            return Position.CENTER

        elif player_move == Position.BOTTOM_LEFT:
            self._current_strategy = '4c'
            return Position.CENTER

        elif player_move == Position.BOTTOM_RIGHT:
            self._current_strategy = '4d'
            return Position.CENTER

        ########################################################################################################

        ########################################################################################################
        # if the Player's first move is an edge, AI takes an adjacent corner (next move will take center)

        # top
        elif player_move == Position.TOP_EDGE:
            strategy = random.randint(1, 2)

            # top-left
            if strategy == 1:
                self._current_strategy = '5a-a'
                return Position.TOP_LEFT

            # top-right
            elif strategy == 2:
                self._current_strategy = '5a-b'
                return Position.TOP_RIGHT

        # left
        elif player_move == Position.LEFT_EDGE:
            strategy = random.randint(1, 2)

            # top-left
            if strategy == Position.TOP_EDGE:
                self._current_strategy = '5b-a'
                return Position.TOP_LEFT

            # bottom-left
            elif strategy == 2:
                self._current_strategy = '5b-b'
                return Position.BOTTOM_LEFT

        # right
        elif player_move == Position.RIGHT_EDGE:
            strategy = random.randint(1, 2)

            # top-right
            if strategy == Position.TOP_EDGE:
                self._current_strategy = '5c-a'
                return Position.TOP_RIGHT

            # bottom-right
            elif strategy == 2:
                self._current_strategy = '5c-b'
                return Position.BOTTOM_RIGHT

        # bottom
        elif player_move == Position.BOTTOM_EDGE:
            strategy = random.randint(1, 2)

            # bottom-left
            if strategy == 1:
                self._current_strategy = '5d-a'
                return Position.BOTTOM_LEFT

            # bottom-right
            elif strategy == 2:
                self._current_strategy = '5d-b'
                return Position.BOTTOM_RIGHT

        ########################################################################################################

        return -1

    def third_move(self, player_move: int) -> int:
        """ Third move - this is the AI's second move"""
        ################################################################################################################
        # AI took the center
        if self._current_strategy == '1':

            ########################################################################################################
            # if Player took an edge, now the AI will take a corner that forces Player to take 2 in a row
            # this should lead to an automatic win via the base cases

            # top
            if player_move == Position.TOP_EDGE:
                self._current_strategy = '1-a'
                return Position.BOTTOM_LEFT

            # left
            elif player_move == Position.LEFT_EDGE:
                self._current_strategy = '1-b'
                return Position.BOTTOM_RIGHT

            # right
            elif player_move == Position.RIGHT_EDGE:
                self._current_strategy = '1-c'
                return Position.TOP_LEFT

            # bottom
            elif player_move == Position.BOTTOM_EDGE:
                self._current_strategy = '1-d'
                return Position.TOP_RIGHT

            ########################################################################################################

            ########################################################################################################
            # if Player took a corner, the AI takes the the opposite corner, try to force an error

            # top-left
            if player_move == Position.TOP_LEFT:
                self._current_strategy = '1-e'
                return Position.BOTTOM_RIGHT

            # top-right
            elif player_move == Position.TOP_RIGHT:
                self._current_strategy = '1-f'
                return Position.BOTTOM_LEFT

            # bottom-left
            elif player_move == Position.BOTTOM_LEFT:
                self._current_strategy = '1-g'
                return Position.TOP_RIGHT

            # bottom-right
            elif player_move == Position.BOTTOM_RIGHT:
                self._current_strategy = '1-h'
                return Position.TOP_LEFT

            ########################################################################################################

        ################################################################################################################

        ################################################################################################################
        # AI took the top-left corner
        elif self._current_strategy == '2a':

            ########################################################################################################
            # if Player took an edge, next move go for center (then go for the corner that makes 2 possible)

            # top
            if player_move == Position.TOP_EDGE:
                self._current_strategy == '2a-a'
                return Position.CENTER

            # left
            elif player_move == Position.LEFT_EDGE:
                self._current_strategy == '2a-b'
                return Position.CENTER

            # right
            elif player_move == Position.RIGHT_EDGE:
                self._current_strategy == '2a-c'
                return Position.CENTER

            # bottom
            elif player_move == Position.BOTTOM_EDGE:
                self._current_strategy == '2a-d'
                return Position.CENTER

            ########################################################################################################
            # if Player took a corner, next move take any corner, then get the last corner for win
            # top-left
            elif player_move == 2:
                self._current_strategy == '2a-e'
                return Position.BOTTOM_LEFT

            # bottom-left
            elif player_move == Position.BOTTOM_LEFT:
                self._current_strategy == '2a-f'
                return Position.BOTTOM_RIGHT

            # bottom-right
            elif player_move == Position.BOTTOM_RIGHT:
                self._current_strategy == '2a-g'
                return Position.TOP_RIGHT

            ########################################################################################################

            ########################################################################################################
            # if Player took center, take opposite corner, try to force an error (if Player takes corner, win)
            elif player_move == Position.CENTER:
                self._current_strategy == '2a-h'
                return Position.BOTTOM_RIGHT

            ########################################################################################################

        ################################################################################################################

        ################################################################################################################
        # AI took the top-right corner
        elif self._current_strategy == '2b':

            ########################################################################################################
            # if Player takes an edge,  next move go for center (then go for the corner that makes 2 possible)

            # top
            if player_move == Position.TOP_EDGE:
                self._current_strategy == '2b-a'
                return Position.CENTER

            # left
            elif player_move == Position.LEFT_EDGE:
                self._current_strategy == '2b-b'
                return Position.CENTER

            # right
            elif player_move == Position.RIGHT_EDGE:
                self._current_strategy == '2b-c'
                return Position.CENTER

            # bottom
            elif player_move == Position.BOTTOM_EDGE:
                self._current_strategy == '2b-d'
                return Position.CENTER

            ########################################################################################################

            ########################################################################################################
            # if Player takes corner, next move any corner, then get the last corner for win

            # top-left
            elif player_move == 0:
                self._current_strategy == '2b-e'
                return Position.BOTTOM_RIGHT

            # bottom-left
            elif player_move == Position.BOTTOM_LEFT:
                self._current_strategy == '2b-f'
                return Position.TOP_LEFT

            # bottom-right
            elif player_move == Position.BOTTOM_RIGHT:
                self._current_strategy == '2b-h'
                return Position.BOTTOM_LEFT

            ########################################################################################################
            # if Player takes center, take opposite corner, try to force an error (if Player is in corner, win)
            elif player_move == Position.CENTER:
                self._current_strategy == '2b-h'
                return Position.BOTTOM_LEFT

            ########################################################################################################

        ################################################################################################################

        ################################################################################################################
        # AI took the bottom-left corner
        elif self._current_strategy == '2c':

            ########################################################################################################
            # if Player takes edge,  next move go for center (then go for the corner that makes 2 possible)

            # top
            if player_move == Position.TOP_EDGE:
                self._current_strategy == '2c-a'
                return Position.CENTER

            # left
            elif player_move == Position.LEFT_EDGE:
                self._current_strategy == '2c-b'
                return Position.CENTER

            # right
            elif player_move == Position.RIGHT_EDGE:
                self._current_strategy == '2c-c'
                return Position.CENTER

            # bottom
            elif player_move == Position.BOTTOM_EDGE:
                self._current_strategy == '2c-d'
                return Position.CENTER

            ########################################################################################################
            # if Player takes corner,  next move any corner, then get the last corner for win

            # top-left
            elif player_move == Position.TOP_LEFT:
                self._current_strategy == '2c-e'
                return Position.BOTTOM_RIGHT

            # top-right
            elif player_move == Position.TOP_RIGHT:
                self._current_strategy == '2c-f'
                return Position.TOP_LEFT

            # bottom-right
            elif player_move == Position.BOTTOM_RIGHT:
                self._current_strategy == '2c-g'
                return Position.TOP_RIGHT

            ########################################################################################################

            ########################################################################################################
            # if Player takes center, take opposite corner, try to force an error (if Player is in corner, win)
            elif player_move == Position.CENTER:
                self._current_strategy == '2c-h'
                return Position.TOP_RIGHT

            ########################################################################################################

        ################################################################################################################

        ################################################################################################################
        # AI took the bottom-right corner
        elif self._current_strategy == '2d':

            ########################################################################################################
            # if Player takes edge, next move go for center (then go for the corner that makes 2 possible)
            # top
            if player_move == Position.TOP_EDGE:
                self._current_strategy == '2d-a'
                return Position.CENTER
            # left
            elif player_move == Position.LEFT_EDGE:
                self._current_strategy == '2d-b'
                return Position.CENTER
            # right
            elif player_move == Position.RIGHT_EDGE:
                self._current_strategy == '2d-c'
                return Position.CENTER
            # bottom
            elif player_move == Position.BOTTOM_EDGE:
                self._current_strategy == '2d-d'
                return Position.CENTER

            ########################################################################################################

            ########################################################################################################
            # if Player takes corner, next move any corner, then get the last corner for win
            # top-left
            elif player_move == Position.TOP_LEFT:
                self._current_strategy == '2d-g'
                return Position.TOP_RIGHT
            # top-right
            elif player_move == Position.TOP_RIGHT:
                self._current_strategy == '2d-e'
                return Position.BOTTOM_LEFT
            # bottom-left
            elif player_move == Position.BOTTOM_LEFT:
                self._current_strategy == '2d-f'
                return Position.TOP_LEFT

            ########################################################################################################

            ########################################################################################################
            # if Player takes center, take opposite corner, try to force an error (if Player is in corner, win)
            elif player_move == Position.CENTER:
                self._current_strategy == '2d-h'
                return Position.TOP_LEFT

            ########################################################################################################

        ################################################################################################################

        return -1

    def fourth_move(self, player_move_1: int, player_move_2: int) -> int:
        """Fourth move - this is the AI's second move"""
        ################################################################################################################
        # Player's first move was to the center
        # AI moved to a corner
        # if the Player moved anywhere except the opposite corner, this won't be hit (AI will block)
        # but we'll handle that case in particular -- move to any available corner
        if self._current_strategy == '3a' or self._current_strategy == '3b' or \
                self._current_strategy == '3c' or self._current_strategy == '3d':

            # find the first empty corner
            if self.game.state[Position.TOP_LEFT] == '':
                return Position.TOP_LEFT
            elif self.game.state[Position.TOP_RIGHT] == '':
                return Position.TOP_RIGHT
            elif self.game.state[Position.BOTTOM_LEFT] == '':
                return Position.BOTTOM_LEFT
            elif self.game.state[Position.BOTTOM_RIGHT] == '':
                return Position.BOTTOM_RIGHT

        ################################################################################################################

        ################################################################################################################
        # Player's first move is a corner
        # AI played to center
        elif self._current_strategy == '4a' or self._current_strategy == '4b' or \
                self._current_strategy == '4c' or self._current_strategy == '4d':

            # if the Player's next move was a corner, play any edge
            if (player_move_1 == Position.TOP_LEFT or player_move_1 == Position.TOP_RIGHT
                or player_move_1 == Position.BOTTOM_LEFT or player_move_1 == Position.BOTTOM_RIGHT) \
                    and (player_move_2 == Position.TOP_LEFT or player_move_2 == Position.TOP_RIGHT
                         or player_move_2 == Position.BOTTOM_LEFT or player_move_2 == Position.BOTTOM_RIGHT):
                return Position.TOP_EDGE

            # if the Player's next move was an edge, play any remaining corner
            else:
                # find first empty corner
                if self.game.state[0] == '':
                    return Position.TOP_LEFT;
                elif self.game.state[2] == '':
                    return Position.TOP_RIGHT;
                elif self.game.state[Position.BOTTOM_LEFT] == '':
                    return Position.BOTTOM_LEFT;
                elif self.game.state[Position.BOTTOM_RIGHT] == '':
                    return Position.BOTTOM_RIGHT;

        ################################################################################################################

        ################################################################################################################
        # Player's first move was to the edge
        # AI moved to an adjacent corner
        # now AI moves to center
        elif self._current_strategy == '5a-a' or self._current_strategy == '5a-b' or \
                self._current_strategy == '5b-a' or self._current_strategy == '5b-b' or \
                self._current_strategy == '5c-a' or self._current_strategy == '5c-b' or \
                self._current_strategy == '5d-a' or self._current_strategy == '5d-b':
            self._current_strategy == self._current_strategy + '-a'
            return Position.CENTER

        ################################################################################################################

        return -1

    def fifth_move(self) -> int:
        """Fifth move - this is the AI's third move"""

        ################################################################################################################
        # AI took the top-left corner
        # Player took an edge
        # AI took center (Player forced to take bottom-right corner)
        # AI takes corner that gives 2 possibilities

        # Player took top edge
        # AI takes bottom-left
        if self._current_strategy == '2a-a':
            return Position.BOTTOM_LEFT

        # Player took left edge
        # AI takes top-right
        elif self._current_strategy == '2a-b':
            return Position.TOP_RIGHT

        ################################################################################################################

        ################################################################################################################
        # AI took the top-left corner
        # Player took another corner
        # AI took another corner, forcing Player to block
        # AI takes the last corner, forcing win

        # top-left, now bottom-right
        elif self._current_strategy == '2a-e':
            return Position.BOTTOM_RIGHT
        # bottom-left, now top-right
        elif self._current_strategy == '2a-f':
            return Position.TOP_RIGHT
        # bottom-right, now bottom-left
        elif self._current_strategy == '2a-g':
            return Position.BOTTOM_LEFT

        ################################################################################################################

        ################################################################################################################
        # AI took the top-right corner
        # Player took an edge
        # AI took center (Player forced to take bottom-left corner)
        # AI takes corner that gives 2 possibilities

        # Player took top edge
        # AI takes bottom-right
        elif self._current_strategy == '2b-a':
            return Position.BOTTOM_RIGHT

        # Player took right edge
        # AI takes top-left
        elif self._current_strategy == '2b-c':
            return Position.TOP_LEFT

        ################################################################################################################

        ################################################################################################################
        # AI took the top-right corner
        # Player took another corner
        # AI took another corner, forcing Player to block
        # AI takes the last corner, forcing win

        # top-left, now bottom-left
        elif self._current_strategy == '2b-e':
            return Position.BOTTOM_LEFT

        # bottom-left, now bottom-right
        elif self._current_strategy == '2b-f':
            return Position.BOTTOM_RIGHT

        # bottom-right, now top-left
        elif self._current_strategy == '2b-h':
            return Position.TOP_LEFT

        ################################################################################################################

        ################################################################################################################
        # AI took the bottom-left corner
        # Player took an edge
        # AI took center (Player forced to take top-right corner)
        # AI takes corner that gives 2 possibilities

        # Player took left edge
        # AI takes bottom-right
        elif self._current_strategy == '2c-b':
            return Position.BOTTOM_RIGHT

        # Player took bottom edge
        # AI takes bottom-right
        elif self._current_strategy == '2c-d':
            return Position.TOP_LEFT

        ################################################################################################################

        ################################################################################################################
        # AI took the bottom-left corner
        # Player took another corner
        # AI took another corner, forcing Player to block
        # AI takes the last corner, forcing win

        # top-left
        elif self._current_strategy == '2c-e':
            return Position.TOP_RIGHT
        # top-right
        elif self._current_strategy == '2c-f':
            return Position.BOTTOM_RIGHT
        # bottom-right
        elif self._current_strategy == '2c-g':
            return Position.TOP_LEFT

        ################################################################################################################

        ################################################################################################################
        # AI took the bottom-right corner
        # Player took an edge
        # AI took center (Player forced to take top-left corner)
        # AI takes corner that gives 2 possibilities

        # Player took right edge
        # AI takes top-right
        elif self._current_strategy == '2d-c':
            return Position.BOTTOM_LEFT

        # Player took bottom edge
        # AI takes top-right
        elif self._current_strategy == '2d-d':
            return Position.TOP_RIGHT

        ################################################################################################################

        ################################################################################################################
        # AI took the bottom-right corner
        # Player took another corner
        # AI took another corner, forcing Player to block
        # AI takes the last corner, forcing win

        # top-left, now bottom-left
        elif self._current_strategy == '2d-g':
            return Position.BOTTOM_LEFT

        # top-right, now top-left
        elif self._current_strategy == '2d-e':
            return Position.TOP_LEFT

        # bottom-left, now top-right
        elif self._current_strategy == '2d-f':
            return Position.TOP_RIGHT

        ################################################################################################################

        return -1
