import pytest

from .game import Game
from .constants import Param

from .action import ActionAcquire

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


NUMBER_OF_PLAYERS = 4


@pytest.fixture
def game() -> Game:
    param = Param(number_of_players=NUMBER_OF_PLAYERS)
    g = Game(param=param)
    state = g.s
    state.scoring_river = ScoringRiver(
        [
            # Most expensive, need pay 1 coin for each item
            {
                "card": ScoringCard("RRRR (5)", uid=0, test_watermark="Scored"),
                "coin": Coin("GGGG"),
            },
            {"card": ScoringCard("RRRRR (6)", uid=1), "coin": Coin("SSSS"),},
            {"card": ScoringCard("RRRRRR (7)", uid=2), "coin": Coin(""),},
            {"card": ScoringCard("RRRRRRR (8)", uid=3), "coin": Coin(""),},
        ]
    )
    state.trader_river = TraderRiver(
        [
            # Most expensive, need pay 1 coin for each item
            {"card": TraderCard("-> YY", uid=0), "resources": Resource("YYY"),},
            {
                "card": TraderCard("-> YY", uid=1, test_watermark="Obtained"),
                "resources": Resource("YY"),
            },
            {"card": TraderCard("-> YY", uid=2), "resources": Resource("Y"),},
            {"card": TraderCard("-> YY", uid=3), "resources": Resource(""),},
        ]
    )
    ps = state.players[0]
    ps.hand = TraderDeck([])
    ps.caravan = Caravan("YY")
    return g


@pytest.mark.xfail
def test_round(game: Game):
    """# Game round

    Each player takes one of the above action from the rounds.
    """
    # Test playing player 0
    game_gen = game.play_round()
    next_player_id, possible_actions, _ = next(game_gen)

    assert next_player_id == 0
    # TODO: double check and validate
    assert list(map(str, possible_actions)) == ["...", "rest"]

    action_to_act = ActionAcquire(1)
    next_player_id, possible_actions, _ = game_gen.send(action_to_act)

    ps = game.s.get_player_state(0)
    assert len(ps.hand) == 1
    assert ps.hand[0].test_watermark == "Obtained", "Card obtained"
    assert next_player_id == 1, "Moved to next player"


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
