from abc import ABC, abstractmethod

from data.entities.actor import _Actor
from data.entities.actor import Direction


class Action(ABC):

    def __init__(self):
        self._actor = None
        self._level = None
        self._game_result = None

    def get_actor(self) -> _Actor:
        return self._actor

    def get_level(self) -> Level:
        return self._level

    def bind(self, actor: _Actor) -> None:
        assert actor is not None
        self._actor = actor
        self._level = actor.level

    @abstractmethod
    def on_execute(self):
        pass

    def execute(self, gameResult: GameResult) -> ActionResult:
        assert self._actor is not None  # Action should be bound to actor already

        self._game_result = gameResult
        return self.on_execute()

    def add_event(self, event) -> None:
        self._game_result.events.add(event)

    def alternate(self, action) -> ActionResult:
        action.bind(self._actor)
        return ActionResult.alternate(action)


class ActionResult:
    def __init__(self, succeeded):
        self.succeeded = succeeded
        self.alternative = None

    SUCCESS = __init__(True)
    FAILURE = __init__(False)

    @classmethod
    def alternate(cls, alternative: Action):
        alternate_result = cls(False)
        alternate_result.alternative = alternative
        return alternate_result


class MoveAction(Action):
    def __init__(self, direction: Direction):
        Action.__init__(self)
        self.direction = direction

    def on_execute(self) -> ActionResult:
        coordinate = self._actor.coordinate + self.direction.value

        target = self._level.actor_at(coordinate)
        if target is not None and target is not self._actor:
            return self.alternate(AttackAction(target))

        tile = self._level.Stage_layer[coordinate]
        if tile == TextureIndices.wall:
            self.add_event(Event("bonk", coordinate))
            return ActionResult.FAILURE

        self._actor.coordinate = coordinate
        return ActionResult.SUCCESS


class AttackAction(Action):

    def __init__(self, defender: _Actor):
        Action.__init__(self)
        self.defender = defender

    def on_execute(self):
        self.add_event(Event("hit", self.defender.coordinate))
        return ActionResult.SUCCESS

# class MoveAction(Action):
#     def __init__(self, direction: Direction):
#         self.direction = direction
#
#     def execute(self, actor: _Actor):
#         if actor.energy.current_energy > 0 and actor.move_cardinal(self.direction):
#             actor.energy.remove_energy(1)
#         if actor.hand is not None:
#             actor.hand.deselect_card()
#
#
# class ClickAction(Action):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def execute(self, actor: _Actor):
#         actor.hand.click(self.x, self.y)
