import functools

from data.engine.gfxengine import TextureIndices
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

    def _move(self, actor: _Actor, x, y):
        # move actor where you want it
        pass

    #the move and damage checks are separated if cards have different spaces for movement and attacks

    # Check that the space is free of walls and actors for movement
    def validate_move(self, position: Position):
        try:
            x, y = position.move_position
            check_x = x + self.owner.x
            check_y = y + self.owner.y
            #gets the list of valid move positions from the cards class to know where to check
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

    # Checks that space is free of walls and actors for attacks
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

    # get the direction of an attack (cardinal)
    def get_direction(self, x, y):
        self_x, self_y = self.owner.x, self.owner.y
        x = self_x - x
        y = self_y - y
        if x == 0 and y == 1:
            return 'North'
        elif x == 0 and y == -1:
            return 'South'
        elif x == -1 and y == 0:
            return 'East'
        elif x == 1 and y == 0:
            return 'West'
        else:
            raise Exception

    # move an attack by 1 (cardinal)
    def direction_move(self, x, y, direction):
        if direction == 'North':
            return x, (y - 1)
        elif direction == 'South':
            return x, (y + 1)
        elif direction == 'East':
            return (x + 1), y
        elif direction == 'West':
            return (x - 1), y
        else:
            raise Exception

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
        def move(new_x, new_y):
            return lambda: (self.owner.move(new_x, new_y))

        # python doesnt like only having 1 position check and simplifies it thus messes with the data structure
        moves = []
        # south
        moves.append(Position((0, 1), ([(0, 1)], [(0, 1)])))
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
        _Card.__init__(self, "bishop", 1)
        self.texture_id = TextureIndices.bishop_card

    def activate(self, indicator_list):
        def move(new_x, new_y):
            return lambda: (self.owner.move(new_x, new_y))

        # python doesnt like only having 1 position check and simplifies it thus messes with the data structure
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
        _Card.__init__(self, "knight", 1)
        self.texture_id = TextureIndices.knight_card

    def activate(self, indicator_list):
        def move(new_x, new_y):
            return lambda: (self.owner.move(new_x, new_y))

        # python doesnt like only having 1 position check and simplifies it thus messes with the data structure
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
        _Card.__init__(self, "lightning_bolt", 1)
        self.texture_id = TextureIndices.lightning_bolt
        self.damage = Damage('Lightning', 999)

    def activate(self, indicator_list):
        def try_to_do_damage(x, y):
            try:
                for actor in self.owner.level.actors:
                    if actor.x == x and actor.y == y:
                        actor.take_damage(self.damage)
                        # add logic to try to damage the spots around this one
            except:
                pass

        def attack(x, y):
            return lambda: try_to_do_damage(x, y)

        # python doesnt like only having 1 position check and simplifies it thus messes with the data structure
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
        _Card.__init__(self, "fire_ball", 1)
        self.texture_id = TextureIndices.fire_ball
        self.damage = Damage('Fire', 999)

    def activate(self, indicator_list):

        def try_to_do_damage(x, y):
            direction = self.get_direction(x, y)
            end = False
            while not end:
                if self.owner.check_valid_attack(x, y):
                    for actor in self.owner.level.actors:
                        if actor.x == x and actor.y == y:
                            actor.take_damage(self.damage)
                            end = True
                    x, y = self.direction_move(x, y, direction)
                else:
                    end = True

        def attack(x, y):
            return lambda: try_to_do_damage(x, y)

        # python doesnt like only having 1 position check and simplifies it thus messes with the data structure
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
