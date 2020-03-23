import pytest

from .state import State
from .action import (
    ActionTrade,
    ActionTradeRange,
    ActionConvert,
    ActionConvertRange,
    ActionAcquire,
    ActionAcquireRange,
    ActionRest,
    ActionScore,
    ActionScoreRange,
)

# importing fixture
from .test_state import state
from .components.cards import TraderCard, TraderDeck, ConversionCard, ScoringCard
from .components.resources import Resource, Caravan
from .components.river import TraderRiver, ScoringRiver
from .components.coins import Coin


@pytest.mark.xfail
def test_trade(state: State):
    """## Trade action

    The trade action will take resources from your caravan and output it to your
    caravan.
    """
    # Arrange: Setup card in hands, and resources in Caravan
    ps = state.players[0]
    ps.hand = TraderDeck(
        [
            TraderCard("-> YY", uid=1),
            TraderCard("YY -> R", uid=2, test_watermark="Traded card"),
            TraderCard("YYY -> R", uid=3, test_watermark="Not tradable"),
        ]
    )
    ps.caravan = Caravan("YY")

    # Assert - how do we consider the trade?
    action_range = ActionTradeRange(state, player_id=0)
    assert str(action_range) == "trade(1,2)"

    action = ActionTrade(2)
    assert action_range.is_valid(action)

    action.resolve(state, player_id=0)
    assert len(ps.hand) == 2, "Card removed from player hand"
    assert len(ps.used_hand) == 1, "Card removed"
    assert ps.used_hand[0].test_watermark == "Traded card"
    assert ps.caravan == Resource("R"), "Traded two yellow as red"


@pytest.mark.xfail
def test_exchange(state: State):
    ps = state.players[0]
    ps.hand = TraderDeck(
        [ConversionCard("Convert(2)", uid=1, test_watermark="Traded card"),]
    )
    ps.caravan = Caravan("YYRG")

    # Assert - how do we consider the trade?
    action_range = ActionConvertRange(state, player_id=0)
    assert str(action_range) == 'convert("YY", "YR", "YG", "RG")'

    action = ActionConvert("YR")
    assert action_range.is_valid(action)

    action.resolve(state, player_id=0)

    assert len(ps.hand) == 0, "Card removed from player hand"
    assert len(ps.used_hand) == 1, "Card removed"
    assert ps.used_hand[0].test_watermark == "Traded card"
    assert ps.caravan == Resource("YRGG"), "YR is upgraded"


@pytest.mark.xfail
def test_acquire(state: State):
    """## Acquiring cards

    To acquire cards, you take a spice of your choice and put it onto the each
    card to the left of your caravan, and pick up the card
    """
    # Arrange: Trade river set
    state.trader_river = TraderRiver(
        [
            # Most expensive, need pay 1 coin for each item
            {"card": TraderCard("-> YY", uid=0), "resources": Resource("YYY"),},
            {
                "card": TraderCard("-> YY", uid=1, test_watermark="obtained"),
                "resources": Resource("YY"),
            },
            {"card": TraderCard("-> YY", uid=2), "resources": Resource("Y"),},
            {"card": TraderCard("-> YY", uid=3), "resources": Resource(""),},
        ]
    )
    ps = state.players[0]
    ps.caravan = Caravan("YY")

    action_range = ActionAcquireRange(state, player_id=0)
    assert (
        str(action_range) == "acquire([0,1,2])"
    ), "We have 2 resource, and can obtain the top 3 cards from river"

    action = ActionAcquire(1)
    assert action_range.is_valid(action)

    action.resolve(state, player_id=0)

    assert ps.hand[0].test_watermark == "obtained", "New card in player hands"
    assert ps.caravan == Caravan("Y"), "Put down one resource for top card"
    # NOTE: currently just assume you put the cheapest resource for now
    assert state.trader_river[0]["resources"] == Resource(
        "YYYY"
    ), "One extra resource put on head of the river"
    assert state.trader_river[1]["card"].uid == 2, "Card shifted over by 1"
    assert state.trader_river[1]["resource"] == Resource("Y"), "No resource added"


@pytest.mark.xfail
def test_rest(state: State):
    """## Rest

    To rest, you take all the cards you have played before back into your
    hand.
    """
    ps = state.players[0]
    ps.hand = TraderDeck([])
    ps.used_hand = TraderDeck(
        [
            TraderCard("-> YY", uid=1, test_watermark="Restored"),
            TraderCard("-> YY", uid=2, test_watermark="Restored"),
        ]
    )

    action = ActionRest()

    action.resolve(state, player_id=0)
    assert len(ps.hand) == 2
    assert len(ps.used_hand) == 0
    assert ps.hand[0].test_watermark == "Restored"
    assert ps.hand[1].test_watermark == "Restored"


@pytest.mark.xfail
def test_score(state: State):
    """## Score

    To score, you pick a scoring card that you can satisfy with
    the number of spices.

    If you take the first or 2nd point cards, then take the gold / silver coin
    from it.
    """
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
    ps = state.players[0]
    ps.caravan = Caravan("RRRRR")
    ps.coins = Coin("")

    action_range = ActionScoreRange(state, player_id=0)
    assert str(action_range) == "score([0,1])", "We have enough resource to score the 2"

    action = ActionScore(0)
    assert action_range.is_valid(action)

    action.resolve(state, player_id=0)

    assert ps.coins == Coin("S")
    assert ps.scored[0].test_watermake == "Scored", "Obtained scored card"


@pytest.mark.xfail
def test_score_depleted_gold(state: State):
    """If you taken the last gold coin, move the silver coin to the stack
    """
    raise NotImplementedError()
