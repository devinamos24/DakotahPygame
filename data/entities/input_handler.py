import pygame
import data.entities.action as action
import data.entities.actor as actor


class _InputHandler:
    def __init__(self):
        self.bindings = {}

    def handle_input(self, events) -> action._Action or None:
        pass

    def bind_command(self, key, action: action._Action):
        self.bindings[key] = action


class PlayerInputHandler(_InputHandler):
    def __init__(self):
        _InputHandler.__init__(self)
        self.bind_command(pygame.K_UP, action.MoveAction(actor.Direction.north))
        self.bind_command(pygame.K_RIGHT, action.MoveAction(actor.Direction.east))
        self.bind_command(pygame.K_DOWN, action.MoveAction(actor.Direction.south))
        self.bind_command(pygame.K_LEFT, action.MoveAction(actor.Direction.west))

    def handle_input(self, events) -> action._Action or None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in list(self.bindings.keys()):
                    print(event)
                    return self.bindings[event.key]
        return None
