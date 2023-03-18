from data.entities.actor import _Actor
from data.entities.actor import Direction


class _Action:
    def __init__(self):
        pass

    def execute(self, actor: _Actor):
        pass


class MoveAction(_Action):
    def __init__(self, direction: Direction):
        _Action.__init__(self)
        self.direction = direction

    def execute(self, actor: _Actor):
        actor.move_cardinal(self.direction)
        if actor.hand is not None:
            actor.hand.deselect_card()


class ClickAction(_Action):
    def __init__(self, x, y):
        _Action.__init__(self)
        self.x = x
        self.y = y

    def execute(self, actor: _Actor):
        actor.hand.click(self.x, self.y)
