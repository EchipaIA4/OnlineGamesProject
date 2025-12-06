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

    def set_flag(name, value = True):
        GameState.flags[name] = value
    
    def get_flag(name):
        return GameState.flags.get(name, False)
    
    def add_log(text):
        GameState.logs.append(text)
    
    def get_logs():
        return GameState.logs.copy()
