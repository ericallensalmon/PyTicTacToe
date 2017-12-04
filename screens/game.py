import random

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty

from difficulty import Difficulty
from playermode import PlayerMode
from playertoken import PlayerToken

# Main game
class Game(Screen):
    # for some reason, adding state to init causes an error. My guess is that Kivy binding happens before init
    # the others seem to be okay because they aren't being evaluated until button press, but it's fragile

    # single dimension array to simplify the bindings, even though it makes some of access logic more complex
    # for Kivy to bind to a property automatically, it must be a Kivy property (e.g. ListProperty or ObjectProperty)
    state = ListProperty(['', '', '', '', '', '', '', '', ''])

    def __init__(self, **kwargs):

        self.mode = ObjectProperty(None)
        self.difficulty = ObjectProperty(None)

        self._allow_move = True
        self._thinking = False
        self._current_player_token = PlayerToken.X.value
        self._grid_size = 3
        super(Game, self).__init__(**kwargs)

    def select_cell(self, x: int, y: int):
        if not self._allow_move:
            return

        self._allow_move = False
        self.state[x*self._grid_size+y] = self._current_player_token
        self.check_end_conditions()

    def player_moved(self):
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
        token = self._current_player_token
        opptoken = PlayerToken.O.value if self._current_player_token == PlayerToken.X.value else PlayerToken.X.value
        # on easy, the moves are completely random
        if self.difficulty == Difficulty.EASY:
            found = False
            while not found:
                cell = self.get_random_cell()
                if self.state[cell] == '':
                    found = True
                    self.state[cell] = token

        # on normal, the moves are mostly random, but the opponent will block you from completing 3
        elif self.difficulty == Difficulty.NORMAL:
            # first look for spaces that will get a win for AI
            cell = self.get_winning_cell(token)

            # next look for spaces to block opponent's imminent win
            if cell == -1:
                cell = self.get_winning_cell(opptoken)

            # otherwise just choose randomly
            if cell == -1:
                found = False
                while not found:
                    cell = self.get_random_cell()
                    if self.state[cell] == '':
                        found = True

            self.state[cell] = token

        # on hard, the opponent will choose the best possible move. The house always wins.
        elif self.difficulty == Difficulty.HARD:
            return

        self.check_end_conditions()
        self.switch_player()
        return

    # Returns a cell where the given token could win, or -1 otherwise
    def get_winning_cell(self,token:str) -> int:
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
        return random.randrange(0, self._grid_size) * self._grid_size + random.randrange(0, self._grid_size)

    def switch_player(self):
        self._current_player_token = PlayerToken.O.value if self._current_player_token == PlayerToken.X.value \
            else PlayerToken.X.value

    def reset(self):
        for i in range(self._grid_size):
            for j in range(self._grid_size):
                self.state[i*self._grid_size+j] = ''

    def check_end_conditions(self):
        if self.check_win_condition():
            self.reset()
            return

        if self.check_draw_condition():
            self.reset()
            return

    def check_win_condition(self) -> bool:
        return self.check_rows() or self.check_cols() or self.check_diagonals()
        pass

    def check_draw_condition(self) -> bool:
        # if any of the cells have an empty space, it's not yet a draw
        for i in range(self._grid_size):
            for j in range(self._grid_size):
                if self.state[i * self._grid_size + j] == '':
                    return False
        return True

    def check_rows(self) -> bool:
        return self.check_row(0) or self.check_row(1) or self.check_row(2)

    def check_row(self, x: int) -> bool:
        cols = self._grid_size
        if self.state[x*self._grid_size] != '' \
                and (self.state[x*cols] == self.state[x*cols+1] == self.state[x*cols+2]):
            return True
        return False

    def check_cols(self) -> bool:
        return self.check_col(0) or self.check_col(1) or self.check_col(2)

    def check_col(self, y: int) -> bool:
        if self.state[y] != '' and (self.state[y] == self.state[self._grid_size+y] == self.state[2*self._grid_size+y]):
            return True
        return False

    def check_diagonals(self) -> bool:
        if self.state[0] != '' and (self.state[0] == self.state[4] == self.state[8]):
            return True

        if self.state[6] != '' and (self.state[6] == self.state[4] == self.state[2]):
            return True

        return False
