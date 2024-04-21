from Card import Card
from Deck import Deck
from typing import List, Tuple
from collections import Counter
import random

class Player:
    def __init__(self,
                 name: str,
                 is_your_turn: bool = False,
                 has_won: bool = False) -> None:
        '''
        Method to initialize a player. A player has no cards at the beginning
        and it's his or her turn or not. He or she has won or not.

        Input:
            name (str): the player's name. Could just be 'Player 1'.
            is_your_turn (bool): is it the player's turn?
            has_won (bool): Has player won the game or is he still playing?

        Output:
            None
        '''

        self.cards: List[Card] = []
        # Player has name
        self.name = name
        self.is_your_turn = is_your_turn
        self.has_won = has_won
        # Player can wish for a color if he/she plays a wildcard. Wish is initiated here
        self.wish = None
        self.n_cards = len(self.cards)

    def __repr__(self) -> str:
        '''Method to print information about the player.
        
        Input:
            None
        
        Output:
            String with information about the player.
        '''
        return "----------------\nName: {0} \nNumber of cards: {1}\n----------------".format(self.name, self.n_cards)

    def count_cards(self) -> int:
        '''
        Method to count the current number of cards a player has.

        Input:
            None
        
        Output:
            numer of cards the player possesses (int).
        '''
        self.n_cards = len(self.cards)
        return len(self.cards)


    def get_card(self, card: Card) -> None:
        '''
        Method to get a card.

        Input:
            card (Card): card that should be added to a player's deck

        Output:
            None
        '''

        self.cards += [card]
        # Update amount of cards
        n_cards = self.count_cards()
        self.n_cards = n_cards

    def check_for_valid_cards(self, card: Card, wish: str, players_deck: Deck) -> bool:
        '''
        Method to investigate whether the player has a valid card to play for a given card.

        Input:
            card (Card): Given card for which the player needs a valid card.
            wish (str): the color the previous player wished for in case he/she played a wildcard.
            players_deck (List[Card]): a deck to look up. Usually the players's deck.

        Output:
            (bool) player has valid card(s) or not.
        '''
        # collect every valid card in a list
        if card.color == 'black':
            valid = [x for x in players_deck if x.color == wish.lower()]
        else:
            valid = [x for x in players_deck if (x.color == card.color)
                    or ((x.value == card.value) and card.value is not None) \
                    or ((x.action == card.action) and card.action is not None) \
                    or (x.color == 'black')]
        
        if len(valid) == 0:
            return False
        return True

    def play_card(self, card: Card, wish: str, deck: Deck) -> Tuple[Card, str]:
        '''
        Method to play a card depending on the previous played card.

        Input:
            card (Card): the previously played card.
            wish (str): the color the previous player wished for.
            deck (deck): a deck from which the player might draw cards.

        Output:
             played_card (Card): card the player plays or None if he/she is not able to play a card.
             wish (str): in case of a wild card the color the player wishes for otherwise None.
        '''

        # Check for valid cards in player's deck for the uppermost card on the stack
        has_valid = self.check_for_valid_cards(card, wish, self.cards)
        move = 0 # did player already draw a card?

        while not has_valid and move == 0:
            # Player draws card from deck
            self.get_card(deck.draw_card())

            # Update number of cards
            self.n_cards = self.count_cards()

            # Player made a move
            move += 1
            print("{} has drawn a card from the deck.".format(self.name))

            # Check again for valid cards in deck
            has_valid = self.check_for_valid_cards(card, wish, self.cards)

        # If the player has no valid card, even if he drew a card from the deck, he/she can't play a card in the current round
        if not has_valid:
            print("{} has no card to play.".format(self.name))
            played_card = None
            self.wish = wish
        else:
            # Initialize a dictionary for the player's cards, so the user can choose a card by its index
            players_cards = {}
            # Insert the info of a card
            for i, c in enumerate(self.cards):
                if c.is_face_down:
                    c.flip()
                players_cards[i] = "{0}, {1}".format(c.color, c.value) if c.action is None else "{0}, {1}".format(c.color, c.action)
            # To give the player an overview, print available cards
            print("{0}: {1}".format(self.name, players_cards))
            # Now the player has to choose a card
            # Initialize valid as False
            valid = False
            # If the player selects an invalid card he has to be asked again to choose one
            while not valid:
                index = int(input("Select card from your deck via index: "))
                # check if the selected card is allowed to played
                valid = self.check_for_valid_cards(card, wish, [self.cards[index]])
                # if the selected card is allowed to be played we remove it from the player's deck and play it
                if valid:
                    played_card = self.cards.pop(index)
                    # in this case player can't wish for a color
                    self.wish = None
                    # If the player plays a wildcard, he/she can wish for a color to be played next
                    if played_card.color == 'black':
                        self.wish = input("Please choose the color to be played next: ")
                        # Color has to be checked if valid
                        while self.wish.lower() not in ['red', 'yellow', 'blue', 'green']:
                            print("Color invalid. Please select again.")
                            self.wish = input("Please choose the color to be played next: ")
                else:
                    print("Card is not valid, please select another one.")

        # Update amount of cards
        self.n_cards = self.count_cards()
        
        # Print current status for player
        print(self.__repr__())

        # If the player has only one card left, he/she has to say 'UNO'
        if self.n_cards == 1:
            print("{}: UNO!!!!".format(self.name))

        return (played_card, self.wish)
    
    # A class for a computer player is also added
class ComputerPlayer(Player):
    def __init__(self, name) -> None:
        '''
        Method to initialize a computer player. A computer player inherits from a player.

        Input:
            name (str): name of the player.

        Output:
            None
        '''
        self.name = name

        Player.__init__(self, name = self.name)

        # Store the most frequent color except black the computer player has
        self.most_freq_color = self.find_most_frequent_color()

    def find_most_frequent_color(self) -> str | None:
        '''Method to find the most frequent color the computer player has.
        This information makes it easier to decide which color a computer player
        should wish for when it plays a wildcard.
        
        Input:
            None
        
        Output:
            color (str) or None if player's deck is empty.
        '''
        # Store all colors of the cards in a list ecept black
        colors = [x.color for x in self.cards if x.color != 'black']
        # Store all black colors in a separate list
        black = [x.color for x in self.cards if x.color == 'black']
        if len(colors) > 0:
            # If the player has colored cards we find the most frequent one
            counter = Counter(colors)
            color = counter.most_common()[0][0]
        elif len(black) > 0:
            # If the player only has black cards left in its deck, we can choose a color randomly
            color = random.choice(['red', 'green', 'blue', 'yellow'])
        else:
            # In case the player does not have any cards
            color = None
        return color
    
    def get_card(self, card: Card) -> None:
        '''Add functionality to count most frequent color to parent method get_card.
        
        Input:
            card (Card): card that should be added to a player's deck

        Output:
            None
        '''
        super().get_card(card)
        # Update most frequent color
        self.most_freq_color = self.find_most_frequent_color()