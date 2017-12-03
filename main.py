from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.button import Button
from difficulty import Difficulty
from playermode import PlayerMode
from kivy.config import Config
# For now, don't allow resize to simplify layouts. Later we'll fix this to be responsive.
Config.set('graphics', 'resizable', False)
# TODO: Test on different resolutions. Playing with it, it looks alright at phone resolutions but double check.
# Config.set('graphics', 'fullscreen', True);


# Simple one or two player select, button logic handled in kv file
class ScreenPlayerSelect(Screen):
    pass


# Simple difficulty select, button logic handled in kv file
class ScreenDifficultySelect(Screen):
    pass


# Main game
class ScreenGame(Screen):
    # TODO: probably some fancy linear algebra ways to make this more clever
    # single dimension array to simplify the bindings, even though it makes some of access logic more complex
    # for Kivy to bind to a property automatically, it must be a Kivy property (e.g. ListProperty or ObjectProperty)
    state = ListProperty(['', '', '', '', '', '', '', '', ''])
    currentPlayerToken = 'X'
    allowMove = ObjectProperty(None)
    mode = ObjectProperty(None)
    difficulty = ObjectProperty(None)
    grid_size = 3

    # TODO: need to decouple view and model, especially to get the AI working smoothly
    def select_cell(self, button: Button, x: int, y: int):
        self.state[x*self.grid_size+y] = self.currentPlayerToken
        button.text = self.currentPlayerToken
        if self.check_win_condition():
            self.reset()
            return

        if self.check_draw_condition():
            self.reset()
            return

        self.switch_player()
        if self.mode == PlayerMode.ONE:
            self.allowMove = False

    def player_moved(self):
        if self.mode == PlayerMode.ONE:
            self.move()

    def move(self):
        pass
        # self.allowMove = True
        # choose a random grid cell
        # select it

    def switch_player(self):
        self.currentPlayerToken = 'O' if self.currentPlayerToken == 'X' else 'X'

    def reset(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.state[i*self.grid_size+j] = ''
        self.allowMove = True

    # TODO: optimize this to use only the x,y we're interested in
    def check_win_condition(self) -> bool:
        return self.check_rows() or self.check_cols() or self.check_diagonals()
        pass

    def check_draw_condition(self) -> bool:
        # if any of the cells have an empty space, it's not yet a draw
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.state[i * self.grid_size + j] == '':
                    return False
        return True

    def check_rows(self) -> bool:
        return self.check_row(0) or self.check_row(1) or self.check_row(2)

    def check_row(self, x: int) -> bool:
        if self.state[x*self.grid_size] != '' \
                and (self.state[x*self.grid_size] == self.state[x*self.grid_size+1] == self.state[x*self.grid_size+2]):
            return True
        return False

    def check_cols(self) -> bool:
        return self.check_col(0) or self.check_col(1) or self.check_col(2)

    def check_col(self, y: int) -> bool:
        if self.state[y] != '' and (self.state[y] == self.state[self.grid_size+y] == self.state[2*self.grid_size+y]):
            return True
        return False

    def check_diagonals(self) -> bool:
        if self.state[0] != '' and (self.state[0] == self.state[4] == self.state[8]):
            return True

        if self.state[6] != '' and (self.state[6] == self.state[4] == self.state[2]):
            return True

        return False

    def is_disabled(self, current_state: str) -> bool:
        return not self.allowMove or current_state != ''

    # def get_text(self, x: int, y: int) -> str:
    #     return self.state[x][y]


class TicTacToeScreenManager(ScreenManager):
    screen_player_select = ObjectProperty(None)
    screen_difficulty_select = ObjectProperty(None)
    screen_game = ObjectProperty(None)


class TicTacToeApp(App):
    def build(self):
        return TicTacToeScreenManager()


if __name__ == '__main__':
    TicTacToeApp().run()