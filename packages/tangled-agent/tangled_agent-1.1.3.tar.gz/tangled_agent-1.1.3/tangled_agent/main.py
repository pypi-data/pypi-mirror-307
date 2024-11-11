"""
Main entry point for the Tangled agent game playing tools.
"""

from __future__ import annotations

import importlib
import os
import sys
import configargparse
from tangled_game_engine import GameAgentBase, Game
from .basic_game import play_local_game, play_remote_game

import logging
from .pretty_game import GameDisplay
from .graph_display import GraphGameGUI
from functools import partial

def import_agent(agent_name: str) -> GameAgentBase:
    """
    Dynamically import a class from a string specification in the format 'module_name.ClassName'.
    
    Args:
        agent_name (str): The module and class name as a single string.
    
    Returns:
        type: The class type that was dynamically imported.
    """
    try:
        # Split the input into module and class
        module_name, class_name = agent_name.rsplit('.', 1)
        logging.debug(f"Importing module {module_name} and class {class_name}")
        
        # Import the module
        module = importlib.import_module(module_name)

        # Get the class from the module
        clazz = getattr(module, class_name)
        if not issubclass(clazz, GameAgentBase):
            raise ValueError(f"Class '{class_name}' is not a subclass of GameAgentBase.")
        
        return clazz
    except (ImportError, AttributeError, ValueError) as e:
        raise ImportError(f"Could not import class {agent_name}. Ensure it exists and is correctly specified (e.g. module_name.ClassName).") from e
    

def generate_sample_agent(agent_name: str) -> str:
    """
    Generate a sample agent class with the given name.
    """
    from importlib import resources
    import tangled_agent
        
    # Validate that the agent name is a valid Python identifier in CamelCase
    if not agent_name.isidentifier() or not agent_name[0].isupper():
        raise ValueError("Agent name must be a valid Python identifier in CamelCase (e.g. MyAgent).")
    
    # Convert camel case agent_name to snake case for file
    file_name = agent_name[0].lower() + ''.join([f"_{c.lower()}" if c.isupper() else c for c in agent_name[1:]]) + ".py"

    # Check if local file_name already exists and ask to overwrite before doing so.
    if os.path.exists(file_name):
        overwrite = input(f"File {file_name} already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Exiting without overwriting file.")
            sys.exit(0)
    
    # Read the random agent template
    with resources.open_text(tangled_agent, "random_agent.py") as f:
        sample_text = f.read()
        # Rename the RandomRandyAgent class to the given name
        sample_text = sample_text.replace("RandomRandyAgent", agent_name)
        # Write it to a file
        
        # Write the file
        with open(file_name, "w") as f:
            f.write(sample_text)        

