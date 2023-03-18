import pygame

from data.engine import gfxengine
from data.engine.gfxengine import TextureIndices
from data.entities.action import _Action
from data.entities.actor import _Actor


class Indicator:
    def __init__(self, x, y, indicator_type, action):
        self.x = x
        self.y = y
        self.indicator_type = indicator_type
        self.action = action

    def activate(self):
        self.action()


class Damage:
    def __init__(self, damage_type, damage_amount):
        self.damage_type = damage_type
        self.damage_amount = damage_amount


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

    # Check that the space is free of walls and actors
    def validate_move(self, position: Position):
        try:
            x, y = position.move_position
            check_x = x + self.owner.x
            check_y = y + self.owner.y
            if not bool(self.owner.check_valid_move(check_x, check_y)):
                def check_or_position():
                    for or_set in position.check_position:
                        def check_and_set():
                            and_test = 0
                            for nx, ny in or_set:
                                if bool(self.owner.check_valid_move(nx + self.owner.x, ny + self.owner.y)):
                                    and_test += 1
                            if len(or_set) == and_test:
                                return False
                            else:
                                return True

                        if check_and_set():
                            result = True
                        else:
                            break
                    else:
                        return check_x, check_y
                    return None

                return check_or_position()
        except Exception:
            # nothing bad actually happened we just checked outside the map bounds
            pass

    # Checks that space is free of walls
    def validate_attack(self, position: Position):
        try:
            x, y = position.move_position
            check_x = x + self.owner.x
            check_y = y + self.owner.y
            if self.owner.check_valid_attack(check_x, check_y):
                def check_or_position():
                    for or_set in position.check_position:
                        def check_and_set():
                            and_test = 0
                            for nx, ny in or_set:
                                if not self.owner.check_valid_attack(nx + self.owner.x, ny + self.owner.y):
                                    and_test += 1
                            if len(or_set) == and_test:
                                return False
                            else:
                                return True

                        if check_and_set():
                            result = True
                        else:
                            break
                    else:
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
        def move(new_x, new_y):
            return lambda: (self.owner.move(new_x, new_y))

        moves = []
        # south
        moves.append(Position((0, 1), ([(0, 1)], [(0,
                                                   1)])))  # python doesnt like only having 1 position check and simplifies it thus messes with the data structure
        moves.append(Position((0, 2), ([(0, 1)], [(0, 2)])))
        moves.append(Position((0, 3), ([(0, 1)], [(0, 2)], [(0, 3)])))
        # north
        moves.append(Position((0, -1), ([(0, -1)], [(0, -1)])))
        moves.append(Position((0, -2), ([(0, -1)], [(0, -2)])))
        moves.append(Position((0, -3), ([(0, -1)], [(0, -2)], [(0, -3)])))
        # east
        moves.append(Position((1, 0), ([(1, 0)], [(1, 0)])))
        moves.append(Position((2, 0), ([(1, 0)], [(2, 0)])))
        moves.append(Position((3, 0), ([(1, 0)], [(2, 0)], [(3, 0)])))
        # west
        moves.append(Position((-1, 0), ([(-1, 0)], [(-1, 0)])))
        moves.append(Position((-2, 0), ([(-1, 0)], [(-2, 0)])))
        moves.append(Position((-3, 0), ([(-1, 0)], [(-2, 0)], [(-3, 0)])))
        if self.owner is not None:
            for _move in moves:
                valid_move = self.validate_move(_move)
                if valid_move is not None:
                    x, y = valid_move
                    indicator_list.append(
                        Indicator(x, y, TextureIndices.move_indicator, move(x, y)))


class BishopCard(_Card):
    def __init__(self):
        _Card.__init__(self, "bishop")
        self.texture_id = TextureIndices.bishop_card

    def activate(self, indicator_list):
        def move(new_x, new_y):
            return lambda: (self.owner.move(new_x, new_y))

        moves = []
        # Down Right
        moves.append(Position((1, 1), ([(1, 1)], [(1, 0), [0, 1]])))
        moves.append(Position((2, 2), ([(1, 1)], [(2, 2)], [(1, 0), [0, 1]], [(2, 1), (1, 2)])))
        moves.append(
            Position((3, 3), ([(1, 1)], [(2, 2)], [(1, 0), [0, 1]], [(2, 1), (1, 2)], [(3, 3)], [(3, 2), (2, 3)])))
        # Up Right
        moves.append(Position((1, -1), ([(1, -1)], [(1, 0), [0, -1]])))
        moves.append(Position((2, -2), ([(1, -1)], [(2, -2)], [(1, 0), [0, -1]], [(2, -1), (1, -2)])))
        moves.append(Position((3, -3), (
        [(1, -1)], [(2, -2)], [(3, -3)], [(1, 0), [0, -1]], [(2, -1), (1, -2)], [(3, -3)], [(3, -2), (2, -3)])))
        # Down Left
        moves.append(Position((-1, 1), ([(-1, 1)], [(-1, 0), [0, 1]])))
        moves.append(Position((-2, 2), ([(-1, 1)], [(-2, 2)], [(-1, 0), [0, 1]], [(-2, 1), (-1, 2)])))
        moves.append(Position((-3, 3), (
        [(-1, 1)], [(-2, 2)], [(-3, 3)], [(-1, 0), [0, 1]], [(-2, 1), (-1, 2)], [(-3, 3)], [(-3, 2), (-2, 3)])))
        # Up Left
        moves.append(Position((-1, -1), ([(-1, -1)], [(-1, 0), [0, -1]])))
        moves.append(Position((-2, -2), ([(-1, -1)], [(-2, -2)], [(-1, 0), [0, -1]], [(-2, -1), (-1, -2)])))
        moves.append(Position((-3, -3), (
        [(-1, -1)], [(-2, -2)], [(-3, -3)], [(-1, 0), [0, -1]], [(-2, -1), (-1, -2)], [(-3, -3)],
        [(-3, -2), (-2, -3)])))
        if self.owner is not None:
            for _move in moves:
                valid_move = self.validate_move(_move)
                if valid_move is not None:
                    x, y = valid_move
                    indicator_list.append(
                        Indicator(x, y, TextureIndices.move_indicator, move(x, y)))


