class Card:
    def __init__(self, name, loc) -> None:
        self.name = name
        self.loc = loc
        self.hover_offset = 10
        self.is_hovered = False
