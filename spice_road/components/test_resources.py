import pytest


@pytest.mark.xfail
def test_resources():
    """## Resources

    There are 4 set of resources:

    * Tumeric (Yellow)
    * Saffaron (Red)
    * Cardamom (Green)
    * Cinnamon (Black)

    Each of these resources are in order of the value, and there are upgrade cards
    that can upgrade these resources to the next level.

    See card_upgrade for detail.
    """
    raise NotImplementedError()


@pytest.mark.xfail
def test_caravan():
    """## Caravan

    Each player have caravan cards to which you can put your spice.

    The Caravan card is limited to 10 spices, and you cannot exceed the capacity
    of the caravan card
    """
    raise NotImplementedError()
