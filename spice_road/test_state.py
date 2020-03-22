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

    This game consists of multiple players, with 2 game decks:

    * Trader cards
    * Scoring cards
    * A set of resource cubes
    * Set of gold and Silver coins

    Each player will have in their own playing area:

    * A hand of trader cards not visible to others
    * A hand of trader cards which has been used
    *
    * A hand of sc
    """
    assert isinstance(state.deck, Deck)
    assert len(state.deck) == 52

    for player_state in state.players:
        assert isinstance(player_state, PlayerState)
        assert isinstance(player_state.hand, Deck)
        assert len(player_state.hand) == 0
