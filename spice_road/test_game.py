import pytest

from .game import Game
from .constants import Param

NUMBER_OF_PLAYERS = 2


@pytest.fixture
def game() -> Game:
    param = Param(number_of_players=NUMBER_OF_PLAYERS)
    g = Game(param=param)
    return g


@pytest.mark.xfail
def test_round(game: Game):
    """# Game round

    Each player takes one of the above action from the rounds.
    """
    # Test playing player 0
    game_gen = game.play_round(0)

    raise NotImplementedError()


@pytest.mark.xfail
def test_end_game(game: Game):
    """## Game end

    Game end after any of the players have achieved their 5th card.
    (Note: in 2-3 players, 6th card).
    """
    raise NotImplementedError()


@pytest.mark.xfail
def test_victory(game: Game):
    """# Victory condition

    * Player counts up their scoring cards.
    * Each gold is 3 points
    * Each silver coin is 1 point.
    * Each resources that is better than tumeric win the game.

    The player with most points win.  In case of tie, the player with the
    later turn order win.
    """
    raise NotImplementedError()
