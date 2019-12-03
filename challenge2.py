from enum import IntEnum
from itertools import product
from typing import List


from common.input_handling import get_input

class OpCode(IntEnum):
    ADD = 1
    MULTIPLY = 2
    STOP = 99

Instructions = List[int]

def load_instructions() -> Instructions:
    return get_input("input/input2.txt", int, delimiter=",")

def run_loop(instructions: Instructions):
    instruction_pointer = 0
    while instructions[instruction_pointer] != OpCode.STOP:
        address1, address2, destination = (
            instructions[instruction_pointer + 1:instruction_pointer + 4]
        )
        if instructions[instruction_pointer] == OpCode.ADD:
            instructions[destination] = instructions[address1] + instructions[address2]
        elif instructions[instruction_pointer] == OpCode.MULTIPLY:
            instructions[destination] = instructions[address1] * instructions[address2]
        else:
            assert False, "Unknown opcode"
        instruction_pointer += 4

def get_value_at_address_zero_after_calculation(noun: int = 12, verb: int = 2) -> int:
    instructions = load_instructions()
    instructions[1] = noun
    instructions[2] = verb
    run_loop(instructions)
    return instructions[0]

def get_correct_noun_verb() -> int:
    for noun, verb in product(range(100), range(100)):
        value = get_value_at_address_zero_after_calculation(noun, verb)
        if value == 19690720:
            return 100 * noun + verb
    raise RuntimeError("You should not reach here, something's wrong")

if __name__ == "__main__":
    print(get_value_at_address_zero_after_calculation())
    print(get_correct_noun_verb())
