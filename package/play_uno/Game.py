from Card import Card
from Deck import Deck
from Player import Player, ComputerPlayer
from typing import Dict, List

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
        players['player1'] = Player(name = 'Player1')
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

        # Initialize player order
        self.player_order = list(self.players.keys())

    def __repr__(self) -> str:
        '''Method to print information about the game.
        
        Input:
            None

        Output:
            String with information about the game.
        '''
        return "Number of players: {}".format(len(self.players))
    
    def update_player_order(self) -> List[str]:
        '''Method to keep track of current player order.
        
        Input:
            None
        Output:
            List of players in their current order.
        '''
        # Previous player
        previous_player = self.player_order.pop(0)
        # Take previous player to the last position
        self.player_order.append(previous_player)

        return self.player_order
    
    def reverse_player_order(self) -> List[str]:
        '''Method to reverse the player order, e.g. when a reverse card is played.
        
        Inupt:
            None
        Output:
            List of players in their reverted order.
        '''
        self.player_order.reverse()
        return self.player_order
    
    def skip_player(self) -> List[str]:
        ''' Method to skip a player.

        Input:
            None
        
        Output:
            List of players in their updated order.
        '''
        previous_player = self.player_order.pop(0)
        skipped_player = self.player_order.pop(0)
        self.player_order.append(previous_player)
        self.player_order.append(skipped_player)

        return self.player_order

    def play_round(self):
        '''
        tbd
        '''

        current_player = self.player_order[0]
        print("It's {}'s turn".format(current_player))

        if self.current_wish is not None:
                print("Current wish: ", self.current_wish)

        info = "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.value) if self.current_stack_card.action is None else "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.action)
        print('Current stack card: {}'.format(info))
        if self.current_stack_card.action == 'draw two':
            for i in range(2):
                 self.players[current_player].get_card(self.deck.draw_card())
            print("{} has drawn two cards from the deck.".format(self.players[current_player].name))
        current_card, self.current_wish = self.players[current_player].play_card(self.current_stack_card, self.current_wish, self.deck)
        if self.current_wish is not None:
                print("Current wish: ", self.current_wish)
        if current_card is not None:
            self.current_stack_card = current_card
        info = "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.value) if self.current_stack_card.action is None else "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.action)
        print('Current stack card: {}\n'.format(info))
        if self.current_stack_card.action == 'reverse':
             self.reverse_player_order()
             print("Next_player:")
             print(self.player_order[0])
        elif self.current_stack_card.action == 'skip':
             self.skip_player()
             print("Next player:")
             print(self.player_order[0])
        else:
             self.update_player_order()
             print("Next_player:")
             print(self.player_order[0])