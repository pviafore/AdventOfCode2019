from typing import List

from common.input_handling import get_input
from common.intcode_computer import Computer

def load_instructions() -> List[int]:
    return get_input("input/input5.txt", int, delimiter=",")

def run_program(input_value):
    computer = Computer(load_instructions())
    computer.inject_input(input_value)
    computer.run_loop()
    return computer.get_last_output()

if __name__ == "__main__":
    run_program(1)
    run_program(5)
