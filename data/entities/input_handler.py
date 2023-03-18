import random

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
                    return self.bindings[event.key]
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                return action.ClickAction(mouse_x, mouse_y)
        return None


class AIInputHandler(_InputHandler):
    def __init__(self):
        _InputHandler.__init__(self)

    def handle_input(self, events) -> action._Action or None:
        move = random.randint(1, 4)
        if move == 1:
            return action.MoveAction(actor.Direction.north)
        if move == 2:
            return action.MoveAction(actor.Direction.east)
        if move == 3:
            return action.MoveAction(actor.Direction.south)
        if move == 4:
            return action.MoveAction(actor.Direction.west)
        raise Exception