def setup_args() -> configargparse.ArgParser:
    """
    Set up handling of command-line arguments.
    """

    description = """
Play a game of Tangled with one or two custom agents, either for local testing
 or for online play."""
    
    epilog = """
Run this program with the --help flag to see the full list of options.
"""

    usage = """
Local game: 
    python -m tangled-agent --agent your_agent.YourAgentClass
Remote game: 
    python -m tangled-agent --game-id <game-id> --agent your_agent.YourAgentClass [--player-index 1] [--new-credentials]

Or you can use a configuration file (e.g. config.ini) with the following format:

```config.ini
[DEFAULT]
agent = your_agent.YourAgentClass
agent_2 = your_agent.OtherAgentClass
vertex_count = 5
game-id = <game-id>
host = <game-host>
new-credentials = False
```

or a combination of both:

    python -m tangled_agent --config config.ini --game_id <game-id> --host <game-host> --new-credentials

If a game-id is provided, the script will connect to the remote game server and join the game as either player 1 or 2 using the specified GameAgent subclass.
"""

    parser = configargparse.ArgParser(description=description,
                                        epilog=epilog,
                                        usage=usage,
                                        default_config_files=['config.ini'])

    

    parser.add('--config', is_config_file=True, help='Path to the configuration file.')
    parser.add_argument('--game-id', type=str, default=None, help='The ID of the game to connect to for a remote game.')
    parser.add_argument('--host', type=str, default='https://game-service-fastapi-blue-pond-7261.fly.dev', help='The host URL for the remote game server.')
    parser.add_argument('--new-credentials', action='store_true', help='Force new credentials.')
    parser.add_argument('--agent', type=str, default="tangled_agent.RandomRandyAgent", help='The qualified name of the game agent class (module.ClassName) to use.')
    parser.add_argument('--agent-2', type=str, default=None, help='The qualified name of the game agent class (module.ClassName) to use for player 2.')
    parser.add_argument('--agent-name', type=str, default="default", help='The name of the player agent to use for record keeping (online games).')
    parser.add_argument('--player-index', type=int, default=0, help='The index of the player to be in the game (0=no preference, 1 or 2).')
    parser.add_argument('--vertex-count', type=int, default=0, help='The number of vertices in the game (default edges are all possible combinations).')
    parser.add_argument('--game-spec', type=str, default=None, help='A JSON-formatted array of pairs (e.g. [[0,1],[0,2],...]) representing the game specification as edges. Vertex count will default to max index in the edge list+1.')
    valid_log_levels = ['PRETTY', 'GRAPH', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    parser.add_argument('--log-level', type=str, default='PRETTY', choices=valid_log_levels, help=f'The logging level to use ({", ".join(valid_log_levels)}).')
    parser.add_argument('--sample', action='store_true', help='Generate a sample agent.')
    return parser


def main():
    """
    Main entry point for the script.
    Get the command-line arguments and start the game.
    """
    global args

    if args.sample:
        print("Generating sample agent SampleAgent in file sample_agent.py")
        generate_sample_agent("SampleAgent")
        sys.exit(0)

    # Create an agent from the class from a string
    agent_class = import_agent(args.agent)

    # Create an agent from the class from a string
    agent_class2 = import_agent(args.agent_2) if args.agent_2 else None


    game_display = None
    callback = None
    if args.log_level:
        if args.log_level == 'PRETTY':
            logging.basicConfig(level=logging.INFO)
            game_display = GameDisplay()
            callback = game_display.display_status
        elif args.log_level == 'GRAPH':
            logging.basicConfig(level=logging.INFO)
            game_display = GraphGameGUI()
            callback = partial(game_display.display_status, delay=0.1)
        else:
            logging.basicConfig(level=args.log_level)
            

    if args.game_id is not None:

        # Create the agent to play the game. The player ID should match one of the players in the game.
        player = agent_class()


        logging.info(f"Game ID: {args.game_id}")
        logging.info(f"Host: {args.host}")
        logging.info(f"Force New Credentials: {args.new_credentials}")
        logging.info(f"Player Index: {args.player_index}")
        logging.info(f"Agent Name: {args.agent_name}")
        
        play_remote_game(args.game_id, 
                         args.host, 
                         player, 
                         force_new_credentials=args.new_credentials, 
                         player_index=args.player_index, 
                         agent_name=args.agent_name, 
                         update_display=callback)
    else:
        # Create two agents with names (e.g. RandomRandyAgent("player1"))
        player1 = agent_class(f'{agent_class.__name__}')
        player2 = agent_class2(f'{agent_class2.__name__}') if agent_class2 else agent_class(f'{agent_class.__name__}')

        # Make a game specification if we have a game spec
        if args.vertex_count >= 2 and args.game_spec:
            game_spec = {"vertex_count": args.vertex_count, "edges": args.game_spec}
        elif args.game_spec:
            game_spec = {"vertex_count": max([max(edge) for edge in args.game_spec])+1, "edges": args.game_spec}
        else:
            if args.vertex_count < 2:
                # Default to 4 vertices if no vertex count is specified
                logging.info("No vertex count specified. Defaulting to 4 vertex game.")
                args.vertex_count = 4
            game_spec = {"vertex_count": args.vertex_count, "edges": [[i, j] for i in range(args.vertex_count-1) for j in range(i+1, args.vertex_count)]}

        logging.info(f"Game Specification: {game_spec}")
        game = Game()
        game.create_game(game_spec["vertex_count"], game_spec["edges"])

        # Play a local game with the two agents
        play_local_game(player1, player2, game, update_display=callback)


args = setup_args().parse_args()

if __name__ == "__main__":
    main()

