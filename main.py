from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.config import Config
# For now, don't allow resize to simplify layouts. Later we'll fix this to be responsive.
Config.set('graphics', 'resizable', False)
# TODO: Test on different resolutions. Playing with it, it looks alright at phone resolutions but double check.
# Config.set('graphics', 'fullscreen', True);


class ScreenPlayerSelect(Screen):
    pass


class ScreenDifficultySelect(Screen):
    pass


class ScreenGame(Screen):
    pass


class TicTacToeScreenManager(ScreenManager):

    screen_player_select = ObjectProperty(None)
    screen_difficulty_select = ObjectProperty(None)
    screen_game = ObjectProperty(None)
    mode = ObjectProperty(None)
    difficulty = ObjectProperty(None)


class TicTacToeApp(App):
    def build(self):
        return TicTacToeScreenManager()


if __name__ == '__main__':
    TicTacToeApp().run()