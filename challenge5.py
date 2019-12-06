from typing import List

from common.input_handling import get_input
from common.intcode_computer import Computer

def load_instructions() -> List[int]:
    return get_input("input/input5.txt", int, delimiter=",")

def run_first_program():
    computer = Computer(load_instructions())
    computer.run_loop()

if __name__ == "__main__":
    run_first_program()
