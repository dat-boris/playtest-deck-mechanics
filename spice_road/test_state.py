import pytest

from playtest import Visibility
from playtest.components import Counter

from .constants import Param
from .state import State, PlayerState
from .components.cards import TraderDeck, ScoringDeck
from .components.river import ScoringRiver, TraderRiver
from .components.resources import Caravan
from .components.coins import Coin

NUMBER_OF_PLAYERS = 4


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
    * A hand of scoring cards which have been claimed
    """
    assert isinstance(state.trader_deck, TraderDeck)
    assert isinstance(state.scoring_deck, ScoringDeck)

    # These are the two rivers of card that we have
    assert isinstance(state.scoring_river, ScoringRiver)
    assert isinstance(state.trader_river, TraderRiver)

    for player_state in state.players:
        assert isinstance(player_state, PlayerState)
        assert isinstance(player_state.caravan, Caravan)
        assert isinstance(player_state.hand, TraderDeck)
        assert isinstance(player_state.scored, ScoringDeck)
        assert isinstance(player_state.coins, Coin)
        assert len(player_state.hand) == 0
        assert len(player_state.scored) == 0


@pytest.mark.xfail
def test_start_setup(state: State):
    """## Starting setup

    Each player, in order, gets:
    * Start player: 3 turmeric
    * 2nd and 3rd players: 4 turmeric each
    * 4th and 5th players: 3 turmeric and 1 saffron each

    Also open up:
    * 6 trader cards.
    * 5 scoring card, with the first one in the river contain same
     number of gold coins as player, 2nd one with same number of silver
     coins as player.
    """
    assert state.players[0].caravan == "YYY"
    assert state.players[1].caravan == "YYYY"
    assert state.players[2].caravan == "YYYY"
    assert state.players[3].caravan == "YYYR"

    assert len(state.trader_river) == 6
    assert len(state.scoring_river) == 5
    assert state.scoring_river[0]["coins"] == Coin("G" * NUMBER_OF_PLAYERS)
    assert state.scoring_river[1]["coins"] == Coin("S" * NUMBER_OF_PLAYERS)
