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

            ############################################################################################################
            # if this is the very first move, choose randomly between corner and center
            # corner is actually a stronger play, but -- for fun -- let the AI choose center sometimes
            if move_number == 1:
                strategy = random.randint(1, 5)

                # center
                if strategy == 1:
                    self._current_strategy = '1'
                    target = Position.CENTER

                # top-left
                elif strategy == 2:
                    self._current_strategy = '2a'
                    target = Position.TOP_LEFT

                # top-right
                elif strategy == 3:
                    self._current_strategy = '2b'
                    target = Position.TOP_RIGHT

                # bottom-left
                elif strategy == 4:
                    self._current_strategy = '2c'
                    target = Position.BOTTOM_LEFT

                # bottom-right
                elif strategy == 5:
                    self._current_strategy = '2d'
                    target = Position.BOTTOM_RIGHT

            ############################################################################################################

            ############################################################################################################
            # second move - this is the AI's first move, and it's reacting to the player's move
            elif move_number == 2:

                ########################################################################################################
                # if the player's first move is the center
                if player_moves[0] == Position.CENTER:
                    # ai moves to any corner
                    strategy = random.randint(1, 4)

                    # top-left
                    if strategy == 1:
                        self._current_strategy = '3a'
                        target = Position.TOP_LEFT

                    # top-right
                    elif strategy == 2:
                        self._current_strategy = '3b'
                        target = Position.TOP_RIGHT

                    # bottom-left
                    elif strategy == 3:
                        self._current_strategy = '3c'
                        target = Position.BOTTOM_LEFT

                    # bottom-right
                    elif strategy == 4:
                        self._current_strategy = '3d'
                        target = Position.BOTTOM_RIGHT

                ########################################################################################################

                ########################################################################################################
                # if the player's first move is a corner, ai moves to center
                elif player_moves[0] == Position.TOP_LEFT:
                    self._current_strategy = '4a'
                    target = Position.CENTER

                elif player_moves[0] == 2:
                    self._current_strategy = '4b'
                    target = Position.CENTER

                elif player_moves[0] == Position.BOTTOM_LEFT:
                    self._current_strategy = '4c'
                    target = Position.CENTER

                elif player_moves[0] == Position.BOTTOM_RIGHT:
                    self._current_strategy = '4d'
                    target = Position.CENTER

                ########################################################################################################

                ########################################################################################################
                # if the player's first move is an edge, take an adjacent corner (next move will take center)

                # top
                elif player_moves[0] == Position.TOP_EDGE:
                    strategy = random.randint(1, 2)

                    # top-left
                    if strategy == 1:
                        self._current_strategy = '5a-a'
                        target = Position.TOP_LEFT

                    # top-right
                    elif strategy == 2:
                        self._current_strategy = '5a-b'
                        target = Position.TOP_RIGHT

                # left
                elif player_moves[0] == Position.LEFT_EDGE:
                    strategy = random.randint(1, 2)

                    # top-left
                    if strategy == Position.TOP_EDGE:
                        self._current_strategy = '5b-a'
                        target = Position.TOP_LEFT

                    # bottom-left
                    elif strategy == 2:
                        self._current_strategy = '5b-b'
                        target = Position.BOTTOM_LEFT

                # right
                elif player_moves[0] == Position.RIGHT_EDGE:
                    strategy = random.randint(1, 2)

                    # top-right
                    if strategy == Position.TOP_EDGE:
                        self._current_strategy = '5c-a'
                        target = Position.TOP_RIGHT

                    # bottom-right
                    elif strategy == 2:
                        self._current_strategy = '5c-b'
                        target = Position.BOTTOM_RIGHT

                # bottom
                elif player_moves[0] == Position.BOTTOM_EDGE:
                    strategy = random.randint(1, 2)

                    # bottom-left
                    if strategy == Position.TOP_EDGE:
                        self._current_strategy = '5d-a'
                        target = Position.BOTTOM_LEFT

                    # bottom-right
                    elif strategy == 2:
                        self._current_strategy = '5d-b'
                        target = Position.BOTTOM_RIGHT

                ########################################################################################################

            ############################################################################################################

            ############################################################################################################
            # third move - ai's second move
            elif move_number == 3:

                ########################################################################################################
                # AI took the center
                if self._current_strategy == '1':

                    ####################################################################################################
                    # if player took an edge, now the AI will take a corner that forces player to take 2 in a row
                    # this should lead to an automatic win via the base cases

                    # top
                    if player_moves[0] == Position.TOP_EDGE:
                        self._current_strategy = '1-a'
                        target = Position.BOTTOM_LEFT

                    # left
                    elif player_moves[0] == Position.LEFT_EDGE:
                        self._current_strategy = '1-b'
                        target = Position.BOTTOM_RIGHT

                    # right
                    elif player_moves[0] == Position.RIGHT_EDGE:
                        self._current_strategy = '1-c'
                        target = Position.TOP_LEFT

                    # bottom
                    elif player_moves[0] == Position.BOTTOM_EDGE:
                        self._current_strategy = '1-d'
                        target = Position.TOP_RIGHT

                    ####################################################################################################

                    ####################################################################################################
                    # if player took a corner, the AI takes the the opposite corner, try to force an error

                    # top-left
                    if player_moves[0] == Position.TOP_LEFT:
                        self._current_strategy = '1-e'
                        target = Position.BOTTOM_RIGHT

                    # top-right
                    elif player_moves[0] == Position.TOP_RIGHT:
                        self._current_strategy = '1-f'
                        target = Position.BOTTOM_LEFT

                    # bottom-left
                    elif player_moves[0] == Position.BOTTOM_LEFT:
                        self._current_strategy = '1-g'
                        target = Position.TOP_RIGHT

                    # bottom-right
                    elif player_moves[0] == Position.BOTTOM_RIGHT:
                        self._current_strategy = '1-h'
                        target = Position.TOP_LEFT

                    ####################################################################################################

                ########################################################################################################

                ########################################################################################################
                # AI took the top-left corner
                elif self._current_strategy == '2a':

                    ####################################################################################################
                    # if player took an edge, next move go for center (then go for the corner that makes 2 possible)

                    # top
                    if player_moves[0] == Position.TOP_EDGE:
                        self._current_strategy == '2a-a'
                        target = Position.CENTER

                    # left
                    elif player_moves[0] == Position.LEFT_EDGE:
                        self._current_strategy == '2a-b'
                        target = Position.CENTER

                    # right
                    elif player_moves[0] == Position.RIGHT_EDGE:
                        self._current_strategy == '2a-c'
                        target = Position.CENTER

                    # bottom
                    elif player_moves[0] == Position.BOTTOM_EDGE:
                        self._current_strategy == '2a-d'
                        target = Position.CENTER

                    ####################################################################################################
                    # if player took a corner, next move take any corner, then get the last corner for win
                    # top-left
                    elif player_moves[0] == 2:
                        self._current_strategy == '2a-e'
                        target = Position.BOTTOM_LEFT

                    # bottom-left
                    elif player_moves[0] == Position.BOTTOM_LEFT:
                        self._current_strategy == '2a-f'
                        target = Position.BOTTOM_RIGHT

                    # bottom-right
                    elif player_moves[0] == Position.BOTTOM_RIGHT:
                        self._current_strategy == '2a-g'
                        target = Position.TOP_RIGHT

                    ####################################################################################################

                    ####################################################################################################
                    # if player took center, take opposite corner, try to force an error (if player takes corner, win)
                    elif player_moves[0] == Position.CENTER:
                        self._current_strategy == '2a-h'
                        target = Position.BOTTOM_RIGHT

                    ####################################################################################################

                ########################################################################################################

                ########################################################################################################
                # AI took the top-right corner
                elif self._current_strategy == '2b':

                    ####################################################################################################
                    # if player takes an edge,  next move go for center (then go for the corner that makes 2 possible)

                    # top
                    if player_moves[0] == Position.TOP_EDGE:
                        self._current_strategy == '2b-a'
                        target = Position.CENTER

                    # left
                    elif player_moves[0] == Position.LEFT_EDGE:
                        self._current_strategy == '2b-b'
                        target = Position.CENTER

                    # right
                    elif player_moves[0] == Position.RIGHT_EDGE:
                        self._current_strategy == '2b-c'
                        target = Position.CENTER

                    # bottom
                    elif player_moves[0] == Position.BOTTOM_EDGE:
                        self._current_strategy == '2b-d'
                        target = Position.CENTER

                    ####################################################################################################

                    ####################################################################################################
                    # if player takes corner, next move any corner, then get the last corner for win

                    # top-left
                    elif player_moves[0] == 0:
                        self._current_strategy == '2b-e'
                        target = Position.BOTTOM_RIGHT

                    # bottom-left
                    elif player_moves[0] == Position.BOTTOM_LEFT:
                        self._current_strategy == '2b-f'
                        target = Position.TOP_LEFT

                    # bottom-right
                    elif player_moves[0] == Position.BOTTOM_RIGHT:
                        self._current_strategy == '2b-h'
                        target = Position.BOTTOM_LEFT

                    ####################################################################################################
                    # if player takes center, take opposite corner, try to force an error (if player is in corner, win)
                    elif player_moves[0] == Position.CENTER:
                        self._current_strategy == '2b-h'
                        target = Position.BOTTOM_LEFT

                    ####################################################################################################

                ########################################################################################################
                # AI took the bottom-left corner
                elif self._current_strategy == '2c':

                    ####################################################################################################
                    # if player takes edge,  next move go for center (then go for the corner that makes 2 possible)

                    # top
                    if player_moves[0] == Position.TOP_EDGE:
                        self._current_strategy == '2c-a'
                        target = Position.CENTER

                    # left
                    elif player_moves[0] == Position.LEFT_EDGE:
                        self._current_strategy == '2c-b'
                        target = Position.CENTER

                    # right
                    elif player_moves[0] == Position.RIGHT_EDGE:
                        self._current_strategy == '2c-c'
                        target = Position.CENTER

                    # bottom
                    elif player_moves[0] == Position.BOTTOM_EDGE:
                        self._current_strategy == '2c-d'
                        target = Position.CENTER

                    ####################################################################################################
                    # if player takes corner,  next move any corner, then get the last corner for win

                    # top-left
                    elif player_moves[0] == Position.TOP_LEFT:
                        self._current_strategy == '2c-e'
                        target = Position.BOTTOM_RIGHT

                    # top-right
                    elif player_moves[0] == Position.TOP_RIGHT:
                        self._current_strategy == '2c-f'
                        target = Position.TOP_LEFT

                    # bottom-right
                    elif player_moves[0] == Position.BOTTOM_RIGHT:
                        self._current_strategy == '2c-g'
                        target = Position.TOP_RIGHT

                    ####################################################################################################

                    ####################################################################################################
                    # if player takes center, take opposite corner, try to force an error (if player is in corner, win)
                    elif player_moves[0] == Position.CENTER:
                        self._current_strategy == '2c-h'
                        target = Position.TOP_RIGHT

                    ####################################################################################################

                ########################################################################################################

                ########################################################################################################
                # AI took the bottom-right corner
                elif self._current_strategy == '2d':
                    # if player takes edge, next move go for center (then go for the corner that makes 2 possible)
                    # top
                    if player_moves[0] == Position.TOP_EDGE:
                        self._current_strategy == '2d-a'
                        target = Position.CENTER
                    # left
                    elif player_moves[0] == Position.LEFT_EDGE:
                        self._current_strategy == '2d-b'
                        target = Position.CENTER
                    # right
                    elif player_moves[0] == Position.RIGHT_EDGE:
                        self._current_strategy == '2d-c'
                        target = Position.CENTER
                    # bottom
                    elif player_moves[0] == Position.BOTTOM_EDGE:
                        self._current_strategy == '2d-d'
                        target = Position.CENTER

                    # if player takes corner, next move any corner, then get the last corner for win
                    # top-left
                    elif player_moves[0] == Position.TOP_LEFT:
                        self._current_strategy == '2d-g'
                        target = Position.TOP_RIGHT
                    # top-right
                    elif player_moves[0] == Position.TOP_RIGHT:
                        self._current_strategy == '2d-e'
                        target = Position.BOTTOM_LEFT
                    # bottom-left
                    elif player_moves[0] == Position.BOTTOM_LEFT:
                        self._current_strategy == '2d-f'
                        target = Position.TOP_LEFT

                    # if player takes center, take opposite corner, try to force an error (if player is in corner, win)
                    elif player_moves[0] == Position.CENTER:
                        self._current_strategy == '2d-h'
                        target = Position.TOP_LEFT

            ############################################################################################################

            ############################################################################################################
            # fourth move, ai's second move
            elif move_number == 4:

                ########################################################################################################
                # player's first move was to the center
                # ai moved to a corner
                # if the player moved anywhere except the opposite corner, this won't be hit (ai will block)
                # but we'll handle that case in particular -- move to any available corner
                if self._current_strategy == '3a' or self._current_strategy == '3b' or \
                        self._current_strategy == '3c' or self._current_strategy == '3d':

                    # find the first empty corner
                    if self.game.state[Position.TOP_LEFT] == '':
                        target = Position.TOP_LEFT
                    elif self.game.state[Position.TOP_RIGHT] == '':
                        target = Position.TOP_RIGHT
                    elif self.game.state[Position.BOTTOM_LEFT] == '':
                        target = Position.BOTTOM_LEFT
                    elif self.game.state[Position.BOTTOM_RIGHT] == '':
                        target = Position.BOTTOM_RIGHT

                ########################################################################################################

                ########################################################################################################
                # player's first move is a corner
                # ai played to center
                if self._current_strategy == '4a' or self._current_strategy == '4b' or \
                        self._current_strategy == '4c' or self._current_strategy == '4d':

                    # if the player's next move was a corner, play any edge
                    if (player_moves[0] == Position.TOP_LEFT or player_moves[0] == Position.TOP_RIGHT
                        or player_moves[0] == Position.BOTTOM_LEFT or player_moves[0] == Position.BOTTOM_RIGHT) \
                            and (player_moves[1] == Position.TOP_LEFT or player_moves[1] == Position.TOP_RIGHT
                                 or player_moves[1] == Position.BOTTOM_LEFT or player_moves[1] == Position.BOTTOM_RIGHT):
                        target = Position.TOP_EDGE

                    # if the player's next move was an edge, play any remaining corner
                    else:
                        # find first empty corner
                        if self.game.state[0] == '':
                            target = Position.TOP_LEFT;
                        elif self.game.state[2] == '':
                            target = Position.TOP_RIGHT;
                        elif self.game.state[Position.BOTTOM_LEFT] == '':
                            target = Position.BOTTOM_LEFT;
                        elif self.game.state[Position.BOTTOM_RIGHT] == '':
                            target = Position.BOTTOM_RIGHT;

                ########################################################################################################

                ########################################################################################################
                # player's first move was to the edge
                # ai moved to an adjacent corner
                # now ai moves to center
                if self._current_strategy == '5a-a' or self._current_strategy == '5a-b' or \
                        self._current_strategy == '5b-a' or self._current_strategy == '5b-b' or \
                        self._current_strategy == '5c-a' or self._current_strategy == '5c-b' or \
                        self._current_strategy == '5d-a' or self._current_strategy == '5d-b':
                    self._current_strategy == self._current_strategy + '-a'
                    target = Position.CENTER

            ############################################################################################################

            ############################################################################################################
            # fifth move - ai's third move
            elif move_number == 5:

                ########################################################################################################
                # AI took the top-left corner
                # Player took an edge
                # AI took center (player forced to take bottom-right corner)
                # AI takes corner that gives 2 possibilities

                # Player took top edge
                # AI takes bottom-left
                if self._current_strategy == '2a-a':
                    target = Position.BOTTOM_LEFT

                # Player took left edge
                # AI takes top-right
                elif self._current_strategy == '2a-b':
                    target = Position.TOP_RIGHT

                ########################################################################################################

                ########################################################################################################
                # AI took the top-left corner
                # Player took another corner
                # AI took another corner, forcing player to block
                # AI takes the last corner, forcing win

                # top-left, now bottom-right
                elif self._current_strategy == '2a-e':
                    target = Position.BOTTOM_RIGHT
                # bottom-left, now top-right
                elif self._current_strategy == '2a-f':
                    target = Position.TOP_RIGHT
                # bottom-right, now bottom-left
                elif self._current_strategy == '2a-g':
                    target = Position.BOTTOM_LEFT

                ########################################################################################################

                ########################################################################################################
                # AI took the top-right corner
                # Player took an edge
                # AI took center (player forced to take bottom-left corner)
                # AI takes corner that gives 2 possibilities

                # Player took top edge
                # AI takes bottom-right
                elif self._current_strategy == '2b-a':
                    target = Position.BOTTOM_RIGHT

                # Player took right edge
                # AI takes top-left
                elif self._current_strategy == '2b-c':
                    target = Position.TOP_LEFT

                ########################################################################################################

                ########################################################################################################
                # AI took the top-right corner
                # Player took another corner
                # AI took another corner, forcing player to block
                # AI takes the last corner, forcing win

                # top-left, now bottom-left
                elif self._current_strategy == '2b-e':
                    target = Position.BOTTOM_LEFT

                # bottom-left, now bottom-right
                elif self._current_strategy == '2b-f':
                    target = Position.BOTTOM_RIGHT

                # bottom-right, now top-left
                elif self._current_strategy == '2b-h':
                    target = Position.TOP_LEFT

                ########################################################################################################

                ########################################################################################################
                # AI took the bottom-left corner
                # Player took an edge
                # AI took center (player forced to take top-right corner)
                # AI takes corner that gives 2 possibilities

                # Player took left edge
                # AI takes bottom-right
                elif self._current_strategy == '2c-b':
                    target = Position.BOTTOM_RIGHT

                # Player took bottom edge
                # AI takes bottom-right
                elif self._current_strategy == '2c-d':
                    target = Position.TOP_LEFT

                ########################################################################################################

                ########################################################################################################
                # AI took the bottom-left corner
                # Player took another corner
                # AI took another corner, forcing player to block
                # AI takes the last corner, forcing win

                # top-left
                elif self._current_strategy == '2c-e':
                    target = Position.TOP_RIGHT
                # top-right
                elif self._current_strategy == '2c-f':
                    target = Position.BOTTOM_RIGHT
                # bottom-right
                elif self._current_strategy == '2c-g':
                    target = Position.TOP_LEFT

                ########################################################################################################

                ########################################################################################################
                # AI took the bottom-right corner
                # Player took an edge
                # AI took center (player forced to take top-left corner)
                # AI takes corner that gives 2 possibilities

                # Player took right edge
                # AI takes top-right
                elif self._current_strategy == '2d-c':
                    target = Position.BOTTOM_LEFT

                # Player took bottom edge
                # AI takes top-right
                elif self._current_strategy == '2d-d':
                    target = Position.TOP_RIGHT

                ########################################################################################################

                ########################################################################################################
                # AI took the bottom-left corner
                # Player took another corner
                # AI took another corner, forcing player to block
                # AI takes the last corner, forcing win

                # top-left, now bottom-left
                elif self._current_strategy == '2d-g':
                    target = Position.BOTTOM_LEFT

                # top-right, now top-left
                elif self._current_strategy == '2d-e':
                    target = Position.TOP_LEFT

                # bottom-left, now top-right
                elif self._current_strategy == '2d-f':
                    target = Position.TOP_RIGHT

                ########################################################################################################

            ############################################################################################################

        super().move(target)
