class State:
    def __init__(self, manager): 
        self.manager = manager
        
    def handle_event(self, event): pass
    def update(self): pass
    def draw(self): pass
    def enter(self): pass
    def exit(self): pass