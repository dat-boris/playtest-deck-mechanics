from playtest.game import Game as BaseGame

from .state import State
from .action import ActionFactory
from .constants import Param

NUMBER_OF_ROUNDS = 3


class Game(BaseGame[State, ActionFactory, Param]):

    def __init__(self, param):
        self.state = State(param=param)
        self.action_factory = ActionFactory(param=param)
        super().__init__(param=param)

    def start(self):
        for _ in range(NUMBER_OF_ROUNDS):
            yield from self.play_round()

    def play_round(self):
        for i in range(self.number_of_players):
            # Note that get_player_action is a generator
            action = yield from self.get_player_action(i)
            self.announcer.say(f"Player {i+1} took action {action}")
            action.resolve()
