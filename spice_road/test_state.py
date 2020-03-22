import pytest

from playtest import Visibility
from playtest.components import Counter

from .constants import Param
from .state import State, PlayerState
from .components.cards import Deck

NUMBER_OF_PLAYERS = 2


@pytest.fixture
def state() -> State:
    param = Param(number_of_players=NUMBER_OF_PLAYERS)
    return State(param=param)


def test_setup(state: State):
    """## Setup instructions

    Describe your game here, for example your game will require
    a set of cards, and each player will have their own hands.

    And each player will have their own hands.  None of these
    players have any cards.
    """
    assert isinstance(state.deck, Deck)
    assert len(state.deck) == 52

    for player_state in state.players:
        assert isinstance(player_state, PlayerState)
        assert isinstance(player_state.hand, Deck)
        assert len(player_state.hand) == 0
