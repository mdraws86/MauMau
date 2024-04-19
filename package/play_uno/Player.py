from Card import Card
from Deck import Deck
from typing import List

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
        self.n_cards = len(self.cards)

    def __repr__(self) -> str:
        '''Method to print information about the player.
        
        Input:
            None
        
        Output:
            String with information about the player.
        '''
        return "Name: {0}, \nNumber of cards: {1}".format(self.name, self.n_cards)

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

    def check_for_valid_cards(self, card: Card, players_deck: Deck) -> bool:
        '''
        Method to investigate whether the player has a valid card to play for a given card.

        Input:
            card (Card): Given card for which the player needs a valid card.
            players_deck (List[Card]): a deck to look up. Usually the players's deck.

        Output:
            (bool) player has valid card(s) or not.
        '''
        # collect every valid card in a list
        valid = [x for x in players_deck if ((x.color == card.color or x.value == card.value) and x.action == None and card.action == None) \
                or ((x.color == card.color or x.action == card.action) and x.value == None and card.value == None) \
                or x.color == 'black']
        
        if len(valid) == 0:
            return False
        return True

    def play_card(self, card: Card, deck: Deck) -> Card:
        '''
        Method to play a card depending on the previous played card.

        Input:
            card (Card): the previously played card.
            deck (deck): a deck from which the player might draw cards.

        Output:
             Card object the player plays or None if he/she is not able to play a card.
        '''

        # Check for valid cards in player's deck for the uppermost card on the stack
        has_valid = self.check_for_valid_cards(card, self.cards)
        move = 0 # did player already draw a card?

        while not has_valid and move == 0:
            # Player draws card from deck
            self.get_card(deck.draw_card())

            # Player made a move
            move += 1
            print("{} has drawn a card from the deck.".format(self.name))

            # Check again for valid cards in deck
            has_valid = self.check_for_valid_cards(card, self.cards)

        # If the player has no valid card, even if he drew a card from the deck, he/she can't play a card in the current round
        if not has_valid:
            print("{} has no card to play.".format(self.name))
            played_card = None
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
                valid = self.check_for_valid_cards(card, [self.cards[index]])
                # if the selected card is allowed to be played we remove it from the player's deck and play it
                if valid:
                    played_card = self.cards.pop(index)
                else:
                    print("Card is not valid, please select another one.")

        print(self.__repr__())

        # Update amount of cards
        self.n_cards = self.count_cards()

        # If the player has only one card left, he/she has to say 'UNO'
        if self.n_cards == 1:
            print("{}: UNO!!!!".format(self.name))

        return played_card