from kivy.app import App
from board import Board

class TicTacToe(App):

    def build(self):

        self.board = Board(cols=3)

        return self.board

if __name__ == '__main__':
    TicTacToe().run()