import pygame

from data.engine import gfxengine
from data.engine.gfxengine import TextureIndices
from data.entities.action import _Action
from data.entities.actor import _Actor


# This will be what used to write the validating functaions for the diffrent result types
# class validator:
#     def __init__(self, arg):
#         pass
#
#     def location_validator():
#         pass
#
#
# # The result types are what allow the cards to do actions
# class Result:
#     def __init__(self, move_loc=None, damage_loc=None, stage_mod_loc=None, summon_loc=None, debuff_loc=None,
#                  buff_loc=None):
#         pass
#
#     def movement(self, valid_movement):
#         # store valid move, damage, summon, stage_mod and rules for use
#         # check validity of result through custom fuctions and rules of use
#         # follow through
#         pass
#
#     def damage(self, valid_damage):
#         pass
#
#     def stage_mod(self, valid_stage_mod):
#         pass
#
#     def summon(self, valid_summon):
#         pass
#
#     def debuff(self, valid_debuff):
#         pass
#
#     def buff(self, valid_buff):
#         pass
#
#
# # card class that will list the cards types, text description of what the card will do, and the cards "result" or calculated action
# class _card:
#     def __init__(self, card_type: str, description: str, result: Result):
#         pass

class Indicator:
    def __init__(self, x, y, indicator_type, action):
        self.x = x
        self.y = y
        self.indicator_type = indicator_type
        self.action = action

    def activate(self):
        self.action()


class Position:
    def __init__(self, move_position, check_position):
        self.move_position = move_position
        self.check_position = check_position

class _Card:
    def __init__(self, name):
        self.name = name
        self.owner = None
        # all cards that inherit this one must have a texture id: ABSTRACT PROPERTY - self.texture_id
        # all cards must be clicked to activate, and can only be on screen if they are in a hand,
        # which means they will always have a self.owner = owner: _Actor instance variable
        pass

    def set_owner(self, new_owner):
        self.owner = new_owner

    def _move(self, actor: _Actor, x, y):
        # move actor where you want it
        pass

    def _validate(self, position: Position):
        try:
            x, y = position.move_position
            check_x = x + self.owner.x
            check_y = y + self.owner.y
            if self.owner.check_valid_move(check_x, check_y):
                def check_or_position():
                    for or_set in position.check_position:
                        def check_and_set():
                            for nx, ny in or_set:
                                if not self.owner.check_valid_move(nx + self.owner.x, ny + self.owner.y):
                                    return False
                            return True
                        if check_and_set():
                            return check_x, check_y
                        return None

                return check_or_position()
        except Exception:
            # nothing bad actually happened we just checked outside the map bounds
            pass

    def activate(self, indicator_list):
        # this method must be overidden by subclasses
        # the logic in this class is the meat of the card, it calls protected functions from the parent class
        pass

    def check_click(self, x, y):
        pass

class RookCard(_Card):
    def __init__(self):
        _Card.__init__(self, "rook")
        self.texture_id = TextureIndices.rook_card

    def activate(self, indicator_list):
        def move(new_x, new_y): return lambda: (self.owner.move(new_x, new_y))
        moves = []
        moves.append(Position((0, 2), ([(0, 1)], [(0, 2)])))
        if self.owner is not None:
            for _move in moves:
                valid_move = self._validate(_move)
                if valid_move is not None:
                    x, y = valid_move
                    indicator_list.append(
                        Indicator(x, y, TextureIndices.move_indicator, move(x, y)))



# class LightningCard(_Card):
#     def __init__(self):
#         _Card.__init__(self)
#
#     def activate(self):
#         lightning_strike = lambda x, y: strike_lightning(x, y) #do something else fancy
#
#         for loop checking and placing indicators blah blah
#         x, y = 1, 1
#         self._place_indicator(x, y, lightning_strike(x, y))
