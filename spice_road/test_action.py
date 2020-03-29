import pytest

from playtest.logger import Announcer

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

from .components.cards import TraderCard, TraderDeck, ConversionCard, ScoringCard
from .components.resources import Resource, Caravan
from .components.river import TraderRiver, ScoringRiver
from .components.coins import Coin
from .constants import Param

# importing fixture
from .test_state import state


def test_trade(state: State):
    """## Trade action

    The trade action will take resources from your caravan and output it to your
    caravan.
    """
    # Arrange: Setup card in hands, and resources in Caravan
    ps = state.players[0]
    ps.hand = TraderDeck(
        [
            TraderCard("-> YY", uid=91),
            TraderCard("YY -> R", uid=92, test_watermark="Traded card"),
            TraderCard("YYY -> R", uid=93, test_watermark="Not tradable"),
        ]
    )
    ps.caravan = Caravan("YY")

    # Assert - how do we consider the trade?
    # Note that this is based on position of the card slot (zero based)
    action_range = ActionTradeRange(state, player_id=0)
    assert str(action_range) == "trade([0,1])"

    action = ActionTrade(1)
    assert action_range.is_valid(action)

    empty_action_range = action.resolve(state, player_id=0)
    assert empty_action_range is None
    assert len(ps.hand) == 2, "Card removed from player hand"
    assert len(ps.used_hand) == 1, "Card removed"
    assert ps.used_hand[0].test_watermark == "Traded card"
    assert ps.caravan == Resource("R"), "Traded two yellow as red"


def test_trade_from_str(state: State):
    action = ActionTrade.from_str("trade(0)")
    assert action == ActionTrade(0)


def test_exchange(state: State):
    ps = state.players[0]
    ps.hand = TraderDeck(
        [
            ConversionCard("Convert(2)", uid=91, test_watermark="Traded card"),
            TraderCard("YY -> R", uid=92),
        ]
    )
    ps.caravan = Caravan("YYRG")

    # Assert - how do we consider the trade?
    action_range = ActionTradeRange(state, player_id=0)
    assert str(action_range) == "trade([0,1])"

    # Now let's trade for the convert card
    action = ActionTrade(0)
    assert action_range.is_valid(action)

    # Now from resolve you are going to get a new action range
    # Since the convert card can ask for new value!
    new_action_range = action.resolve(state, player_id=0)
    assert isinstance(new_action_range, ActionConvertRange)
    assert str(new_action_range) == "convert([RG,YG,YR,YY])"

    action_convert = ActionConvert("YR")  # type: ignore
    assert new_action_range.is_valid(action_convert)

    empty_action_range = action_convert.resolve(state, player_id=0)
    assert empty_action_range is None
    assert len(ps.hand) == 1, "Card removed from player hand"
    assert len(ps.used_hand) == 1, "Card removed"
    assert ps.used_hand[0].test_watermark == "Traded card"
    assert ps.caravan == Resource("YRGG"), "YR is upgraded"


def test_acquire(state: State):
    """## Acquiring cards

    To acquire cards, you take a spice of your choice and put it onto the each
    card to the left of your caravan, and pick up the card
    """
    # Arrange: Trade river set
    state.trader_river = TraderRiver(
        cards=[
            # Most expensive, need pay 1 coin for each item
            TraderCard("-> Y", uid=90),
            TraderCard("-> YY", uid=91, test_watermark="obtained"),
            TraderCard("-> YYY", uid=92),
            TraderCard("-> YYYY", uid=93),
            TraderCard("-> YYYYY", uid=94),
            TraderCard("-> YYYYYY", uid=95),
        ],
        resources=[
            Resource("YYY"),
            Resource("RR"),
            Resource("Y"),
            Resource(""),
            Resource(""),
            Resource(""),
        ],
    )
    ps = state.players[0]
    # Clear player's hand of default cards
    ps.hand = TraderDeck([])
    ps.caravan = Caravan("YY")
    assert len(state.trader_river) == Param.number_of_trader_slots

    action_range = ActionAcquireRange(state, player_id=0)

    assert (
        str(action_range) == "acquire([0,1,2])"
    ), "We have 2 resource, and can obtain the top 3 cards from river"

    # Acquire based on positio n
    action = ActionAcquire(1)
    assert action_range.is_valid(action)

    action.resolve(state, player_id=0, a=Announcer())

    assert ps.hand[0].test_watermark == "obtained", "New card in player hands"
    assert ps.caravan == Caravan(
        "YRR"
    ), "Put down one resource for top card, and got resources"
    # NOTE: currently just assume you put the cheapest resource for now
    assert (
        state.trader_river.to_data()[0]["resources"] == "YYYY"
    ), "Test data representation"
    assert state.trader_river[0]["resources"] == Resource(
        "YYYY"
    ), "One extra resource put on head of the river"
    assert state.trader_river[1]["card"].uid == 92, "Card shifted over by 1"
    assert state.trader_river[1]["resources"] == Resource("Y"), "No resource added"
    assert (
        len(state.trader_river) == Param.number_of_trader_slots
    ), "River card was restored"


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


def test_score(state: State):
    """## Score

    To score, you pick a scoring card that you can satisfy with
    the number of spices.

    If you take the first or 2nd point cards, then take the gold / silver coin
    from it.
    """
    state.scoring_river = ScoringRiver(
        cards=[
            ScoringCard("RRRR (5)", uid=90, test_watermark="Scored"),
            ScoringCard("RRRRR (6)", uid=91),
            ScoringCard("RRRRRR (7)", uid=92),
            ScoringCard("RRRRRRR (8)", uid=93),
            ScoringCard("RRRRRRRR (9)", uid=93),
        ],
        resources=[Coin("GGGG"), Coin("SSSS"), Coin(""), Coin(""), Coin(""),],
    )
    ps = state.players[0]
    ps.caravan = Caravan("RRRRR")
    ps.coins = Coin("")
    assert len(state.scoring_river) == Param.number_of_scoring_slots

    action_range = ActionScoreRange(state, player_id=0)
    assert str(action_range) == "score([0,1])", "We have enough resource to score the 2"

    action = ActionScore(0)
    assert action_range.is_valid(action)

    action.resolve(state, player_id=0)

    assert ps.coins == Coin("G")
    assert ps.scored[0].test_watermark == "Scored", "Obtained scored card"
    assert len(state.scoring_river) == Param.number_of_scoring_slots, "Card is replaced"


@pytest.mark.xfail
def test_score_depleted_gold(state: State):
    """If you taken the last gold coin, move the silver coin to the stack
    """
    raise NotImplementedError()
