from Card import Card
from typing import List
import random

class Deck:
    def __init__(self) -> None:
        '''
        Method to initialize a deck of cards.

        Input:
            None
        
        Output:
            None
        '''

        # Define deck as list of cards:
        deck: List[Card] = []

        # Colors for UNO cards
        colors = ['red', 'green', 'blue', 'yellow']

        # Two times numbers from 1 - 9 for colors red, blue, green and yellow
        for i in range(2):
            for c in colors:
                for v in range(1, 10):
                    deck += [Card(c, v, None)]

        # One time number 0 for each color
        for c in colors:
            deck += [Card(c, 0, None)]
        
        # All acions
        actions = ['reverse', 'draw two', 'skip']

        # Add actoins two times for each color
        for i in range(2):
            for c in colors:
                for a in actions:
                    deck += [Card(c, None, a)]

        # All black wild cards
        wilds = ['choose color', 'choose color and draw four']

        # Add wild cards four times for each type
        for i in range(4):
            for w in wilds:
                deck += [Card('black', None, w)]

        # Sort cards in deck randomly
        random.shuffle(deck)

        # Return randomly sorted deck
        self.deck = deck

        # Count number of cards in deck
        self.n_cards = self.count_cards()

    def __repr__(self) -> str:
        '''Print current number of cards in the deck.
        
        Input:
            None

        Output:
            String with information about number of cards in the deck.
        '''
        return "{} cards in the deck".format(self.n_cards)

    def refill(self, stack: List[Card]) -> None:
        '''
        Method to refill a deck, e.g. with already played cards when deck is empty.

        Input:
            stack (List[Card]): list of cards.

        Output:
            None
        '''

        # Refill deck with one or more cards in a list.
        self.deck += stack

    def count_cards(self) -> int:
        '''
        Method to count current number of cards in deck.

        Input:
            None
        
        Output:
            Number of cards in deck (int).
        '''
        n_cards = len(self.deck)
        return n_cards
    
    def draw_card(self) -> Card:
        '''Method to give uppermost card of the deck
        
        Input:
            None
        
        Output:
            the uppermost card in the deck.
        '''

        # Pop the uppermost card from the deck
        uppermost = self.deck.pop()
        # Flip card to reveal all information
        uppermost.flip()
        # Count number of cards again
        self.n_cards = self.count_cards()

        return uppermost