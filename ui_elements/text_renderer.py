from ui_elements.ui_text import UI_Text
from colors import Colors


class TextRenderer:
    def __init__(self):
        self.ui_text = UI_Text()
        self.colors = Colors()
        

        self.start_text = self.ui_text.render_small("Press ENTER to Start")
        self.multiplayer_text = self.ui_text.render_small("Press SHIFT for Multiplayer")
        self.multiplayer_menu_text = self.ui_text.render_small("Start a room here", self.colors.WHITE)
        self.sort_rank_text = self.ui_text.render_small("Rank", self.colors.BLACK)
        self.sort_suit_text = self.ui_text.render_small("Suit", self.colors.BLACK)
        self.player_knock_text = self.ui_text.render_small("Knock", self.colors.BLACK)
        self.opp_knock_text = self.ui_text.render_small("Knock", self.colors.BLACK)

        #title text
        self.title_text = self.ui_text.render_title("Gin Rummy", self.colors.TAN)

        #menu text
        self.r_option_text = self.ui_text.render_medium("Retry", self.colors.WHITE)
        self.mm_option_text = self.ui_text.render_medium("Main Menu", self.colors.WHITE)
        self.c_option_text = self.ui_text.render_medium("Customize", self.colors.WHITE)
        self.s_option_text = self.ui_text.render_medium("Settings", self.colors.WHITE)
        self.qg_option_text = self.ui_text.render_medium("Quit Game", self.colors.WHITE)

        #round end text
        self.continue_text = self.ui_text.render_small("Press Enter to continue", self.colors.WHITE)
        self.player_score_text = None
        self.opp_score_text = None

    def update_title(self, frame, anim_frames):
        self.ui_text.update_title_size(frame, anim_frames)
        self.title_text = self.ui_text.render_title("Gin Rummy", self.colors.TAN)
        self.ui_text.update_title_alpha(self.title_text, frame, anim_frames)

    def update_score_text(self, hand_score, opp_score):
        self.player_score_text = self.ui_text.render_small(f"Player: {hand_score}", self.colors.WHITE)
        self.opp_score_text = self.ui_text.render_small(f"Opponent: {opp_score}", self.colors.WHITE)





