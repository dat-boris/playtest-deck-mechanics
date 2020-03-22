from .test_state import test_setup
from .components.test_cards import test_deck
from .test_game import test_round, test_victory
from .test_action import test_hit

# This define the list of rules which we follow
RULE_TESTS = [
    """> `RULES.md`: do not modify this file - this is automatically generated
    by `mk_rules.py`
    """,
    test_setup,
    test_deck,
    test_round,
    test_hit,
    test_victory,
]
