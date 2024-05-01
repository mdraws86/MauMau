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

![Game play](/Users/martindraws/Github/UNO/images/Gameplay.png)
