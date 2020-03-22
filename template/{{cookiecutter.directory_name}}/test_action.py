from .state import State
from .action import ActionHit

# importing fixture
from .test_state import state


def test_hit(state: State):
    """### Getting a card

    A player can decide to get a card. A card will be dealt from the player's
    hand.
    """
    ps1 = state.get_player_state(0)

    assert len(ps1.hand) == 0

    action = ActionHit()
    action.resolve(state, player_id=0)

    assert len(ps1.hand) == 1
