import pytest


@pytest.mark.xfail
def test_trade_exchange():
    """## Trade card: Exchange

    There are two types of trade cards.  The exchange cards take a set of
    source spices to the target.  As long as you have enough spices,
    you can trade the spices for a set in the target space for spice.
    """
    raise NotImplementedError()


@pytest.mark.xfail
def test_trade_conversion():
    """## Trade card: Conversion

    Another set of cards is to allow conversion.  The conversion card
    allow us to follow the rule of resources to upgrade the spices.
    """
    raise NotImplementedError()
