import itertools

from typing import List
from enum import Enum
from common.cartesian import get_orthogonal_points, Point, TextGrid
from common.input_handling import get_input
from common.intcode_computer import Computer, ParameterMode

def load_instructions() -> List[int]:
    return get_input("input/input17.txt", int, delimiter=",")

def is_surrounded_by_scaffolds(scaffold: Point, text_grid: TextGrid) -> bool:
    adjacent_points = get_orthogonal_points(scaffold)
    return all(text_grid.get(p) == '#' for p in adjacent_points)

class Orientation(Enum):
    LEFT=1,
    RIGHT=2,
    UP=3,
    DOWN=4

    def get_next_point(self, point: Point) -> Point:
        match self:
            case Orientation.UP: return point.to_above()
            case Orientation.DOWN: return point.to_below()
            case Orientation.LEFT: return point.to_left()
            case Orientation.RIGHT: return point.to_right()
        assert False, "Out of orientations"
    
    def turn_left(self) -> 'Orientation':
        match self:
            case Orientation.UP: return Orientation.LEFT
            case Orientation.DOWN: return Orientation.RIGHT
            case Orientation.LEFT: return Orientation.DOWN
            case Orientation.RIGHT: return Orientation.UP
        assert False, "Out of orientations"
    
    def turn_right(self) -> 'Orientation':
        match self:
            case Orientation.UP: return Orientation.RIGHT
            case Orientation.DOWN: return Orientation.LEFT
            case Orientation.LEFT: return Orientation.UP
            case Orientation.RIGHT: return Orientation.DOWN
        assert False, "Out of orientations"
    
    def opposite(self) -> 'Orientation':
        match self:
            case Orientation.UP: return Orientation.DOWN
            case Orientation.DOWN: return Orientation.UP
            case Orientation.LEFT: return Orientation.RIGHT
            case Orientation.RIGHT: return Orientation.LEFT
        assert False, "Out of orientations"

    def __str__(self) -> str:
        match self:
            case Orientation.UP: return "U"
            case Orientation.DOWN: return "D"
            case Orientation.LEFT: return "L"
            case Orientation.RIGHT: return "R"
        assert False, "Out of orientations"


    
def get_orientation(symbol: str) -> Orientation:
    return {
        '<': Orientation.LEFT,
        '>': Orientation.RIGHT,
        '^': Orientation.UP,
        'v': Orientation.DOWN,
    }[symbol]

