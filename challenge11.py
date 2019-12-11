from collections import defaultdict
from enum import IntEnum, unique
from typing import List

from common.cartesian import draw, ORIGIN, Point
from common.input_handling import get_input
from common.intcode_computer import Computer

def load_instructions() -> List[int]:
    return get_input("input/input11.txt", int, delimiter=",")

@unique
class Color(IntEnum):
    BLACK = 0
    WHITE = 1

DIRECTIONS = [Point.to_above, Point.to_right, Point.to_below, Point.to_left]

class Robot:
    def __init__(self, color: Color):
        self.position = ORIGIN
        self.tracked_squares: defaultdict = defaultdict(lambda: Color.BLACK)
        self.tracked_squares[self.position] = color
        self.direction_index = 0
        self.outputter = Robot.paint

    def output_func(self, value: int):
        self.outputter(self, value)
        self.outputter = Robot.turn if self.outputter == Robot.paint else Robot.paint

    def input_func(self):
        return int(self.tracked_squares[self.position])

    def paint(self, value: int):
        self.tracked_squares[self.position] = Color(value)

    def turn(self, value: int):
        self.direction_index += 1 if value else -1
        direction_func = DIRECTIONS[self.direction_index % 4]
        self.position = direction_func(self.position)

    def get_painted_squares(self):
        return len(self.tracked_squares)

def run_program(color: Color):
    computer = Computer(load_instructions())
    robot = Robot(color)
    computer.input_function = robot.input_func
    computer.output_function = robot.output_func
    computer.run_loop()
    return robot


def draw_code():
    robot = run_program(Color.WHITE)
    info = robot.tracked_squares
    draw(info, (lambda c: '█' if c == Color.WHITE else ' '), inverted=True)

if __name__ == "__main__":
    print(run_program(Color.BLACK).get_painted_squares())
    draw_code()
