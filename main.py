import pygame
from game_context import GameContext
from state_manager import StateManager
from states.title_state.title_state import TitleState
from states.game_state.game_state import GameState
from states.networking_state.networking_state import NetworkingState
from states.wipe_state import WipeState


pygame.init()
pygame.mouse.set_visible(False)
context = GameContext()
state_manager = StateManager()
state_manager.add_state("title", TitleState(state_manager, context))
state_manager.add_state("game", GameState(state_manager, context))
state_manager.add_state("networking", NetworkingState(state_manager, context))
state_manager.add_state("wipe", WipeState(state_manager, context))
state_manager.set("title")

while state_manager.running:
    context.dt = context.clock.tick(200) / 1000 #fps

    for event in pygame.event.get():
        state_manager.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            context.screen.toggle_fullscreen()
            if context.screen.ui_scale == 1:
                context.screen.ui_scale = 2
            else:
                context.screen.ui_scale = 1
            context.image_loader.reload_sources()

    state_manager.update()
    state_manager.draw()

    pygame.display.update()

pygame.quit()