from states.title_state import TitleState
from states.networking_state import NetworkingState
from states.game_state import GameState

class StateManager:
    def __init__(self):
        self.active_state = None
        self.states = {}
        self.running = True
        self.menu_active = False
        self.restart_from_main_menu = False
        self.restart = False

    def add_state(self, name, state):
        self.states[name] = state

    def set(self, name):
        if self.active_state:
            self.active_state.exit()
        self.active_state = self.states[name]
        self.active_state.enter()

    def handle_event(self, event):
        self.active_state.handle_event(event)

    def update(self):
        self.active_state.update()

        if self.active_state.requested_state_change:
            self.set(self.active_state.requested_state_change)

    def draw(self):
        self.active_state.draw()