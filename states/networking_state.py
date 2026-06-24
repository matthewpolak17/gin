from states.state import State

class NetworkingState(State):
    def __init__(self, manager, context):
        super().__init__(manager)
        self.context = context

    def update(self):
        pass
    def draw(self):
        pass
    def exit(self):
        pass
    def enter(self):
        pass
    def handle_event(self):
        pass