# textarena/player_online/matchmaking.py

from typing import Optional
from threading import Thread
import time

class MatchmakingQueue:
    def __init__(self):
        self.queue = []
        self.matches = {}
    
    def add_to_queue(self, model_id: str):
        self.queue.append(model_id)
        # Start matchmaking in a separate thread
        matchmaking_thread = Thread(target=self.match_agents)
        matchmaking_thread.start()
    
    def match_agents(self):
        while len(self.queue) >= 2:
            player1 = self.queue.pop(0)
            player2 = self.queue.pop(0)
            # Create a match between player1 and player2
            game_id = self.create_game(player1, player2)
            self.matches[game_id] = (player1, player2)
        time.sleep(1)  # Sleep before checking the queue again
    
    def create_game(self, player1_id: str, player2_id: str) -> str:
        # Implement game creation logic
        # Return a unique game_id
        pass
