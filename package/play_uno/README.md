# Play UNO in the command line

## Blogpost
Please consider to also read my blogpost on [Medium](https://medium.com/@ma.draws/boston-or-seattle-an-airbnb-perspective-df0ababbbeb6).

## Authors and Licensing
- Author: Martin Draws

- License [MIT License](https://opensource.org/license/mit)

## Functionality
This module for Pyrhon enables the user to play the famous game UNO in the comment line.

First the module has to be imported. Then a game named 'uno' is created. In this example it has four players.
The user can choose between 3 and 10 players.

Afterwards the game is started by *uno.play()*.

```
from play_uno.Game import Game

uno = Game(4)

uno.play()
```

The user plays always as player 1. He or she can choose a card from his/her deck to play by index. If there is no valid card, a card is drawn automatically. If there is still no valid card to play, it's the next player's turn.

The other players are computer players. That means thy play cards automatically without user input.

The game play looks as follows:

![Game play](https://github.com/mdraws86/UNO/blob/development/images/Gameplay.png)

If the first player hasn't got any cards left in his/her deck, this player wins the game and it is ended. There are no further rounds for second or third place.

Have fun :)