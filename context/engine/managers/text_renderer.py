class TextRenderer:
    def __init__(self, context):
        self.context = context

        self.start_text = self.context.ui_text.render_small("Press ENTER to Start")
        self.multiplayer_text = self.context.ui_text.render_small("Press SHIFT for Multiplayer")
        self.multiplayer_menu_text = self.context.ui_text.render_small("Start a room here", self.context.constants.WHITE)
        self.sort_rank_text = self.context.ui_text.render_small("Rank", self.context.constants.BLACK)
        self.sort_suit_text = self.context.ui_text.render_small("Suit", self.context.constants.BLACK)
        self.player_knock_text = self.context.ui_text.render_small("Knock", self.context.constants.BLACK)
        self.discard_knock_text = self.context.ui_text.render_small("Discard one of the following cards", self.context.constants.WHITE)
        self.opp_knock_text = self.context.ui_text.render_small("Knock", self.context.constants.BLACK)
        self.title_text = self.context.ui_text.render_title("Gin Rummy", self.context.constants.TAN)

        #menu text
        self.r_option_text = self.context.ui_text.render_medium("Retry", self.context.constants.WHITE)
        self.mm_option_text = self.context.ui_text.render_medium("Main Menu", self.context.constants.WHITE)
        self.c_option_text = self.context.ui_text.render_medium("Customize", self.context.constants.WHITE)
        self.s_option_text = self.context.ui_text.render_medium("Settings", self.context.constants.WHITE)
        self.qg_option_text = self.context.ui_text.render_medium("Quit Game", self.context.constants.WHITE)

        #round end text
        self.continue_text = self.context.ui_text.render_small("Press Enter to continue", self.context.constants.WHITE)
        self.player_score_text = None
        self.opp_score_text = None

    def update_score_text(self, hand_score, opp_score):
        self.player_score_text = self.context.ui_text.render_small(f"Player: {hand_score}", self.context.constants.WHITE)
        self.opp_score_text = self.context.ui_text.render_small(f"Opponent: {opp_score}", self.context.constants.WHITE)





