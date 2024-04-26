from Card import Card
from Deck import Deck
from Player import Player, ComputerPlayer
from typing import Dict, List
import random

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

        # We also need a stack where the played cards are stored
        # draw current card from game's deck
        self.stack = [self.deck.deck.pop()]
        self.current_stack_card = self.give_current_stack_card()
        if self.current_stack_card.is_face_down:
             self.current_stack_card.flip()

        players = {}
        players['player1'] = Player(name = 'Player1')
        for p in range(2, n_players + 1):
            players['player' + str(p)] = ComputerPlayer(name = 'Player' + str(p))
        for p in range(1, n_players + 1):
            # draw cards from deck
            for i in range(7):
                players['player' + str(p)].get_card(self.deck.draw_card())
        
        self.players = players

        # Initialize current wish for a color
        self.current_wish = None

        # Initialize how many times 'draw two' has been played
        self.times_draw_two = 0

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
    
    def give_current_stack_card(self) -> Card:
        '''Method to make current stack card accessible.
        
        Input:
            None

        Output:
            Current stack card [Card]
        '''
        current_stack_card = self.stack[-1]
        return current_stack_card
    
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

        # Initialize variable to indicate whether a player has drawn cards and can play a card afterwards or if he extended 'draw two' and can thus play no further cards
        # Even if there was no 'draw two' card played, we need the variable set to True to play a card
        has_drawn = True

        info = "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.value) if self.current_stack_card.action is None else "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.action)
        print('Current stack card: {}'.format(info))
        if self.current_stack_card.action == 'draw two':
            self.times_draw_two += 1
            # Check if the current player has 'draw two' to extend
            has_draw_two = bool(len([x for x in self.players[current_player].cards if x.action == 'draw two']))
            if has_draw_two:
                # If the player is a computer player it will always extend
                if self.players[current_player].is_computer_player:
                    has_drawn = False
                # Else the player can choose how to proceed
                else:
                    print({'0': 'extend', '1': 'draw {} cards'.format(2 * self.times_draw_two)})
                    has_drawn = bool(int(input("select action by index: ")))
                if has_drawn:
                    for i in range(2 * self.times_draw_two):
                        self.players[current_player].get_card(self.deck.draw_card())
                    print("{0} has drawn {1} cards from the deck.".format(self.players[current_player].name, 2 * self.times_draw_two))
                    self.times_draw_two = 0
                else:
                     current_card = self.players[current_player].play_draw_two()
            else:
                for i in range(2 * self.times_draw_two):
                    self.players[current_player].get_card(self.deck.draw_card())
                print("{0} has drawn {1} cards from the deck.".format(self.players[current_player].name, 2 * self.times_draw_two))
                self.times_draw_two = 0
                
        if has_drawn:
            current_card, self.current_wish = self.players[current_player].play_card(self.current_stack_card, self.current_wish, self.deck)
            if self.current_wish is not None:
                    print("Current wish: ", self.current_wish)
            if current_card is not None:
                self.stack += [current_card]
                self.current_stack_card = self.give_current_stack_card()
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

        # If the number of cards in the deck gets small we need to fill it up with the cards in the stack again. 
        # Before we do that we keep the uppermost card and sort the other cards in the stack randomly.
        # Then these cards are added to the deck again.
        if self.deck.n_cards <= 10:
             uppermost_card = self.stack.pop()
             random.shuffle(self.stack)
             self.deck = self.stack + self.deck
             self.stack = [uppermost_card]
