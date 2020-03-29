import pytest

from playtest.action import ActionInstance

from .game import Game
from .constants import Param

from .action import ActionAcquire, ActionTrade, ActionConvert, ActionRest

from .components.cards import (
    TraderCard,
    TraderDeck,
    ConversionCard,
    ScoringCard,
    ScoringDeck,
)
from .components.resources import Resource, Caravan
from .components.river import TraderRiver, ScoringRiver
from .components.coins import Coin


NUMBER_OF_PLAYERS = 2


@pytest.fixture
def game() -> Game:
    param = Param(number_of_players=NUMBER_OF_PLAYERS)
    g = Game(param=param)
    state = g.s
    state.scoring_river = ScoringRiver(
        cards=[
            ScoringCard("RRRR (5)", uid=0, test_watermark="Scored"),
            ScoringCard("RRRRR (6)", uid=1),
            ScoringCard("RRRRRR (7)", uid=2),
            ScoringCard("RRRRRRR (8)", uid=3),
        ],
        resources=[Coin("GGGG"), Coin("SSSS"), Coin(""), Coin(""),],
    )
    state.trader_river = TraderRiver(
        cards=[
            TraderCard("-> YY", uid=0),
            TraderCard("-> YY", uid=1),
            ConversionCard("Convert(2)", uid=2, test_watermark="Obtained"),
            TraderCard("-> YY", uid=3),
        ],
        resources=[Resource("YYY"), Resource("YY"), Resource("Y"), Resource(""),],
    )
    ps = state.players[0]
    ps.hand = TraderDeck([])
    ps.caravan = Caravan("YYYY")
    return g


def test_round(game: Game):
    """# Game round

    Each player takes one of the above action from the rounds.
    """
    # Test playing player 0
    game_gen = game.start()
    next_player_id, possible_actions, _ = next(game_gen)

    assert next_player_id == 0
    assert list(map(str, possible_actions)) == ["acquire([0,1,2,3,4])", "rest"]

    action_to_act: ActionInstance = ActionAcquire(2)
    next_player_id, possible_actions, _ = game_gen.send(action_to_act)

    ps = game.s.get_player_state(0)
    assert len(ps.hand) == 1
    assert ps.hand[0].test_watermark == "Obtained", "Card obtained"
    assert len(ps.caravan) == 3, "Spent 2 resource to obtain card"
    assert next_player_id == 1, "Moved to next player"

    action_to_act = ActionRest()
    next_player_id, possible_actions, _ = game_gen.send(action_to_act)
    assert next_player_id == 0

    action_to_act = ActionTrade(0)
    next_player_id, possible_actions, _ = game_gen.send(action_to_act)
    assert next_player_id == 0
    assert len(ps.hand) == 0
    assert len(ps.used_hand) == 1

    assert list(map(str, possible_actions)) == ["convert([YY])"]
    action_to_act = ActionConvert("YY")
    next_player_id, possible_actions, _ = game_gen.send(action_to_act)
    assert ps.caravan == Resource("RRY"), "Resource upgraded"


@pytest.mark.xfail
def test_end_game(game: Game):
    """## Game end

    Game end after any of the players have achieved their 5th card.
    (Note: in 2-3 players, 6th card).
    """
    assert not game.is_end(), "Game ongoing if nobody have scoring cards"
    ps = game.s.get_player_state(0)
    ps.scored = ScoringDeck(
        [ScoringCard("RRRR (5)", uid=0, test_watermark="Scored")] * 5
    )
    assert game.is_end(), "Once have 5+ scored card, game is ending"


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
    # TODO: implement each of the score
    raise NotImplementedError()
