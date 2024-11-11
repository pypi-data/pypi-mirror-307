import requests
from typing import Any, Dict, Optional
import time
import json

class APIClient:
    def __init__(self, model_key: str, base_url: str = "http://127.0.0.1:8000/api"):
        self.model_key = model_key
        self.base_url = base_url.rstrip('/')
        self.session_token = None
        self.session_expires_at = 0
        self.authenticate()
        
    def authenticate(self):
        url = f"{self.base_url}/models/authenticate"
        headers = {
            "Authorization": f"ModelKey {self.model_key}"
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.session_token = data['session_token']
            self.session_expires_at = time.time() + data['expires_in']
        else:
            raise Exception(f"Authentication failed: {response.status_code} {response.text}")
    
    def ensure_authenticated(self):
        if self.session_token is None or time.time() >= self.session_expires_at:
            self.authenticate()
    
    def create_game(self, env_id: str, game_name: Optional[str] = None) -> Dict[str, Any]:
        self.ensure_authenticated()
        url = f"{self.base_url}/games"
        headers = {
            "Authorization": f"Bearer {self.session_token}"
        }
        data = {
            "environment_id": env_id,
            "game_name": game_name
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Game creation failed: {response.status_code} {response.text}")
    
    def join_game(self, game_id: str):
        self.ensure_authenticated()
        url = f"{self.base_url}/games/{game_id}/join"
        headers = {
            "Authorization": f"Bearer {self.session_token}"
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Joining game failed: {response.status_code} {response.text}")
    
    def wait_for_turn(self, game_id: str, game_key: str) -> Dict[str, Any]:
        url = f"{self.base_url}/games/{game_id}/wait_for_turn"
        headers = {
            "Authorization": f"GameKey {game_key}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error getting observation: {response.status_code} {response.text}")
    
    def submit_action(self, game_id: str, game_key: str, action: str):
        url = f"{self.base_url}/games/{game_id}/action"
        headers = {
            "Authorization": f"GameKey {game_key}"
        }
        data = {
            "action": action
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error submitting action: {response.status_code} {response.text}")
