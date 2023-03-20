import functools

from data.engine.gfxengine import TextureIndices
from data.entities.actor import _Actor, Coordinate
from data.utility import movement


class Indicator:
    def __init__(self, coordinate, indicator_type, action):
        self.coordinate = coordinate
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
    def __init__(self, name, energy_cost):
        self.name = name
        self.energy_cost = energy_cost
        self.owner = None
        # all cards that inherit this one must have a texture id: ABSTRACT PROPERTY - self.texture_id
        # all cards must be clicked to activate, and can only be on screen if they are in a hand,
        # which means they will always have a self.owner = owner: _Actor instance variable
        pass

    def set_owner(self, new_owner):
        self.owner = new_owner

    # Create an anonymous function that moves the owner of the card
    def _move(self, coordinate):
        return lambda: (self.owner.move(coordinate))

    # Check that the space is free of walls and actors
    def validate_move(self, position: Position):
        try:
            coordinate = Coordinate(position.move_position[0], position.move_position[1]) + self.owner.coordinate
            if not bool(self.owner.check_valid_move(coordinate)):
                def check_or_position():
                    for or_set in position.check_position:
                        def check_and_set():
                            and_test = 0
                            for nx, ny in or_set:
                                if bool(self.owner.check_valid_move(self.owner.coordinate + Coordinate(nx, ny))):
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
                        return coordinate
                    return None

                return check_or_position()
        except Exception:
            # nothing bad actually happened we just checked outside the map bounds
            pass

    # Checks that space is free of walls
    def validate_attack(self, position: Position):
        try:
            coordinate = Coordinate(position.move_position[0], position.move_position[1]) + self.owner.coordinate
            if self.owner.check_valid_attack(coordinate):
                def check_or_position():
                    for or_set in position.check_position:
                        def check_and_set():
                            and_test = 0
                            for nx, ny in or_set:
                                if not self.owner.check_valid_attack(self.owner.coordinate + Coordinate(nx, ny)):
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
                        return coordinate
                    return None

                return check_or_position()
        except Exception:
            # nothing bad actually happened we just checked outside the map bounds
            pass

    # get the direction of an attack (cardinal)
    def get_direction(self, coordinate):
        return coordinate - self.owner.coordinate
        # if coordinate == movement.Direction.N.value:
        #     return movement.Direction.N
        # elif coordinate == movement.Direction.S.value:
        #     return movement.Direction.S
        # elif coordinate == movement.Direction.E.value:
        #     return movement.Direction.E
        # elif coordinate == movement.Direction.W.value:
        #     return movement.Direction.W
        # else:
        #     raise Exception

    # move an attack by 1 (cardinal)

    def activate(self, indicator_list):
        # this method must be overidden by subclasses
        # the logic in this class is the meat of the card, it calls protected functions from the parent class
        pass

    def check_click(self, x, y):
        pass


class RookCard(_Card):
    def __init__(self):
        _Card.__init__(self, "rook", 1)
        self.texture_id = TextureIndices.rook_card

    def activate(self, indicator_list):

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
            for move in moves:
                valid_move = self.validate_move(move)
                if valid_move is not None:
                    indicator_list.append(
                        Indicator(valid_move, TextureIndices.move_indicator, self._move(valid_move)))


class BishopCard(_Card):
    def __init__(self):
        _Card.__init__(self, "bishop", 1)
        self.texture_id = TextureIndices.bishop_card

    def activate(self, indicator_list):
        def move(coordinate):
            return lambda: (self.owner.move(coordinate))

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
                    indicator_list.append(
                        Indicator(valid_move, TextureIndices.move_indicator, self._move(valid_move)))


class KnightCard(_Card):
    def __init__(self):
        _Card.__init__(self, "knight", 1)
        self.texture_id = TextureIndices.knight_card

    def activate(self, indicator_list):
        def move(new_x, new_y):
            return lambda: (self.owner.move(Coordinate(new_x, new_y)))

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
                    indicator_list.append(
                        Indicator(valid_move, TextureIndices.move_indicator, self._move(valid_move)))


class LightningBoltCard(_Card):
    def __init__(self):
        _Card.__init__(self, "lightning_bolt", 1)
        self.texture_id = TextureIndices.lightning_bolt
        self.damage = Damage('Lightning', 999)

    def activate(self, indicator_list):
        def try_to_do_damage(coordinate):
            for actor in self.owner.level.actors:
                if actor.coordinate == coordinate:
                    actor.take_damage(self.damage)
                    # add logic to try to damage the spots around this one

        def attack(coordinate):
            return lambda: try_to_do_damage(coordinate)

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
                    indicator_list.append(
                        Indicator(valid_position, TextureIndices.move_indicator, attack(valid_position)))


class FireBallCard(_Card):
    def __init__(self):
        _Card.__init__(self, "fire_ball", 1)
        self.texture_id = TextureIndices.fire_ball
        self.damage = Damage('Fire', 999)

    def activate(self, indicator_list):

        def try_to_do_damage(coordinate):
            direction = self.get_direction(coordinate)
            end = False
            while not end:
                if self.owner.check_valid_attack(coordinate):
                    for actor in self.owner.level.actors:
                        if actor.coordinate == coordinate:
                            actor.take_damage(self.damage)
                            end = True
                    coordinate += direction
                else:
                    end = True

        def attack(coordinate):
            return lambda: try_to_do_damage(coordinate)

        attack_position = []
        attack_position.append(Position((1, 0), ([(1, 0)], [(1, 0)])))
        attack_position.append(Position((-1, 0), ([(-1, 0)], [(-1, 0)])))
        attack_position.append(Position((0, 1), ([(0, 1)], [(0, 1)])))
        attack_position.append(Position((0, -1), ([(0, -1)], [(0, -1)])))
        if self.owner is not None:
            for positions in attack_position:
                valid_position = self.validate_attack(positions)
                if valid_position is not None:
                    indicator_list.append(
                        Indicator(valid_position, TextureIndices.move_indicator, attack(valid_position)))
