#!/usr/bin/env python3
import dataclasses
import enum

from ordered_set import OrderedSet
from rich import print

from helpers import load_input, parse_grid


@dataclasses.dataclass
class Node:
    char: str
    beams: OrderedSet["Direction"] = dataclasses.field(default_factory=OrderedSet)

    def __str__(self):
        if self.char in "|-":
            return self.char
        elif self.beams:
            return str(len(self.beams))
        return self.char

    def __repr__(self):
        return self.__str__()


class Direction(enum.Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)

    @property
    def char(self):
        if self is Direction.NORTH:
            return "^"
        elif self is Direction.SOUTH:
            return "v"
        elif self is Direction.WEST:
            return "<"
        else:
            return ">"


@dataclasses.dataclass
class Coord:
    x: int = 0
    y: int = 0

    def copy(self):
        return Coord(self.x, self.y)


@dataclasses.dataclass
class BeamTip:
    coord: Coord
    direction: Direction

    def move(self):
        self.coord.x += self.direction.value[0]
        self.coord.y += self.direction.value[1]

    def flip(self, char):
        if char not in "\\/":
            return

        if self.direction is Direction.EAST:
            self.direction = Direction.NORTH if char == "/" else Direction.SOUTH
        elif self.direction is Direction.WEST:
            self.direction = Direction.NORTH if char == "\\" else Direction.SOUTH
        elif self.direction is Direction.NORTH:
            self.direction = Direction.EAST if char == "/" else Direction.WEST
        else:
            self.direction = Direction.EAST if char == "\\" else Direction.WEST


def parse_file_contents(file_contents: str) -> list[list[Node]]:
    grid = parse_grid(file_contents, tile_class=Node)
    return grid


def part1(file_contents: str) -> int:
    grid = parse_file_contents(file_contents)
    print(grid)
    beams = [BeamTip(Coord(), Direction.EAST)]
    while beams:
        if (
            beams[0].coord.x < 0
            or beams[0].coord.x >= len(grid)
            or beams[0].coord.y < 0
            or beams[0].coord.y >= len(grid[0])
        ):
            beams.pop(0)
            continue
        tile = grid[beams[0].coord.x][beams[0].coord.y]
        if beams[0].direction in tile.beams:
            beams.pop(0)
            continue
        tile.beams.add(beams[0].direction)
        if tile.char == "|" and beams[0].direction in {Direction.EAST, Direction.WEST}:
            beams[0].direction = Direction.NORTH
            new_beam = BeamTip(beams[0].coord.copy(), Direction.SOUTH)
            new_beam.move()
            beams.append(new_beam)
        elif tile.char == "-" and beams[0].direction in {Direction.NORTH, Direction.SOUTH}:
            beams[0].direction = Direction.WEST
            new_beam = BeamTip(beams[0].coord.copy(), Direction.EAST)
            new_beam.move()
            beams.append(new_beam)
        elif tile.char in r"\/":
            beams[0].flip(tile.char)

        beams[0].move()
    return sum(1 for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y].beams)


def part2(file_contents: str) -> int:
    return 0


if __name__ == "__main__":
    answer1 = part1(load_input(__file__))
    answer2 = part2(load_input(__file__))
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""


def test_part1():
    assert part1(test_data) == 46


def test_part1_real():
    assert part1(load_input(__file__)) == 8249


def test_part2():
    assert part2(test_data) == 0


# def test_part2_real():
#     assert part2(load_input(__file__)) == 0
