"""
Module for the main game logic

Handles the main game loop including turn order, AI, and end conditions
"""
import random

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty

from constants.difficulty import Difficulty
from constants.playermode import PlayerMode
from constants.playertoken import PlayerToken


class Game(Screen):
    """Main game screen"""
    # for some reason, adding state to init causes an error. My guess is that Kivy binding happens before init
    # the others seem to be okay because they aren't being evaluated until button press, but it's fragile

    # single dimension array to simplify the bindings, even though it makes some of access logic more complex
    # for Kivy to bind to a property automatically, it must be a Kivy property (e.g. ListProperty or ObjectProperty)
    state = ListProperty(['', '', '', '', '', '', '', '', ''])

    def __init__(self, **kwargs):
        """Initializes screen with default values"""
        self.mode = ObjectProperty(None)
        self.difficulty = ObjectProperty(None)

        self._allow_move = True
        self._thinking = False
        self._current_ai_strategy = ''
        self._current_player_token = PlayerToken.X.value
        self._grid_size = 3
        super(Game, self).__init__(**kwargs)

    def select_cell(self, x: int, y: int):
        """Selects a cell using the current player's token"""
        if not self._allow_move:
            return

        self._allow_move = False
        self.state[x*self._grid_size+y] = self._current_player_token
        self.check_end_conditions()

    def player_moved(self):
        """Called when a player (human or AI) moves to progress the game"""
        # poor man's debounce - this and allow_move mostly handle rapid clicking
        if self._thinking:
            return

        self._thinking = True
        self.switch_player()
        if self.mode == PlayerMode.ONE:
            # self._allow_move = False
            self.move()
        self._thinking = False
        self._allow_move = True

    def move(self):
        """Selects a move based on the AI's difficulty and corresponding decision tree"""
        token = self._current_player_token
        o = PlayerToken.O.value
        x = PlayerToken.X.value
        opponent_token = o if self._current_player_token == x else x
        cell = -1

        # TODO: refactor AI logic out into its own module
        # on easy, the moves are completely random (handled below as a fallback for the other AI's)

        # on normal, the moves are mostly random, but the opponent will block you from completing 3
        if self.difficulty == Difficulty.NORMAL:
            # first look for spaces that will get a win for AI
            cell = self.get_winning_cell(token)

            # next look for spaces to block opponent's imminent win
            if cell == -1:
                cell = self.get_winning_cell(opponent_token)

            # otherwise just choose randomly
            if cell == -1:
                found = False
                while not found:
                    cell = self.get_random_cell()
                    if self.state[cell] == '':
                        found = True

        # It might be possible to do this more elegantly if the board state is abstracted  further
        #   so that each corner has an opposite, etc. Not sure if it's worth it.
        # on hard, the opponent will choose the best possible move. The house always wins.
        elif self.difficulty == Difficulty.HARD:
            # TODO: the hard difficult logic is pretty hard to follow right now, refactoring numbers out will help
            cell = self.get_winning_cell(token)
            if cell == -1:
                cell = self.get_winning_cell(opponent_token)

            if cell == -1:
                player_moves = []
                move_number = 0
                # TODO: there's most likely a more clever way to handle iterations in Python, KISS for now
                for i in range(len(self.state)):
                        state = self.state[i]
                        if state != '':
                            move_number += 1
                            if state == opponent_token:
                                player_moves.append(i)

                # if this is the very first move, choose randomly between corner and center
                # corner is actually a stronger play, but for fun let the AI choose center sometimes
                if move_number == 0:
                    strategy = random.randint(1, 5)
                    # center
                    if strategy == 1:
                        self._current_ai_strategy = '1'
                        cell = 4
                    # top left
                    elif strategy == 2:
                        self._current_ai_strategy = '2a'
                        cell = 0
                    # top right
                    elif strategy == 3:
                        self._current_ai_strategy = '2b'
                        cell = 2
                    # bottom left
                    elif strategy == 4:
                        self._current_ai_strategy = '2c'
                        cell = 6
                    # bottom right
                    elif strategy == 5:
                        self._current_ai_strategy = '2d'
                        cell = 8

                # second move - this is the AI's first move, and it's reacting to the player's move
                elif move_number == 1:
                    # if the player's first move is the center
                    if player_moves[0] == 4:
                        # ai moves to any corner
                        strategy = random.randint(1,4)
                        # top-left
                        if strategy == 1:
                            self._current_ai_strategy = '3a'
                            cell = 0
                        # top-right
                        elif strategy == 2:
                            self._current_ai_strategy = '3b'
                            cell = 2
                        # bottom-left
                        elif strategy == 3:
                            self._current_ai_strategy = '3c'
                            cell = 6
                        # bottom-right
                        elif strategy == 4:
                            self._current_ai_strategy = '3d'
                            cell = 8

                    # if the player's first move is a corner
                    elif player_moves[0] == 0:
                        self._current_ai_strategy = '4a'
                        cell = 4
                    elif player_moves[0] == 2:
                        self._current_ai_strategy = '4b'
                        cell = 4
                    elif player_moves[0] == 6:
                        self._current_ai_strategy = '4c'
                        cell = 4
                    elif player_moves[0] == 8:
                        self._current_ai_strategy = '4d'
                        cell = 4

                    # if the player's first move is an edge, take an adjacent corner - next move center
                    # top
                    elif player_moves[0] == 1:
                        strategy = random.randint(1,2)
                        # top left
                        if strategy == 1:
                            self._current_ai_strategy = '5a-a'
                            cell = 0
                        # top right
                        elif strategy == 2:
                            self._current_ai_strategy = '5a-b'
                            cell = 2

                    # left
                    elif player_moves[0] == 3:
                        strategy = random.randint(1,2)
                        # top left
                        if strategy == 1:
                            self._current_ai_strategy = '5b-a'
                            cell = 0
                        # bottom left
                        elif strategy == 2:
                            self._current_ai_strategy = '5b-b'
                            cell = 6

                    # right
                    elif player_moves[0] == 5:
                        strategy = random.randint(1, 2)
                        # top right
                        if strategy == 1:
                            self._current_ai_strategy = '5c-a'
                            cell = 2
                        # bottom right
                        elif strategy == 2:
                            self._current_ai_strategy = '5c-b'
                            cell = 8

                    # bottom
                    elif player_moves[0] == 7:
                        strategy = random.randint(1, 2)
                        # bottom left
                        if strategy == 1:
                            self._current_ai_strategy = '5d-a'
                            cell = 6
                        # bottom right
                        elif strategy == 2:
                            self._current_ai_strategy = '5d-b'
                            cell = 8

                # third move - ai's second move
                elif move_number == 2:
                    # center
                    if self._current_ai_strategy == '1':
                        # player's move - edge - this should force a win without having to explicitly code other moves
                        # top
                        if player_moves[0] == 1:
                            self._current_ai_strategy = '1-a'
                            cell = 0
                        # left
                        elif player_moves[0] == 3:
                            self._current_ai_strategy = '1-b'
                            cell = 6
                        # right
                        elif player_moves[0] == 5:
                            self._current_ai_strategy = '1-c'
                            cell = 2
                        # bottom
                        elif player_moves[0] == 7:
                            self._current_ai_strategy = '1-d'
                            cell = 8

                        # player's move - corner - the best next move is the opposite corner, try to force an error
                        # top left
                        if player_moves[0] == 0:
                            self._current_ai_strategy = '1-e'
                            cell = 8
                        # top right
                        elif player_moves[0] == 2:
                            self._current_ai_strategy = '1-f'
                            cell = 6
                        # bottom left
                        elif player_moves[0] == 6:
                            self._current_ai_strategy = '1-g'
                            cell = 2
                        # bottom right
                        elif player_moves[0] == 8:
                            self._current_ai_strategy = '1-h'
                            cell = 0

                    # top left
                    elif self._current_ai_strategy  == '2a':
                        # player's move - edge - next move go for center (then go for the corner that makes 2 possible)
                        # top
                        if player_moves[0] == 1:
                            self._current_ai_strategy == '2a-a'
                            cell = 4
                        # left
                        elif player_moves[0] == 3:
                            self._current_ai_strategy == '2a-b'
                            cell = 4
                        # right
                        elif player_moves[0] == 5:
                            self._current_ai_strategy == '2a-c'
                            cell = 4
                        # bottom
                        elif player_moves[0] == 7:
                            self._current_ai_strategy == '2a-d'
                            cell = 4

                        # player's move - corner - next move any corner, then get the last corner for win
                        # top left
                        elif player_moves[0] == 2:
                            self._current_ai_strategy == '2a-e'
                            cell = 6
                        # bottom left
                        elif player_moves[0] == 6:
                            self._current_ai_strategy == '2a-f'
                            cell = 8
                        # bottom right
                        elif player_moves[0] == 8:
                            self._current_ai_strategy == '2a-g'
                            cell = 2

                        # player's move - center - opposite corner, try to force an error (if player is in corner, win)
                        elif player_moves[0] == 4:
                            self._current_ai_strategy == '2a-h'
                            cell = 8

                    # top right
                    elif self._current_ai_strategy == '2b':
                        # player's move - edge - next move go for center (then go for the corner that makes 2 possible)
                        # top
                        if player_moves[0] == 1:
                            self._current_ai_strategy == '2b-a'
                            cell = 4
                        # left
                        elif player_moves[0] == 3:
                            self._current_ai_strategy == '2b-b'
                            cell = 4
                        # right
                        elif player_moves[0] == 5:
                            self._current_ai_strategy == '2b-c'
                            cell = 4
                        # bottom
                        elif player_moves[0] == 7:
                            self._current_ai_strategy == '2b-d'
                            cell = 4

                        # player's move - corner - next move any corner, then get the last corner for win
                        # top left
                        elif player_moves[0] == 0:
                            self._current_ai_strategy == '2b-e'
                            cell = 8
                        # bottom left
                        elif player_moves[0] == 6:
                            self._current_ai_strategy == '2b-f'
                            cell = 0
                        # bottom right
                        elif player_moves[0] == 8:
                            self._current_ai_strategy == '2b-h'
                            cell = 6

                        # player's move - center - opposite corner, try to force an error (if player is in corner, win)
                        elif player_moves[0] == 4:
                            self._current_ai_strategy == '2b-h'
                            cell = 6

                    # bottom left
                    elif self._current_ai_strategy == '2c':
                        # player's move - edge - next move go for center (then go for the corner that makes 2 possible)
                        # top
                        if player_moves[0] == 1:
                            self._current_ai_strategy == '2c-a'
                            cell = 4
                        # left
                        elif player_moves[0] == 3:
                            self._current_ai_strategy == '2c-b'
                            cell = 4
                        # right
                        elif player_moves[0] == 5:
                            self._current_ai_strategy == '2c-c'
                            cell = 4
                        # bottom
                        elif player_moves[0] == 7:
                            self._current_ai_strategy == '2c-d'
                            cell = 4

                        # player's move - corner - next move any corner, then get the last corner for win
                        # top left
                        elif player_moves[0] == 0:
                            self._current_ai_strategy == '2c-e'
                            cell = 8
                        # top right
                        elif player_moves[0] == 2:
                            self._current_ai_strategy == '2c-f'
                            cell = 0
                        # bottom right
                        elif player_moves[0] == 8:
                            self._current_ai_strategy == '2c-g'
                            cell = 2

                        # player's move - center - opposite corner, try to force an error (if player is in corner, win)
                        elif player_moves[0] == 4:
                            self._current_ai_strategy == '2c-h'
                            cell = 2

                    #bottom right
                    elif self._current_ai_strategy == '2d':
                        # player's move - edge - next move go for center (then go for the corner that makes 2 possible)
                        # top
                        if player_moves[0] == 1:
                            self._current_ai_strategy == '2d-a'
                            cell = 4
                        # left
                        elif player_moves[0] == 3:
                            self._current_ai_strategy == '2d-b'
                            cell = 4
                        # right
                        elif player_moves[0] == 5:
                            self._current_ai_strategy == '2d-c'
                            cell = 4
                        # bottom
                        elif player_moves[0] == 7:
                            self._current_ai_strategy == '2d-d'
                            cell = 4

                        # player's move - corner - next move any corner, then get the last corner for win
                        # top left
                        elif player_moves[0] == 0:
                            self._current_ai_strategy == '2d-g'
                            cell = 2
                        # top right
                        elif player_moves[0] == 2:
                            self._current_ai_strategy == '2d-e'
                            cell = 6
                        # bottom left
                        elif player_moves[0] == 6:
                            self._current_ai_strategy == '2d-f'
                            cell = 0

                        # player's move - center - opposite corner, try to force an error (if player is in corner, win)
                        elif player_moves[0] == 4:
                            self._current_ai_strategy == '2d-h'
                            cell = 0

                # fourth move
                elif move_number == 3:
                    # player's first move was to the center
                    # ai moved to a corner
                    # if the player moved anywhere except the opposite corner, this won't be hit (ai will block)
                    # but we'll handle that case in particular -- move to any available corner
                    if self._current_ai_strategy == '3a' or self._current_ai_strategy == '3b' or \
                        self._current_ai_strategy == '3c' or self._current_ai_strategy == '3d':

                            if self.state[0] == '':
                                cell = 0;
                            elif self.state[2] == '':
                                cell = 2;
                            elif self.state[6] == '':
                                cell = 6;
                            elif self.state[8] == '':
                                cell = 8;

                    # player's first move is a corner
                    # ai played to center
                    if self._current_ai_strategy == '4a' or self._current_ai_strategy == '4b' or \
                            self._current_ai_strategy == '4c' or self._current_ai_strategy == '4d':
                        # if the player's next move was a corner, play any edge
                        if (player_moves[0] == 0 or player_moves[0] == 2
                            or player_moves[0] == 6 or player_moves[0] == 8) \
                                and (player_moves[1] == 0 or player_moves[1] == 2
                                     or player_moves[1] == 6 or player_moves[1] == 8):
                            cell = 1
                            # if the player's next move was an edge, play any remaining corner
                        else:
                            if self.state[0] == '':
                                cell = 0;
                            elif self.state[2] == '':
                                cell = 2;
                            elif self.state[6] == '':
                                cell = 6;
                            elif self.state[8] == '':
                                cell = 8;

                    # player's first move was to the edge
                    # ai moved to an adjacent corner
                    # now ai moves to center
                    if self._current_ai_strategy == '5a-a' or self._current_ai_strategy == '5a-b' or \
                        self._current_ai_strategy == '5b-a' or self._current_ai_strategy == '5b-b' or \
                        self._current_ai_strategy == '5c-a' or self._current_ai_strategy == '5c-b' or \
                            self._current_ai_strategy == '5d-a' or self._current_ai_strategy == '5d-b':
                        self._current_ai_strategy == self._current_ai_strategy + '-a'
                        cell = 4

                # fifth move - ai's third move
                elif move_number == 4:

                    # AI took the top-left corner
                    # Player took top edge
                    # AI took center (player forced to take bottom-right corner
                    # AI takes bottom-left
                    if self._current_ai_strategy == '2a-a':
                        cell = 6
                    # AI took the top-left corner
                    # Player took left edge
                    # AI took center (player forced to take bottom-right corner
                    # AI takes top-right
                    elif self._current_ai_strategy == '2a-b':
                        cell = 2
                    # right
                    elif player_moves[0] == 5:
                        self._current_ai_strategy == '2a-c'
                        cell = 2
                    # bottom
                    elif player_moves[0] == 7:
                        self._current_ai_strategy == '2a-d'
                        cell = 6

                    # ai took top-left
                    # player moved to corner
                    # ai grabbed another corner, forcing player to block
                    # ai grabs the last corner, forcing win
                    # top left, now bottom right
                    elif self._current_ai_strategy == '2a-e':
                        cell = 8
                    # bottom left, now top right
                    elif  self._current_ai_strategy == '2a-f':
                        cell = 2
                    # bottom right, now bottom-left
                    elif self._current_ai_strategy == '2a-g':
                        cell = 6

                    # top right
                    # top
                    # center
                    # bottom-left
                    # bottom-right
                    if self._current_ai_strategy == '2b-a':
                        cell = 8

                    # left
                    elif self._current_ai_strategy == '2b-b':
                        cell = 0
                    # right
                    elif self._current_ai_strategy == '2b-c':
                        cell = 0
                    # bottom
                    elif self._current_ai_strategy == '2b-d':
                        cell = 8

                    # player's move - corner - next move any corner, then get the last corner for win
                    # top left
                    elif self._current_ai_strategy == '2b-e':
                        cell = 6
                    # bottom left
                    elif self._current_ai_strategy == '2b-f':
                        cell = 8
                    # bottom right
                    elif self._current_ai_strategy == '2b-h':
                        cell = 0

                # bottom left
                elif self._current_ai_strategy == '2c':
                    # bottom-left
                    # top
                    # center
                    # top-right
                    if self._current_ai_strategy == '2c-a':
                        cell = 0
                    # left
                    elif self._current_ai_strategy == '2c-b':
                        cell = 8
                    # right
                    elif self._current_ai_strategy == '2c-c':
                        cell = 8
                    # bottom
                    elif self._current_ai_strategy == '2c-d':
                        cell = 0

                    # top left
                    elif self._current_ai_strategy == '2c-e':
                        cell = 2
                    # top right
                    elif self._current_ai_strategy == '2c-f':
                        cell = 8
                    # bottom right
                    elif self._current_ai_strategy == '2c-g':
                        cell = 0

                # bottom right
                elif self._current_ai_strategy == '2d':
                    # bottom-right
                    # top
                    # center
                    # top-left

                    if self._current_ai_strategy == '2d-a':
                        cell = 2
                    # left
                    elif self._current_ai_strategy == '2d-b':
                        cell = 6
                    # right
                    elif self._current_ai_strategy == '2d-c':
                        cell = 6
                    # bottom
                    elif self._current_ai_strategy == '2d-d':
                        cell = 2

                    # player's move - corner - next move any corner, then get the last corner for win
                    # top left
                    elif self._current_ai_strategy == '2d-g':
                        cell = 6
                    # top right
                    elif self._current_ai_strategy == '2d-e':
                        cell = 0
                    # bottom left
                    elif self._current_ai_strategy == '2d-f':
                        cell = 2

        if cell == -1 or self.state[cell] != '':
            while cell == -1:
                rand = self.get_random_cell()
                if self.state[rand] == '':
                    cell = rand

        self.state[cell] = token
        self.check_end_conditions()
        self.switch_player()
        return

    def get_winning_cell(self,token:str) -> int:
        """Checks to see if any cell could lead to a win, and returns it (or -1 otherwise)"""
        cell = -1

        # Row 0
        if self.state[0] == token and self.state[1] == token and self.state[2] == '':
            cell = 2
        elif self.state[0] == token and self.state[2] == token and self.state[1] == '':
            cell = 1
        elif self.state[1] == token and self.state[2] == token and self.state[0] == '':
            cell = 0

        # Row 1
        elif self.state[3] == token and self.state[4] == token and self.state[5] == '':
            cell = 5
        elif self.state[3] == token and self.state[5] == token and self.state[4] == '':
            cell = 4
        elif self.state[4] == token and self.state[5] == token and self.state[3] == '':
            cell = 3

        # Row 2
        elif self.state[6] == token and self.state[7] == token and self.state[8] == '':
            cell = 8
        elif self.state[6] == token and self.state[8] == token and self.state[7] == '':
            cell = 7
        elif self.state[7] == token and self.state[8] == token and self.state[6] == '':
            cell = 6

        # Col 0
        elif self.state[0] == token and self.state[3] == token and self.state[6] == '':
            cell = 6
        elif self.state[0] == token and self.state[6] == token and self.state[3] == '':
            cell = 3
        elif self.state[3] == token and self.state[6] == token and self.state[0] == '':
            cell = 0

        # Col 1
        elif self.state[1] == token and self.state[4] == token and self.state[7] == '':
            cell = 7
        elif self.state[1] == token and self.state[7] == token and self.state[4] == '':
            cell = 4
        elif self.state[4] == token and self.state[7] == token and self.state[1] == '':
            cell = 1

        # Col 2
        elif self.state[2] == token and self.state[5] == token and self.state[8] == '':
            cell = 8
        elif self.state[2] == token and self.state[8] == token and self.state[5] == '':
            cell = 5
        elif self.state[5] == token and self.state[8] == token and self.state[2] == '':
            cell = 2

        # Dia 1
        elif self.state[0] == token and self.state[4] == token and self.state[8] == '':
            cell = 8
        elif self.state[0] == token and self.state[8] == token and self.state[4] == '':
            cell = 4
        elif self.state[4] == token and self.state[8] == token and self.state[0] == '':
            cell = 0

        # Dia 2
        elif self.state[6] == token and self.state[4] == token and self.state[2] == '':
            cell = 2
        elif self.state[6] == token and self.state[2] == token and self.state[4] == '':
            cell = 4
        elif self.state[4] == token and self.state[2] == token and self.state[6] == '':
            cell = 6

        return cell

    def get_random_cell(self) -> int:
        """Gets a random cell in the grid"""
        cell = -1
        while cell == -1:
            rand = random.randrange(0, self._grid_size) * self._grid_size + random.randrange(0, self._grid_size)
            if self.state[rand] == '':
                cell = rand

        return cell

    def switch_player(self):
        """Switches the current player token between the player's tokens"""
        self._current_player_token = PlayerToken.O.value if self._current_player_token == PlayerToken.X.value \
            else PlayerToken.X.value

    def reset(self):
        """Resets the grid state"""
        for i in range(len(self.state)):
                self.state[i] = ''
        # X is always the token for the player that makes the first move (seems odd?)
        self._current_player_token = PlayerToken.X.value

    def check_end_conditions(self):
        """Check all game end conditions"""
        if self.check_win_condition():
            self.reset()
            return

        if self.check_draw_condition():
            self.reset()
            return

    def check_win_condition(self) -> bool:
        """Check all game win conditions"""
        return self.check_rows() or self.check_cols() or self.check_diagonals()
        pass

    def check_draw_condition(self) -> bool:
        """Check the draw condition"""
        # if any of the cells have an empty space, it's not yet a draw
        for i in range(len(self.state)):
                if self.state[i] == '':
                    return False
        return True

    def check_rows(self) -> bool:
        """Check rows for a match"""
        return self.check_row(0) or self.check_row(1) or self.check_row(2)

    def check_row(self, x: int) -> bool:
        """Check row for a match"""
        cols = self._grid_size
        if self.state[x*self._grid_size] != '' \
                and (self.state[x*cols] == self.state[x*cols+1] == self.state[x*cols+2]):
            return True
        return False

    def check_cols(self) -> bool:
        """Check columns for a match"""
        return self.check_col(0) or self.check_col(1) or self.check_col(2)

    def check_col(self, y: int) -> bool:
        """Check column for a match"""
        if self.state[y] != '' and (self.state[y] == self.state[self._grid_size+y] == self.state[2*self._grid_size+y]):
            return True
        return False

    def check_diagonals(self) -> bool:
        """Check diagonals for a match"""
        if self.state[0] != '' and (self.state[0] == self.state[4] == self.state[8]):
            return True

        if self.state[6] != '' and (self.state[6] == self.state[4] == self.state[2]):
            return True

        return False
