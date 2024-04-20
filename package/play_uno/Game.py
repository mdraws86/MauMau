from Card import Card
from Deck import Deck
from Player import Player, ComputerPlayer

class Game:
    def __init__(self, n_players: int) -> None:
        '''
        Method to initialize a game.

        Input:
            n_players (int): number of players

        Output:
            None
        '''

        # We need a deck to play
        self.deck = Deck()

        players = {}
        players[1] = Player(name = 'Player1')
        for p in range(2, n_players + 1):
            players['player' + str(p)] = ComputerPlayer(name = 'Player' + str(p))
        for p in range(1, n_players + 1):
            # draw cards from deck
            for i in range(7):
                players['player' + str(p)].get_card(self.deck.draw_card())
        
        self.players = players

        # draw current card from game's deck
        current_stack_card = self.deck.deck.pop()
        if current_stack_card.is_face_down:
            current_stack_card.flip()
        self.current_stack_card = current_stack_card

        # Initialize current wish for a color
        self.current_wish = None

    def __repr__(self) -> str:
        '''Method to print information about the game.
        
        Input:
            None

        Output:
            String with information about the game.
        '''
        return "Number of players: {}".format(len(self.players))

    def play_round(self):
        '''
        tbd
        '''

        player_order = list(self.players.keys())

        if self.current_wish is not None:
                print("Current wish: ", self.current_wish)

        info = "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.value) if self.current_stack_card.action is None else "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.action)
        print('Current stack card: {}'.format(info))
        current_card, self.current_wish = self.players['player1'].play_card(self.current_stack_card, self.current_wish, self.deck)
        if self.current_wish is not None:
                print("Current wish: ", self.current_wish)
        if current_card is not None:
            self.current_stack_card = current_card
        info = "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.value) if self.current_stack_card.action is None else "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.action)
        print('Current stack card: {}\n'.format(info))