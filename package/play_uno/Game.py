from Card import Card
from Deck import Deck
from Player import Player, ComputerPlayer
from typing import Dict, List
import random
import time

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

        # Initialize if current player was able to play a card
        self.previous_player_has_played = True

        # Initialize how many times 'draw two' has been played
        self.times_draw_two = 0

        # Initialize a variable tracking if the deck is refilled
        # so we know if a single card in the stack is the very first card
        self.is_deck_refilled = False

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

        # The first card in the stack is drawn automatically. But we have to
        # take into account the action it might have. This action immediately
        # has influence on player 1
        if len(self.stack) == 1 and not self.is_deck_refilled and self.current_stack_card.action is not None:
            # If the first card is black, the player can wish for a color
            if self.current_stack_card.color == 'black':
                print("Most frequent color {0}: {1}".format(self.players[current_player].name, self.players[current_player].most_freq_color))
                while self.current_wish not in ['red', 'green', 'yellow', 'blue']:
                    self.current_wish = input("Please choose the color to be played next: ").lower()
                print("{0}: Current wish: {1}".format(self.players[current_player].name, self.current_wish))
            # If the action of the first card is 'skip' the first player is not allowed to play
            elif self.current_stack_card.action == 'skip':
                print("{} skipped.".format(self.players[current_player].name))
                self.skip_player()
                current_player = self.player_order[0]
                print("Next player:")
                print(self.player_order[0] + "\n")
            # If the action of the first card is 'reverse' the first player is allowed to play but the order is reversed afterwards
            elif self.current_stack_card.action == 'reverse':
                self.reverse_player_order()
                self.player_order = [self.player_order.pop()] + self.player_order
            else:
                pass

        if self.current_wish is not None:
                print("Current wish: ", self.current_wish)

        # Initialize variable to indicate whether a player has drawn cards and can play a card afterwards or if he extended 'draw two' and can thus play no further cards
        # Even if there was no 'draw two' card played, we need the variable set to True to play a card
        has_drawn = True

        info = "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.value) if self.current_stack_card.action is None else "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.action)
        print('Current stack card: {}'.format(info))
        # Complicated loop in case the previous player played 'draw two'
        # The player has the choice to extend 'draw two' if he can or just draw the requested amount of cards and play a card afterwards
        if self.current_stack_card.action == 'draw two' and self.previous_player_has_played:
            self.times_draw_two += 1
            # Check if the current player has 'draw two' to extend
            has_draw_two = bool(len([x for x in self.players[current_player].cards if x.action == 'draw two']))
            if has_draw_two:
                # If the player is a computer player it will always extend
                if self.players[current_player].is_computer_player:
                    has_drawn = False
                # Else the player can choose how to proceed
                else:
                    # Choose between 'extend' and 'draw two'
                    print({'0': 'extend', '1': 'draw {} cards'.format(2 * self.times_draw_two)})
                    has_drawn = bool(int(input("select action by index: ")))
                # If the player decided not to extend though he could, he/she draws cards and is still alowed to play a card afterwards
                if has_drawn:
                    # Draw amount of cards depending on how many times 'draw two' has been extended
                    for i in range(2 * self.times_draw_two):
                        self.players[current_player].get_card(self.deck.draw_card())
                    print("{0} has drawn {1} cards from the deck.".format(self.players[current_player].name, 2 * self.times_draw_two))
                    # Reset the amount of extensions to zero again
                    self.times_draw_two = 0
                    # Update player's number of cards
                    self.players[current_player].count_cards()
                # If the player decided to extend
                else:
                     # Choose card with action 'draw two' from player's deck
                     if not self.players[current_player].is_computer_player:
                        current_card = self.players[current_player].play_draw_two()
                     else:
                         current_card = self.players[current_player].play_draw_two(self.current_stack_card)
                     print("{} extends 'draw two'".format(self.players[current_player].name))
                     # Update stack
                     self.stack += [current_card]
                     self.current_stack_card = self.give_current_stack_card()
                     # In case the player extended 'draw two' it's the next player's turn
                     self.update_player_order()
                     info = "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.value) if self.current_stack_card.action is None else "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.action)
                     print('Current stack card: {}\n'.format(info))
                     print("Next_player:")
                     print(self.player_order[0] + "\n")
            # Else the player has no choice than to draw an amount of cards depending on how many times 'draw two' has been extended
            else:
                for i in range(2 * self.times_draw_two):
                    self.players[current_player].get_card(self.deck.draw_card())
                print("{0} has drawn {1} cards from the deck.".format(self.players[current_player].name, 2 * self.times_draw_two))
                if self.players[current_player].is_computer_player:
                    self.players[current_player].update_has_drawn(True)
                # Reset the amount of extensions to zero again
                self.times_draw_two = 0
        # In case the action is 'draw four' the player has no choice
        elif self.current_stack_card.action == 'choose color and draw four' and self.previous_player_has_played:
            for i in range(4):
                self.players[current_player].get_card(self.deck.draw_card())
            print("{} has drawn 4 cards from the deck".format(self.players[current_player].name))
        else:
            pass
                
        if has_drawn:
            current_card, self.current_wish = self.players[current_player].play_card(self.current_stack_card, self.current_wish, self.deck)
            if self.current_wish is not None:
                    print("Current wish: ", self.current_wish)
            if current_card is not None:
                self.stack += [current_card]
                self.current_stack_card = self.give_current_stack_card()
                self.previous_player_has_played = True
            else:
                self.previous_player_has_played = False
            if self.players[current_player].is_computer_player:
                    self.players[current_player].update_has_drawn(False)
            info = "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.value) if self.current_stack_card.action is None else "{0}, {1}".format(self.current_stack_card.color, self.current_stack_card.action)
            print('Current stack card: {}\n'.format(info))
            if self.current_stack_card.action == 'reverse' and self.previous_player_has_played:
                self.reverse_player_order()
                print("Next_player:")
                print(self.player_order[0])
            elif self.current_stack_card.action == 'skip' and self.previous_player_has_played:
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
             self.is_deck_refilled = True

    def play(self) -> None:
        '''Method to repeat play_round as long as all players have cards.
        
        Input:
            None

        Output:
            None
        '''

        # Play until the first player has no more cards
        while not any([self.players[player].n_cards == 0 for player in self.players.keys()]):
            self.play_round()
            # Wait 2 seconds for the next round
            time.sleep(2)
        winner = [self.players[player].name for player in self.players.keys() if self.players[player].n_cards == 0][0]
        print("-----------------\n-----------------\nWinner {}!!!!\n-----------------\n-----------------".format(winner))