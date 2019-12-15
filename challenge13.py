from collections import defaultdict
from enum import Enum, IntEnum, unique
from typing import  List, Optional

from common.cartesian import draw, Point
from common.input_handling import get_input
from common.intcode_computer import Computer, ParameterMode

def load_instructions() -> List[int]:
    return get_input("input/input13.txt", int, delimiter=",")

@unique
class TileType(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    def __str__(self):
        return " |█-*"[int(self.value)]

@unique
class JoyStickInput(IntEnum):
    LEFT = -1
    NEUTRAL = 0
    RIGHT = 1

class Game:

    def __init__(self, should_draw=False):
        self.canvas: defaultdict = defaultdict(lambda: TileType.EMPTY)
        self.xpos: Optional[int] = None
        self.ypos: Optional[int] = None
        self.score: int = 0
        self.ball: Point = Point(0, 0)
        self.draw = should_draw

    def display(self):
        print('\x1b[2J\x1b[H')
        draw(self.canvas, inverted=True)
        print(self.score, self.ball)

    def draw_tile(self, value: int):
        if self.xpos is None:
            self.xpos = value
        elif self.ypos is None:
            self.ypos = value
        else:
            if self.xpos == -1 and self.ypos == 0:
                self.score = value
            else:
                if TileType(value) == TileType.BALL:
                    self.ball = Point(self.xpos, self.ypos)
                self.canvas[Point(self.xpos, self.ypos)] = TileType(value)
            self.xpos = self.ypos = None
            if self.draw:
                self.display()

    def get_number_of_blocks(self) -> int:
        return list(self.canvas.values()).count(TileType.BLOCK)

    def get_score(self) -> int:
        return self.score

    def get_joystick_input(self) -> int:
        paddles = [p.x for p, tile_type in self.canvas.items() if tile_type == TileType.PADDLE]
        paddle_pos = paddles[0]
        if paddle_pos == self.ball.x:
            return JoyStickInput.NEUTRAL
        return JoyStickInput.LEFT if paddle_pos > self.ball.x else JoyStickInput.RIGHT


def run_program(input_value: Optional[int] = None, should_draw=False) -> Game:
    computer = Computer(load_instructions())
    if input_value:
        computer.write(0, ParameterMode.POSITIONAL, input_value)
    game = Game(should_draw)
    computer.input_function = game.get_joystick_input
    computer.output_function = game.draw_tile
    computer.run_loop()
    return game



if __name__ == "__main__":
    print(run_program().get_number_of_blocks())
    print(run_program(2).get_score())
