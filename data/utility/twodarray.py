from data.utility.movement import Coordinate


class TwoDArray:
    def __init__(self, height: int, width: int, starting_value):
        self._array = [[starting_value for _ in range(width)] for _ in range(height)]
        self._height = height
        self._width = width

    def __setitem__(self, coordinate, value):
        self._array[coordinate.y][coordinate.x] = value

    def __getitem__(self, coordinate):
        return self._array[coordinate.y][coordinate.x]

    def __iter__(self):
        self._current_x = -1
        self._current_y = 0
        return self

    def __next__(self):
        if self._current_x == self._width - 1 and self._current_y == self._height - 1:
            raise StopIteration
        elif self._current_x == self._width - 1:
            self._current_x = 0
            self._current_y += 1
        else:
            self._current_x += 1
        return Coordinate(self._current_x, self._current_y), self._array[self._current_y][self._current_x]

    def reset(self, default):
        for coordinate, _ in self:
            self[coordinate] = default
