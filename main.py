import pygame
from game_context import GameContext
from state_manager import StateManager
from states.title_state import TitleState
from states.game_state import GameState
from states.networking_state import NetworkingState
from states.wipe_state import WipeState


pygame.init()
context = GameContext()
state_manager = StateManager()
state_manager.add_state("title", TitleState(state_manager, context))
state_manager.add_state("game", GameState(state_manager, context))
state_manager.add_state("networking", NetworkingState(state_manager, context))
state_manager.add_state("wipe", WipeState(state_manager, context))
state_manager.set("title")

while state_manager.running:
    context.dt = context.clock.tick(120) / 1000 #fps

    for event in pygame.event.get():
        state_manager.handle_event(event)

    state_manager.update()
    state_manager.draw()

    pygame.display.update()

pygame.quit()