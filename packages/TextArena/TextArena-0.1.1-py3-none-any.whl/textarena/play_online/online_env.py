from typing import Any, Dict, Optional, List
from textarena.play_online.api_client import APIClient
from textarena.core import Env, Observations, Rewards, Info
import time

class OnlineEnv(Env):
    def __init__(self, env_id: str, api_client: APIClient, game_name: Optional[str] = None):
        self.env_id = env_id
        self.api_client = api_client
        self.game_id = None
        self.game_key = None
        self.done = False
        self.info = {}
        self.observations = {}
        self.rewards = {}
        self.current_turn = 0

    def reset(self, seed: Optional[int] = None) -> Optional[Observations]:
        # Create a new game and add to matchmaking
        game_info = self.api_client.create_game(env_id=self.env_id, game_name=None)
        self.game_id = game_info['game_id']
        self.game_key = game_info['game_key']

        # Wait for the game to be in progress
        # Implement a polling mechanism to ensure the game has started
        # This is necessary because matchmaking may take some time
        max_wait_time = 15  # seconds
        wait_interval = 1    # second
        elapsed = 0
        while elapsed < max_wait_time:
            try:
                observation = self.api_client.wait_for_turn(self.game_id, self.game_key)
                self.observations = observation['observation']
                self.rewards = observation['reward']
                self.done = observation['done']
                self.info = observation['info']
                self.current_turn = 0
                return self.observations
            except Exception as e:
                print(f"Waiting for game to start... {elapsed}/{max_wait_time} seconds elapsed.")
                time.sleep(wait_interval)
                elapsed += wait_interval
        # After waiting, assume the game has been matched with a default agent
        # Optionally, you can check the server's response to confirm
        try:
            observation = self.api_client.wait_for_turn(self.game_id, self.game_key)
            self.observations = observation['observation']
            self.rewards = observation['reward']
            self.done = observation['done']
            self.info = observation['info']
            self.current_turn = 0
            return self.observations
        except Exception as e:
            raise Exception(f"Failed to start the game: {e}")

    def wait_for_turn_and_get_observation(self) -> Optional[Observations]:
        if self.done:
            return None
        observation = self.api_client.wait_for_turn(self.game_id, self.game_key)
        self.observations = observation['observation']
        self.rewards = observation['reward']
        self.done = observation['done']
        self.info = observation['info']
        self.current_turn += 1
        return self.observations

    def submit_action(self, action: str):
        if self.done:
            raise Exception("Game is already completed.")
        response = self.api_client.submit_action(self.game_id, self.game_key, action)
        # Update done and info based on response if necessary
        # For simplicity, assume the server handles state updates
        # and 'done' flag
        # Here, we might need to fetch the latest game state
        # For simplicity, skip this step
        pass

    def step(self, player_id: int, action: str) -> tuple[
        Observations,
        Rewards,
        bool,
        bool,
        Info,
    ]:
        """
        Not implemented for OnlineEnv.
        Use wait_for_turn_and_get_observation and submit_action instead.
        """
        raise NotImplementedError("Use wait_for_turn_and_get_observation and submit_action instead.")

    def render(self):
        # Optional: Implement rendering if needed
        pass
