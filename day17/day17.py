# This one stumped me entirely for a year. I had no idea how to approach it, had to look up a solution
# Thank you to xavdid (https://github.com/xavdid/advent-of-code/tree/main) for a great write-up on his site
# and an elegant solution

from heapq import heappop, heappush
from enum import IntEnum
from typing import NamedTuple, Literal

city = [[int(c) for c in l.strip()] for l in open('Inputs/day17.txt', 'r').readlines()]

Rotation = Literal["CCW", "CW"]

GridPoint = tuple[int, int]
Grid = dict[GridPoint, str]

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def rotate(facing: "Direction", towards: Rotation) -> "Direction":
        offset = 1 if towards == "CW" else -1
        return Direction((facing.value + offset) % 4)

    @staticmethod
    def offset(facing: "Direction") -> GridPoint:
        return _ROW_COLL_OFFSETS[facing]


_ROW_COLL_OFFSETS: dict[Direction, GridPoint] = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}

def add_points(a: GridPoint, b: GridPoint) -> GridPoint:
    return a[0] + b[0], a[1] + b[1]

class Position(NamedTuple):
    loc: GridPoint
    facing: Direction

    @property
    def next_loc(self) -> GridPoint:
        return add_points(self.loc, Direction.offset(self.facing))

    def step(self) -> "Position":
        return Position(self.next_loc, self.facing)

    def rotate_and_step(self, towards: Rotation):
        return Position(self.loc, Direction.rotate(self.facing, towards)).step()


State = tuple[int, Position, int]

queue: list[State] = [
            (0, Position((0, 0), Direction.DOWN), 0),
            (0, Position((0, 0), Direction.RIGHT), 0),
        ]

seen: set[tuple[Position, int]] = set()


target = len(city) - 1, len(city[-1]) - 1
grid = {}
for i, row in enumerate(city):
    for j, val in enumerate(row):
        grid[(i, j)] = val

min_steps = 4
max_steps = 10

def solve(min_steps, max_steps):

    queue: list[State] = [
        (0, Position((0, 0), Direction.DOWN), 0),
        (0, Position((0, 0), Direction.RIGHT), 0),
    ]
    seen: set[tuple[Position, int]] = set()

    while queue:
        cost, pos, num_steps = heappop(queue)

        if pos.loc == target and num_steps >= min_steps:
            return cost

        if (pos, num_steps) in seen:
            continue
        seen.add((pos, num_steps))

        if (
            num_steps >= min_steps
            and (left := pos.rotate_and_step("CCW")).loc in grid
        ):
            heappush(queue, (cost + grid[left.loc], left, 1))

        if (
            num_steps >= min_steps
            and (right := pos.rotate_and_step("CW")).loc in grid
        ):
            heappush(queue, (cost + grid[right.loc], right, 1))

        if num_steps < max_steps and (forward := pos.step()).loc in grid:
            heappush(queue, (cost + grid[forward.loc], forward, num_steps + 1))

    print("No solution found")

print(f"Part 1: {solve(1, 3)}")
print(f"Part 2: {solve(4, 10)}")