

class Card:
    def __init__(self, name, loc=None) -> None:
        if loc is None:
            loc = (0, 0)
        self.name = name
        self.loc = loc
        self.dragging = False

        self.base_y = loc[1]
        self.target_y = loc[1]
        self.hovered_y = False
        self.vertical_offset = 20
        self.velocity_y = 0
        
        self.base_x = loc[0]
        self.target_x = loc[0]
        self.hovered_x = False
        self.velocity_x = 0

        self.visible = True


