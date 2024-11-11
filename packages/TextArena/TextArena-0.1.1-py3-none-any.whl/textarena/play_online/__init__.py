from .api_client import APIClient
from .online_env import OnlineEnv

from typing import Optional


def make_online(
    env_id: str,
    model_key: str,
    base_url: str = "http://127.0.0.1:8000/api",
    game_name: Optional[str] = None
) -> OnlineEnv:
    """
    Create an online environment instance for playing games online.
    
    Args:
        env_id (str): The ID of the environment to create.
        model_key (str): The unique key of the registered model.
        base_url (str): The base URL of the API server.
        game_name (Optional[str]): Optional name for the game.
        
    Returns:
        OnlineEnv: An instance of the online environment.
    """
    api_client = APIClient(model_key=model_key, base_url=base_url)
    return OnlineEnv(env_id=env_id, api_client=api_client, game_name=game_name)
