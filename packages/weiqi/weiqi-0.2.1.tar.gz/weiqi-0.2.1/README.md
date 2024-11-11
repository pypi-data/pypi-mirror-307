# weiqi.py - Library for the game of Go

This is a library for the game of Go. It is written in Python and is designed to be easy to understand and use. It is also designed to be easy to extend and modify.

### Usage

To use this library, you need to have Python installed on your computer.

To install the library, you can use the following command:

```
pip install weiqi
```

To use the library, you can import it in your Python code like this:

```python
from weiqi import Board, WeiqiGame, Player, Stone


# Example user implementation
class User:
    def __init__(self, name: str):
        self.name = name

# If you want to adapt the Player class to your User class
# you can create an adapter class like this
class PlayerAdapter(User, Player):
    def __init__(self, name: str, stone: Stone):
        User.__init__(self, name)
        Player.__init__(self, stone)

    # Override the __eq__ method to compare the user
    def __eq__(self, other):
        if not isinstance(other, PlayerAdapter):
            return NotImplemented
        return self.name == other.name and self.figure == other.figure


player_black = PlayerAdapter("Alice", Stone.BLACK)
player_white = PlayerAdapter("Bob", Stone.WHITE)

# 19x19 board
board = Board.generate_empty_board(19)

game: WeiqiGame[User] = WeiqiGame(
    player_black=player_black, player_white=player_white, board=board
)

# Then you can implement user interaction with the game
# through various interfaced (Example: CLI, GUI, etc.)
# You can also implement AI players

```

### Testing

To run the tests, you can use the following command:

```
python -m unittest discover -s tests
```

### Example

<img src="example/example.png" alt="Example of the library in use" width="400"/>

You can see an example with a simple Pygame GUI in the `example/pygame_example.py` file.

For starting the example, you can run the following command:
```
poetry install --only example
python example/pygame_example.py
```

After running the command, you should see a window pop up with a Go board. You can click on the board to place stones.

### TODO

- [ ] New example pygame for v0.2.0 (with the new features)
- [ ] Implement the time control system
- [ ] Implement the AI players