from context.engine import constants
from context.engine.ui_text import UI_Text

class TextRenderer:
    def __init__(self, context):
        self.ui_text = UI_Text()
        self.context = context

        self.start_text = self.ui_text.render_small("Press ENTER to Start")
        self.multiplayer_text = self.ui_text.render_small("Press SHIFT for Multiplayer")
        self.multiplayer_menu_text = self.ui_text.render_small("Start a room here", constants.WHITE)
        self.sort_rank_text = self.ui_text.render_small("Rank", constants.BLACK)
        self.sort_suit_text = self.ui_text.render_small("Suit", constants.BLACK)
        self.player_knock_text = self.ui_text.render_small("Knock", constants.BLACK)
        self.opp_knock_text = self.ui_text.render_small("Knock", constants.BLACK)
        #title text
        self.title_text = self.ui_text.render_title("Gin Rummy", constants.TAN)

        #menu text
        self.r_option_text = self.ui_text.render_medium("Retry", constants.WHITE)
        self.mm_option_text = self.ui_text.render_medium("Main Menu", constants.WHITE)
        self.c_option_text = self.ui_text.render_medium("Customize", constants.WHITE)
        self.s_option_text = self.ui_text.render_medium("Settings", constants.WHITE)
        self.qg_option_text = self.ui_text.render_medium("Quit Game", constants.WHITE)

        #round end text
        self.continue_text = self.ui_text.render_small("Press Enter to continue", constants.WHITE)
        self.player_score_text = None
        self.opp_score_text = None

    def update_title(self, frame, anim_frames):
        self.ui_text.update_title_size(frame, anim_frames)
        self.title_text = self.ui_text.render_title("Gin Rummy", constants.TAN)
        self.ui_text.update_title_alpha(self.title_text, frame, anim_frames)

    def update_score_text(self, hand_score, opp_score):
        self.player_score_text = self.ui_text.render_small(f"Player: {hand_score}", constants.WHITE)
        self.opp_score_text = self.ui_text.render_small(f"Opponent: {opp_score}", constants.WHITE)





