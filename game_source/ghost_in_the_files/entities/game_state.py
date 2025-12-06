class GameState:
    flags = {}
    logs = []

    def set_flag(name, value = True):
        GameState.flags[name] = value
    
    def get_flag(name):
        return GameState.flags.get(name, False)
    
    def add_log(text):
        GameState.logs.append(text)
    
    def get_logs():
        return GameState.logs.copy()
