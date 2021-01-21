from kivy.core import text
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

SYMBOLS = ('X', 'O')

class Board(GridLayout):

    grid = None
    symbols = None

    def __init__(self, cols=3, **kwargs):
        super(Board, self).__init__(**kwargs)

        self.cols = cols
        self.rows = cols
        self.symbols = {
            'player':'X',
            'ai':'O'
        }
        self.trun = 'player'

        self.grid = [[None for col in range(self.cols)] for row in range(self.rows)]

        self._draw_tiles()


    def _draw_tiles(self):
        """
            Adds the tiles to the grid (widgets to the gridset)
        """
        for row in range(self.rows):
            for col in range(self.cols):
                tile = Button(font_size=60)
                tile.bind(on_press=self._onclick)
                self.grid[row][col] = tile
                self.add_widget(tile)


    def _onclick(self, instance):
        """
            Handles player move
        """
        if self.trun == 'player':
            if instance.text:
                return None

            instance.text = self.symbols['player']

            if self._check_status():

                self._ai_turn()


#---------------ai
    def _ai_turn(self):
        """
            Handles ai's move
        """
        self.trun = 'ai'
        
        bestMove = self.minimax(self.trun)
        bestMove['index'].text = self.symbols['ai']

        self._check_status(True)
        self.trun = 'player'


    def getAvailableSpots(self):
        emptySpots = []

        for row in self.grid:
            for col in row:
                if col.text == '':
                    emptySpots.append(col)
        return emptySpots


    def minimax(self, player):
        availSpots = self.getAvailableSpots()
        
        if self._get_winner() != None: 
            if player == 'player':
                return {'score': 10}
            else:
                return {'score': -10}
        elif len(availSpots) == 0:
            return {'score': 0}

        moves = []
        for emptySpot in availSpots:
            move = {'index': emptySpot, 'score': 0}
            if player == 'ai':
                emptySpot.text = self.symbols['ai']
                result = self.minimax('player')
                move['score'] = result['score']
            else:
                emptySpot.text = self.symbols['player']
                result = self.minimax('ai')
                move['score'] = result['score']

            emptySpot =  move['index'].text = ''
            moves.append(move);

        bestMove = None
        if player == 'ai':
            bestScore = -10000
            for move in moves:
                if move['score'] > bestScore:
                    bestScore = move['score']
                    bestMove = move
        else:
            bestScore = 10000
            for move in moves:
                if move['score'] < bestScore:
                    bestScore = move['score']
                    bestMove = move

        return bestMove
#-------------ai^^


    def _check_status(self, ai=False):
        """
            Checks board status
        """
        winner = self._get_winner()
        spots = len(self.getAvailableSpots())

        if winner or spots == 0:
            close_button = Button(text='Close')
            content = BoxLayout(orientation='vertical')

            popup = None
            if spots == 0:
                content.add_widget(Label(text='tie!'))
                content.add_widget(close_button)
                popup = Popup(title='tie!', content=content, size_hint=(.8, .8))
            elif winner:
                content.add_widget(Label(text='%s won the game!' % winner))
                content.add_widget(close_button)
                popup = Popup(title='%s won!' % winner, content=content, size_hint=(.8, .8))

            popup.open()
            close_button.bind(on_press = lambda *args: popup.dismiss())
            self._restart_board()
        else:
            return True


    def _get_winner(self):
        """
            Returns winning symbol or None
        """
        values = [[col.text for col in row] for row in self.grid]

        # check horizontal
        for row in values:
            result = self._is_same_symbol(row)
            if result:
                return result

        # check vertical
        for row in [list(row) for row in zip(*values)]:
            result = self._is_same_symbol(row)
            if result:
                return result

        # check forward diagonal
        forward_diagonal = [row[col] for col, row in enumerate(values)]
        result = self._is_same_symbol(forward_diagonal)
        if result:
            return result

        # check backwards diagonal
        backwards_diagonal = [row[-col-1] for col, row in enumerate(values)]
        result = self._is_same_symbol(backwards_diagonal)
        if result:
            return result

        return None


    def _is_same_symbol(self, row):
        for symbol in SYMBOLS:
            if [symbol for _ in range(self.cols)] == row:
                return symbol
        return False


    def _restart_board(self):
        for row in self.grid:
            for col in row:
                col.text = ''