from typing import Generator, List

from common.cartesian import get_orthogonal_points, Point, TextGrid
from common.input_handling import get_input
from common.intcode_computer import Computer, ParameterMode

def load_instructions() -> List[int]:
    return get_input("input/input17.txt", int, delimiter=",")

def is_surrounded_by_scaffolds(scaffold: Point, text_grid: TextGrid) -> bool:
    adjacent_points = get_orthogonal_points(scaffold)
    return all(text_grid.get(p) == '#' for p in adjacent_points)

def to_left(symbol: str) -> str:
    return {
        '<': 'v',
        'v': '>',
        '>': '^',
        '^': '<'
    }[symbol]

def to_right(symbol: str) -> str:
    return {
        '<': '^',
        'v': '<',
        '>': 'v',
        '^': '>'
    }[symbol]

class Scaffolding:

    def __init__(self):
        self.points: str = ''

    def plot_point(self, value: int):
        self.points += chr(value)

    def __str__(self) -> str:
        return str(self.points)

    def find_intersections(self) -> List[Point]:
        text_grid = TextGrid(self.points.split('\n'))
        scaffolds = text_grid.get_all_points_matching_symbol('#')
        return [s for s in scaffolds if is_surrounded_by_scaffolds(s, text_grid)]

    def get_possible_routes(self) -> Generator[str, None, None]:
        # text_grid = TextGrid(self.points.split('\n'))
        # routes = []
        while self.points:
            #current_position = text_grid.get_all_points_matching_function(lambda c: c in '<<>^v')
            # left = to_left(text_grid[current_position[0]])
            # right = to_right(text_grid[current_position[0]])
            break
        # to-do figure this out later
        yield 'abc'



def get_alignment(intersection: Point) -> int:
    return intersection.x * intersection.y

def run_program():
    computer = Computer(load_instructions())
    scaffolding = Scaffolding()
    computer.output_function = scaffolding.plot_point
    computer.run_loop()
    return sum(get_alignment(i) for i in scaffolding.find_intersections())

def get_functions(_possible_route: str) -> List[str]:
    return []

class VacuumRobot:
    def __init__(self, scaffolding: Scaffolding):
        self.scaffolding = scaffolding

        self.computer = Computer(load_instructions())
        self.computer.write(0, ParameterMode.POSITIONAL, 2)
        self.computer.input_function = self.get_movement_routines
        for possible_route in scaffolding.get_possible_routes():
            functions = get_functions(possible_route)
            if len(functions) == 4:
                self.functions = functions
                break
        self.functions.append('n')

    def run(self):
        self.computer.run_loop()

    def get_movement_routines(self) -> int:
        return ord(self.functions.pop(0)) if self.functions else ord("\n")


def get_space_dust() -> int:
    computer = Computer(load_instructions())
    scaffolding = Scaffolding()
    computer.output_function = scaffolding.plot_point
    computer.run_loop()

    robot = VacuumRobot(scaffolding)
    robot.run()
    return 0

if __name__ == "__main__":
    print(run_program())
    print(get_space_dust())
