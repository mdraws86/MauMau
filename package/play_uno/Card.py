# Import modules
from typing import List

class Card:
    def __init__(self, 
                 color: str,
                 value: int,
                 action: str,
                 is_face_down: bool = True) -> None:
        '''
        Method to initialise a card.

        Input:
            color (str): color of the card, in UNO usually red, blue, green or yellow.
            value (int): value of a card, numer between 0 and 9
            action (str): action a card calls, e.g. reverse
            is_face_down (bool): is card face down or not?

        Output:
            None 
        '''
        self.color = color
        self.value = value
        self.action = action
        self.is_face_down = is_face_down

    def __repr__(self) -> str:
        '''Method to print color, value and action attributes.
        
        Input:
            None

        Output:
            info about the card (str).
        '''

        # if face down no information is revealed
        if self.is_face_down:
            return "face down"
        # else all not None information about the card is printed
        else:
            if self.value is None:
                return ", ".join(filter(None, (self.color, self.value, self.action)))
            else:
                return ", ".join(filter(None, (self.color, str(self.value), self.action)))

    def flip(self) -> None:
        '''
        Method to flip a card from face down to face up and vice versa.

        Input:
            None

        Output:
            None
        '''

        if self.is_face_down:
            self.is_face_down = False
        else:
            self.is_face_down = True