class KnightCard(_Card):
    def __init__(self):
        _Card.__init__(self, "knight")
        self.texture_id = TextureIndices.knight_card

    def activate(self, indicator_list):
        def move(new_x, new_y):
            return lambda: (self.owner.move(new_x, new_y))

        moves = []
        # Down Right
        moves.append(Position((2, 1), ([(1, 0), (0, 1)], [(1, 1), (1, 0)], [(1, 1), (2, 0)])))
        moves.append(Position((1, 2), ([(0, 1), (1, 0)], [(1, 1), (0, 1)], [(1, 1), (0, 2)])))
        # Down Left
        moves.append(Position((-2, 1), ([(-1, 0), (0, 1)], [(-1, 1), (-1, 0)], [(-1, 1), (-2, 0)])))
        moves.append(Position((-1, 2), ([(0, 1), (-1, 0)], [(-1, 1), (0, 1)], [(-1, 1), (0, 2)])))
        # Up Right
        moves.append(Position((2, -1), ([(1, 0), (0, -1)], [(1, -1), (1, 0)], [(1, -1), (2, 0)])))
        moves.append(Position((1, -2), ([(0, -1), (1, 0)], [(1, -1), (0, -1)], [(1, -1), (0, -2)])))
        # Down Right
        moves.append(Position((-2, -1), ([(-1, 0), (0, -1)], [(-1, -1), (-1, 0)], [(-1, -1), (-2, 0)])))
        moves.append(Position((-1, -2), ([(0, -1), (-1, 0)], [(-1, -1), (0, -1)], [(-1, -1), (0, -2)])))
        if self.owner is not None:
            for _move in moves:
                valid_move = self.validate_move(_move)
                if valid_move is not None:
                    x, y = valid_move
                    indicator_list.append(
                        Indicator(x, y, TextureIndices.move_indicator, move(x, y)))


class LightningBoltCard(_Card):
    def __init__(self):
        _Card.__init__(self, "lightning_bolt")
        self.texture_id = TextureIndices.lightning_bolt
        self.damage = Damage('Lightning', 999)

    def activate(self, indicator_list):
        def try_to_do_damage(x, y):
            try:
                self.owner.level.actors[y][x].take_damage(self.damage)
            except:
                pass

        def attack(x, y):
            return lambda: try_to_do_damage(x, y)

        attack_position = []
        attack_position.append(Position((1, 1), ([(1, 1)], [(1, 1)])))
        attack_position.append(Position((-1, 1), ([(-1, 1)], [(-1, 1)])))
        attack_position.append(Position((1, -1), ([(1, -1)], [(1, -1)])))
        attack_position.append(Position((-1, -1), ([(-1, -1)], [(-1, -1)])))
        attack_position.append(Position((1, 0), ([(1, 0)], [(1, 0)])))
        attack_position.append(Position((-1, 0), ([(-1, 0)], [(-1, 0)])))
        attack_position.append(Position((0, 1), ([(0, 1)], [(0, 1)])))
        attack_position.append(Position((0, -1), ([(0, -1)], [(0, -1)])))
        if self.owner is not None:
            for positions in attack_position:
                valid_position = self.validate_attack(positions)
                if valid_position is not None:
                    x, y = valid_position
                    indicator_list.append(
                        Indicator(x, y, TextureIndices.move_indicator, attack(x, y)))
                    

class FireBallCard(_Card):
    def __init__(self):
        _Card.__init__(self, "fire_ball")
        self.texture_id = TextureIndices.fire_ball
        self.damage = Damage('Fire', 999)

    def activate(self, indicator_list):
        def try_to_do_damage(x, y):
            while True:
                if self.owner.check_valid_attack(x,y):
                    try:
                        self.owner.level.actors[y][x].take_damage(self.damage)
                    except:
                        x = x + 1
                        y = y + 1
                else:
                    break

        def attack(x, y):
            return lambda: try_to_do_damage(x, y)

        attack_position = []
        attack_position.append(Position((1, 0), ([(1, 0)], [(1, 0)])))
        attack_position.append(Position((-1, 0), ([(-1, 0)], [(-1, 0)])))
        attack_position.append(Position((0, 1), ([(0, 1)], [(0, 1)])))
        attack_position.append(Position((0, -1), ([(0, -1)], [(0, -1)])))
        if self.owner is not None:
            for positions in attack_position:
                valid_position = self.validate_attack(positions)
                if valid_position is not None:
                    x, y = valid_position
                    indicator_list.append(
                        Indicator(x, y, TextureIndices.move_indicator, attack(x, y)))