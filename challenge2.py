from itertools import product
from typing import List

from common.input_handling import get_input
from common.intcode_computer import Computer

def load_instructions() -> List[int]:
    return get_input("input/input2.txt", int, delimiter=",")

def get_value_at_address_zero_after_calculation(noun: int = 12, verb: int = 2) -> int:
    computer = Computer(load_instructions())
    computer.write(1, noun)
    computer.write(2, verb)
    computer.run_loop()
    return computer.read(0)

def get_correct_noun_verb() -> int:
    for noun, verb in product(range(100), range(100)):
        value = get_value_at_address_zero_after_calculation(noun, verb)
        if value == 19690720:
            return 100 * noun + verb
    raise RuntimeError("You should not reach here, something's wrong")

if __name__ == "__main__":
    print(get_value_at_address_zero_after_calculation())
    print(get_correct_noun_verb())
