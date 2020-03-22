import pytest


from .cards import TraderCard, ScoringCard, ConversionCard


@pytest.mark.xfail
def test_trade_exchange():
    """## Trade card: Exchange

    There are two types of trade cards.  The exchange cards take a set of
    source spices to the target.  As long as you have enough spices,
    you can trade the spices for a set in the target space for spice.
    """
    r = TraderCard("RRR -> RBG")
    assert r.to_data() == "RRR -> BGR"
    assert r.src == Resource("RRR")
    assert r.dst == Resource("RBG")

    assert not r.can_trade(Resource("RR"))
    assert r.can_trade(Resource("RRRR"))
    assert r.trade(Resource("RRR")) == Resource("RBG")


@pytest.mark.xfail
def test_trade_conversion():
    """## Trade card: Conversion

    Another set of cards is to allow conversion.  The conversion card
    allow us to follow the rule of resources to upgrade the spices.
    """
    r = ConversionCard(2)
    assert r.to_data() == "Convert(2)"
    assert r.can_trade(Resource("YY"))
    assert r.trade(Resource("YY")) == Resource("RR"), \
        "Upgrade any 2 resources according to resource rule"


@pytest.mark.xfail
def test_scoring_card():
    """## Scoring card

    Each scoring card will have a victory point, and resources required.

    You will need to provide enough resources in order to obtain the
    scoring card.
    """
    r = ScoringCard("YYYBBB (3)")
    assert r.victory_point == 3
    assert r.target == Resource("BBBYYY")

    assert r.check_enough(Resource("YYBB")) is False
    assert r.check_enough(Resource("YYYYBBBBG")) is True
