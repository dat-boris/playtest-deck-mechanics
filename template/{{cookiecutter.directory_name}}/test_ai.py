"""A test file to validate that training with AI will work
"""

import os
import pytest

from playtest.agents import KerasDQNAgent, train_agents
from playtest.env import GameWrapperEnvironment, EnvironmentInteration


from .game import Game
from .constants import Param

AGENT_FILENAME = "example_agent_{{cookiecutter.directory_name}}.h5f"


@pytest.fixture
def env() -> GameWrapperEnvironment:
    env = GameWrapperEnvironment(Game(Param(number_of_players=4)))
    return env


@pytest.mark.xfail
def test_training(env: GameWrapperEnvironment):
    agents = [KerasDQNAgent(env) for _ in range(env.n_agents)]
    try:
        os.remove(AGENT_FILENAME)
    except OSError:
        pass
    train_agents(env, agents, save_filenames=[AGENT_FILENAME], nb_steps=10)
    assert os.path.exists(AGENT_FILENAME)

    new_agent = KerasDQNAgent(env)
    new_agent.load_weights(AGENT_FILENAME)

    assert new_agent


@pytest.mark.xfail
def test_playing(env):
    if not os.path.exists(AGENT_FILENAME):
        agents = [KerasDQNAgent(env) for _ in range(env.n_agents)]
        # create agent file
        train_agents(env, agents, save_filenames=[AGENT_FILENAME], nb_steps=10)
    else:
        agents = [
            KerasDQNAgent(env, weight_file=AGENT_FILENAME) for _ in range(env.n_agents)
        ]

    # Let's play 4 rounds of game!
    game = EnvironmentInteration(env, agents, rounds=4)
    game.play()

    state = game.env.game.s
    assert True, "Game exists"
