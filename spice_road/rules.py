from spice_road import test_state, test_action, test_game
from spice_road.components import test_resources, test_cards

# This define the list of rules which we follow
RULE_TESTS = [
    """> `RULES.md`: do not modify this file - this is automatically generated
    by `mk_rules.py`
    """,
    test_state.test_setup,
    test_state.test_start_setup,
    test_resources.test_resources,
    test_resources.test_caravan,
    test_cards.test_trade_exchange,
    test_cards.test_trade_conversion,
    """# Actions
    Each round, you can take one of the following actions:
    """,
    test_action.test_trade,
    test_action.test_acquire,
    test_action.test_rest,
    test_action.test_score,
    test_action.test_score_depleted_gold,
    """# Game play
    """,
    test_game.test_round,
    test_game.test_end_game,
    test_game.test_victory,
]
