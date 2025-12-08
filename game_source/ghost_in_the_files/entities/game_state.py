import pygame

class GameState:
    flags = {}
    logs = []
    convertor_state = {
        "selected_file": None,
        "mode": "Base64"
    }
    
    locked_program_state = {
        "input": ["-", "-", "-", "-"],
        "guessed": False
    }
    
    ram_puzzle_state = {
        "grid": [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ],
        "game_started": False,
        "memory_chip_inserted": False,
        "win": False,
        "big_block_appeared": False,
        "reward_given": False
    }
    
    cpu_puzzle_state = {
        "cpu_cores": [0, 0, 0, 0],
        "item_used": False,
        "win": False,
        "reward_given": False
    }
    
    network_puzzle_state = {
        "nodes": {},
        "edges": {},
        "item_used": False,
        "win": False,
        "reward_given": False
    }
    
    game_time_minutes = 6 * 60
    time_update = pygame.time.get_ticks()

    def set_flag(name, value = True):
        GameState.flags[name] = value
    
    def get_flag(name):
        return GameState.flags.get(name, False)
    
    def add_log(text):
        GameState.logs.append(text)
    
    def get_logs():
        return GameState.logs.copy()
    
    def reset():
        GameState.flags = {}
        GameState.logs = []
        GameState.convertor_state = {
            "selected_file": None,
            "mode": "Base64"
        }
        GameState.locked_program_state = {
            "input": ["-", "-", "-", "-"],
            "guessed": False
        }
        GameState.ram_puzzle_state = {
            "grid": [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]
            ],
            "game_started": False,
            "memory_chip_inserted": False,
            "win": False,
            "big_block_appeared": False,
            "reward_given": False
        }
        GameState.cpu_puzzle_state = {
            "cpu_cores": [0, 0, 0, 0],
            "item_used": False,
            "win": False,
            "reward_given": False
        }
        GameState.network_puzzle_state = {
            "nodes": {},
            "edges": {},
            "item_used": False,
            "win": False,
            "reward_given": False
        }
        GameState.game_time_minutes = 6 * 60
        GameState.time_update = pygame.time.get_ticks()
