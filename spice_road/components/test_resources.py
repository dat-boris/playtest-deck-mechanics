import pytest


from spice_road.components.resources import Resource, Caravan


def test_resources():
    """## Resources

    There are 4 set of resources:

    * Tumeric (Yellow)
    * Saffron (Red)
    * Cardamom (Green)
    * Cinnamon (Black)

    Each of these resources are in order of the value, and there are upgrade cards
    that can upgrade these resources to the next level.

    See card_upgrade for detail.
    """
    r = Resource("RBGY")
    assert (
        r.to_data() == "BGRY"
    ), "Resource representation is always sorted in alphabets"

    assert r.stack == {
        Resource.RED: 1,
        Resource.BLACK: 1,
        Resource.GREEN: 1,
        Resource.YELLOW: 1,
    }

    r = Resource("RRR")
    assert r.to_data() == "RRR"
    assert r.stack == {
        Resource.RED: 3,
        Resource.BLACK: 0,
        Resource.YELLOW: 0,
        Resource.GREEN: 0,
    }

    assert r.has_required(Resource("RR")) is True
    assert r.has_required(Resource("RRRR")) is False
    assert r.has_required(Resource("BBBB")) is False

    # Base state for the resources
    r.reset()
    assert r.to_data() == ""
    assert r.stack == {
        Resource.RED: 0,
        Resource.BLACK: 0,
        Resource.GREEN: 0,
        Resource.YELLOW: 0,
    }


def test_caravan():
    """## Caravan

    Each player have caravan cards to which you can put your spice.

    The Caravan card is limited to 10 spices, and you cannot exceed the capacity
    of the caravan card
    """
    # Note: we automatically remove the cheapest resoruces for now.
    # In real game, player have a choice on what resources to discard
    c = Caravan("RGBY")
    assert isinstance(c, Resource), "Caravan is a subtype of resource"

    c = Caravan("Y")
    c.discard_to(10)
    assert c.stack == {
        Resource.BLACK: 0,
        Resource.YELLOW: 1,
        Resource.GREEN: 0,
        Resource.RED: 0,
    }

    c = Caravan("Y" * 10 + "B" * 5)
    c.discard_to(10)
    assert c.stack == {
        Resource.BLACK: 5,
        Resource.YELLOW: 5,
        Resource.GREEN: 0,
        Resource.RED: 0,
    }

    c = Caravan("Y" * 0 + "R" * 5 + "B" * 15)
    c.discard_to(10)
    assert c.stack == {
        Resource.BLACK: 10,
        Resource.YELLOW: 0,
        Resource.GREEN: 0,
        Resource.RED: 0,
    }