Moves = list[int | Orientation]
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
    

    def get_next_orientation(self, text_grid: TextGrid, next_point: Point, next_orientation: Orientation) -> tuple[Orientation, Orientation] | None:
        if text_grid.get(next_orientation.turn_left().get_next_point(next_point)) == '#':
            return (Orientation.LEFT, next_orientation.turn_left())
        elif text_grid.get(next_orientation.turn_right().get_next_point(next_point)) == '#':
            return (Orientation.RIGHT, next_orientation.turn_right())
        return None


    def get_route(self) -> Moves:
        text_grid = TextGrid(self.points.split('\n'))
        current_position = text_grid.get_all_points_matching_function(lambda c: c in '<<>^v')[0]
        current_orientation = get_orientation(text_grid.get(current_position))
        moves : Moves = []
        if text_grid.get(current_orientation.get_next_point(current_position )) == '.':
            turn, current_orientation = self.get_next_orientation(text_grid, current_position, current_orientation)
            moves.append(turn)

        last_move = 0
        next_point = current_position
        next_orientation = current_orientation
        while True:
            new_point = next_orientation.get_next_point(next_point)
            if text_grid.get(new_point) == '#':
                last_move += 1 
                next_point = new_point
            else:
                moves.append(last_move)
                last_move = 0
                next_move = self.get_next_orientation(text_grid, next_point, next_orientation)
                if not next_move:
                    break  # we are at the end
                turn, next_orientation = next_move
                moves.append(turn.opposite())  # we do the opposite because our coorindate system is not upside down
        return moves

    
    def get_programs(self):
        route = self.get_route()
        max_index = 100 
        for a_len, b_len, c_len in itertools.product(range(1,11), range(1,11), range(1,11)):
            candidates = [([], [], [], [], list(route))]
            while candidates:
                path,a,b,c,remaining_route = candidates.pop()
                if len(",".join(path)) > 20 or len(",".join(str(x) for x in a)) > 20 or len(",".join(str(x) for x in b)) > 20 or len(",".join(str(x) for x in c)) > 20:
                    continue
                if not remaining_route:
                    return path, a, b, c
                if a and remaining_route[:len(a)] == a:
                    candidates.append((path + ['A'], a, b, c, remaining_route[len(a):]))
                if b and remaining_route[:len(b)] == b:
                    candidates.append((path + ['B'], a, b, c, remaining_route[len(b):]))
                if c and remaining_route[:len(c)] == c:
                    candidates.append((path + ['C'], a, b, c, remaining_route[len(c):]))
                if not a:
                    candidates.append((path+['A'], remaining_route[:a_len], b, c, remaining_route[a_len:])) # assign a to a certain length
                    last_value = remaining_route[a_len - 1]
                    if type(last_value) == int:
                        for val in range(1,last_value):
                            new_remaining_route = remaining_route[:a_len - 1] + [val, last_value - val] + remaining_route[a_len + 2:]
                            candidates.append((path+['A'], new_remaining_route[:a_len], b, c, new_remaining_route[a_len:])) # assign a to a certain length
                elif not b:
                    candidates.append((path+['B'], a, remaining_route[:b_len], c, remaining_route[b_len:])) # assign b to a certain length
                    last_value = remaining_route[b_len - 1]
                    if type(last_value) == int:
                        for val in range(1,last_value):
                            new_remaining_route = remaining_route[:b_len - 1] + [val, last_value - val] + remaining_route[b_len + 2:]
                            candidates.append((path+['B'], a, new_remaining_route[:b_len], c, new_remaining_route[b_len:])) # assign b to a certain length
                elif not c:
                    candidates.append((path+['C'], a, b, remaining_route[:c_len], remaining_route[c_len:])) # assign c to a certain length
                    last_value = remaining_route[c_len - 1]
                    if type(last_value) == int:
                        for val in range(1,last_value):
                            new_remaining_route = remaining_route[:c_len - 1] + [val, last_value - val] + remaining_route[c_len + 2:]
                            candidates.append((path+['C'], a, b, new_remaining_route[:c_len], new_remaining_route[c_len:])) # assign c to a certain length
        assert False, "Should not reach here"

def get_alignment(intersection: Point) -> int:
    return intersection.x * intersection.y

def run_program():
    computer = Computer(load_instructions())
    scaffolding = Scaffolding()
    computer.output_function = scaffolding.plot_point
    computer.run_loop()
    return sum(get_alignment(i) for i in scaffolding.find_intersections())


def get_alignment(intersection: Point) -> int:
    return intersection.x * intersection.y

def run_program():
    computer = Computer(load_instructions())
    scaffolding = Scaffolding()
    computer.output_function = scaffolding.plot_point
    computer.run_loop()
    return sum(get_alignment(i) for i in scaffolding.find_intersections())


class VacuumRobot:
    def __init__(self, scaffolding: Scaffolding):
        self.scaffolding = scaffolding

        self.programs = self.scaffolding.get_programs()
        self.computer = Computer(load_instructions())
        self.computer.write(0, ParameterMode.POSITIONAL, 2)
        self.computer.output_function = self.read_dust
        self.computer.input_function = self.get_programs
        self.dust = 0
        self.line = None
        self.sent_visual = False

    def get_programs(self):
        if self.programs or self.line:
            if not self.line:
                self.line = ",".join(str(x) for x in self.programs[0]) + "\n"
                self.programs = self.programs[1:]
            c = self.line[0]
            self.line = self.line[1:]
            return ord(c)
        if not self.sent_visual:
            self.sent_visual = True
            return ord('n')
        return ord("\n")

    def run(self):
        self.computer.run_loop()

    def read_dust(self, val):
        self.dust = val


def get_space_dust() -> int:
    computer = Computer(load_instructions())
    scaffolding = Scaffolding()
    computer.output_function = scaffolding.plot_point
    computer.run_loop()

    robot = VacuumRobot(scaffolding)
    robot.run()
    return robot.dust 

if __name__ == "__main__":
    print(run_program())
    print(get_space_dust())
