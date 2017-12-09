"""
Module for the main game logic

Handles the main game loop including turn order, AI, and end conditions
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty

from constants.difficulty import Difficulty
from constants.playertoken import PlayerToken
from constants.gamemode import GameMode

from players.ai.easy import EasyAI
from players.ai.normal import NormalAI
from players.ai.hard import HardAI
from players.player import Player


class Game(Screen):
    """Main game screen"""
    # for some reason, adding state to init causes an error. My guess is that Kivy binding happens before init
    # the others seem to be okay because they aren't being evaluated until button press, but it's fragile

    # single dimension array to simplify the bindings, even though it makes some of access logic more complex
    # for Kivy to bind to a property automatically, it must be a Kivy property (e.g. ListProperty or ObjectProperty)
    state = ListProperty(['', '', '', '', '', '', '', '', ''])

    def __init__(self, **kwargs):
        """Initializes screen with default values"""
        super(Game, self).__init__(**kwargs)
        self.mode = ObjectProperty(None)
        self.difficulty = ObjectProperty(None)
        self._player_one = Player(self, PlayerToken.X)
        self._player_two = Player(self, PlayerToken.O)
        self._current_player = self._player_one
        self._allow_move = True
        self.grid_size = 3

    def set_difficulty(self, difficulty: Difficulty):
        token = self._player_two.token
        """sets up an AI of the given difficulty"""
        if difficulty == Difficulty.EASY:
            self._player_two = EasyAI(self, token)
        if difficulty == Difficulty.NORMAL:
            self._player_two = NormalAI(self, token)
        if difficulty == Difficulty.HARD:
            self._player_two = HardAI(self, token)

    def select_cell(self, position: int):
        """Selects a cell using the current player's token"""
        if not self._allow_move:
            return

        self.fill_cell(position, self._current_player.token)
        self.player_moved()

    def fill_cell(self, position: int, token: PlayerToken):
        """Selects a cell using the given token"""
        self.state[position] = token.value
        self.check_end_conditions()
        self.switch_player()

    def player_moved(self):
        """Called when a player moves to progress the game"""
        self._allow_move = False

        # basic debounce - this and allow_move should mostly handle rapid clicking
        if self.mode == GameMode.ONE_PLAYER:
            if self._current_player.thinking:
                return
            else:
                self._current_player.move()

        self._allow_move = True

    def switch_player(self):
        """Switches the current player token between the two players"""
        self._current_player = self._player_one if self._current_player == self._player_two else self._player_two

    def reset(self):
        """Resets the grid state"""
        for i in range(len(self.state)):
                self.state[i] = ''

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
        cols = self.grid_size
        if self.state[x*self.grid_size] != '' \
                and (self.state[x*cols] == self.state[x*cols+1] == self.state[x*cols+2]):
            return True
        return False

    def check_cols(self) -> bool:
        """Check columns for a match"""
        return self.check_col(0) or self.check_col(1) or self.check_col(2)

    def check_col(self, y: int) -> bool:
        """Check column for a match"""
        if self.state[y] != '' and (self.state[y] == self.state[self.grid_size+y] == self.state[2*self.grid_size+y]):
            return True
        return False

    def check_diagonals(self) -> bool:
        """Check diagonals for a match"""
        if self.state[0] != '' and (self.state[0] == self.state[4] == self.state[8]):
            return True

        if self.state[6] != '' and (self.state[6] == self.state[4] == self.state[2]):
            return True

        return False
