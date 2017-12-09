"""A simple Tic Tac Toe game that supports one or two players, as well as multiple difficulties of AI"""

# TODO: figure out if there's a good way to automatically strip out debug code for python, for now comment out in push
# debug only
# from constants.difficulty import Difficulty
# from constants.gamemode import GameMode
# from constants.screen import Screen
# from screens.game import Game


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.config import Config
# For now, don't allow resize to simplify layouts. Later we'll fix this to be responsive.
Config.set('graphics', 'resizable', False)
# TODO: Test on different resolutions. Playing with it, it looks alright at phone resolutions but double check.
# Config.set('graphics', 'fullscreen', True);


class TicTacToeScreenManager(ScreenManager):
    """Enables easy transitions between the different screens of the game"""
    screen_player_select = ObjectProperty(None)
    screen_difficulty_select = ObjectProperty(None)
    screen_game = ObjectProperty(None)

    # debug only, jump straight to game screen with options selected
    # def debug(self, game: Game, player_mode: GameMode = GameMode.ONE_PLAYER, difficulty: Difficulty = Difficulty.EASY):
    #     game.set_difficulty(difficulty)
    #     game.mode = player_mode
    #     self.screen_game = game
    #     self.current = Screen.GAME.value


class TicTacToeApp(App):
    """The entry point for the Tic Tac Toe game"""
    # debug only
    # def build(self):
    #     manager = TicTacToeScreenManager()
    #     manager.debug(manager.screen_game, GameMode.ONE_PLAYER, Difficulty.HARD)
    #     return manager

    # release
    def build(self):
        return TicTacToeScreenManager()


if __name__ == '__main__':
    TicTacToeApp().run()
