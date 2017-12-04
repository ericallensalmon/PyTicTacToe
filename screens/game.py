import random

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty

from difficulty import Difficulty
from playermode import PlayerMode


# Main game
class Game(Screen):
    state = ListProperty(['', '', '', '', '', '', '', '', ''])

    def __init__(self, **kwargs):
        # single dimension array to simplify the bindings, even though it makes some of access logic more complex
        # for Kivy to bind to a property automatically, it must be a Kivy property (e.g. ListProperty or ObjectProperty)

        self.mode = ObjectProperty(None)
        self.difficulty = ObjectProperty(None)

        self._allow_move = True
        self._thinking = False
        self._current_player_token = 'X'
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
        # on easy, the moves are completely random
        if self.difficulty == Difficulty.EASY:
            found = False
            while not found:
                cell = self.get_random_cell()
                if self.state[cell] == '':
                    found = True
                    self.state[cell] = self._current_player_token

        # on normal, the moves are mostly random, but the opponent will block you from completing 3
        if self.difficulty == Difficulty.NORMAL:
            return

        # on hard, the opponent will choose the best possible move. The house always wins.
        if self.difficulty == Difficulty.HARD:
            return

        self.check_end_conditions()
        self.switch_player()
        return

    def get_random_cell(self) -> int:
        return random.randrange(0, self._grid_size) * self._grid_size + random.randrange(0, self._grid_size)

    def switch_player(self):
        self._current_player_token = 'O' if self._current_player_token == 'X' else 'X'

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
        if self.state[x*self._grid_size] != '' \
                and (self.state[x*self._grid_size] == self.state[x*self._grid_size+1] == self.state[x*self._grid_size+2]):
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
