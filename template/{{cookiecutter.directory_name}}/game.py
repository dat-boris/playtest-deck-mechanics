from playtest.game import Game as BaseGame

from .state import State
from .action import ActionFactory, ActionHitRange, ActionSkipRange
from .constants import Param

NUMBER_OF_ROUNDS = 3


class Game(BaseGame[State, ActionFactory, Param]):
    def __init__(self, param, **kwargs):
        self.state = State(param=param)
        self.action_factory = ActionFactory(param=param)
        super().__init__(param=param, **kwargs)

    def start(self):
        for _ in range(NUMBER_OF_ROUNDS):
            yield from self.play_round()

    def play_round(self):
        for i in range(self.number_of_players):
            # Note that get_player_action is a generator
            action = yield from self.get_player_action(
                i, accepted_range=[ActionHitRange, ActionSkipRange]
            )
            self.announcer.say(f"Player {i+1} took action {action}")
            action.resolve(self.state, player_id=i)
