from .random_agent import RandomRandyAgent
from .remote_game_player import RemoteGamePlayer

from tangled_game_engine import GamePlayerBase, LocalGamePlayer, GameAgentBase, Game

def play_local_game(player1: GameAgentBase, player2: GameAgentBase, game: Game, update_display: callable = None):
    """
    Sets up and starts a local game with two random agents.

    Args:
        player1 (GameAgentBase): The first player agent.
        player2 (GameAgentBase): The second player agent.
        game (Game): The game instance to play.
    """

    # Start the game using the helper function for local games (LocalGamePlayer)
    # This will repeatedly call the agents' make_move methods until the game is over

    GamePlayerBase.start_game(LocalGamePlayer, player1, player2, game, update_display=update_display)

def play_remote_game(game_id: str, host: str, player: GameAgentBase, update_display: callable = None, force_new_credentials: bool = False, **kwargs): 
    """
    Sets up and starts a remote game with a random agent.

    Args:
        game_id (str): The ID of the game to connect to (provided by create_game on the website).
        host (str): The host URL for the remote game server (provided by create_game on the website).
        player (GameAgentBase): The player agent to use.
    """

    # Start the game using the helper function for remote games (RemoteGamePlayer)
    # This will connect to the server and join the game, generate your credentials (if needed),
    # then start the game loop.
    # This will repeatedly call the agent's make_move methods and pass it back to the
    # server until the game is over
    GamePlayerBase.start_game(RemoteGamePlayer, player, game_id, host, update_display=update_display, force_new_credentials=force_new_credentials, **kwargs)

