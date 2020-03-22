import pytest

from .game import Game
from .constants import Param

NUMBER_OF_PLAYERS = 2


@pytest.fixture
def game() -> Game:
    param = Param(number_of_players=NUMBER_OF_PLAYERS)
    g = Game(param=param)
    return g


def test_round(game: Game):
    """# Game round

    Now let's talk about each round of the game.

    At each round, the player can ask for a card, or not.  If they ask for
    a card, it is dealt to them.

    If not, no card is dealt.
    """
    game_gen = game.play_round()

    next_player_id, possible_actions, _ = next(game_gen)
    assert next_player_id == 0
    assert list(map(str, possible_actions)) == [
        "hit",
        "skip",
    ], "Player 1 have 2 choice of actions."


@pytest.mark.xfail
def test_victory(game: Game):
    """# Victory condition

    Well, we have not thought much about this!  We will get to this.
    """
    raise NotImplementedError()
