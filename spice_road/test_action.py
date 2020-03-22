import pytest

from .state import State
from .action import ActionHit

# importing fixture
from .test_state import state


@pytest.mark.xfail
def test_trade(state: State):
    """## Trade action

    The trade action will take resources from your caravan and output it to your
    caravan.
    """
    raise NotImplementedError()


@pytest.mark.xfail
def test_acquire(state: State):
    """## Acquiring cards

    To acquire cards, you take a spice of your choice and put it onto the each
    card to the left of your caravan, and pick up the card
    """
    raise NotImplementedError()


@pytest.mark.xfail
def test_rest(state: State):
    """## Rest

    To rest, you take all the cards you have played before back into your
    hand.
    """
    raise NotImplementedError()


@pytest.mark.xfail
def test_score(state: State):
    """## Score

    To score, you pick a scoring card that you can satisfy with
    the number of spices.

    If you take the first or 2nd point cards, then take the gold / silver coin
    from it.
    """
    raise NotImplementedError()


@pytest.mark.xfail
def test_score_depleted_gold(state: State):
    """If you taken the last gold coin, move the silver coin to the stack
    """
    raise NotImplementedError()
