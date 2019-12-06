from enum import IntEnum, IntFlag
from typing import Callable, List

class OpCode(IntEnum):
    ADD = 1
    MULTIPLY = 2
    STOP = 99

class ParameterMode(IntFlag):
    FIRST = 1
    SECOND = 2
    THIRD = 4


ComputerOperation = Callable[[], int]

class Computer:
    def __init__(self, program: List[int]):
        self._halted = False
        self._memory = program
        self._instruction_pointer = 0

    def _opcode_mapping(self, code: OpCode) -> ComputerOperation:
        return {
            OpCode.ADD: self._add,
            OpCode.MULTIPLY: self._multiply,
            OpCode.STOP: self._halt
        }[code]

    def _get_parameters(self, size: int = 3) -> List[int]:
        return self._memory[self._instruction_pointer + 1:self._instruction_pointer + 1 + size]

    def _add(self) -> int:
        address1, address2, destination = self._get_parameters()
        self._memory[destination] = self._memory[address1] + self._memory[address2]
        return 4

    def _multiply(self) -> int:
        address1, address2, destination = self._get_parameters()
        self._memory[destination] = self._memory[address1] * self._memory[address2]
        return 4

    def _halt(self) -> int:
        self._halted = True
        return 0

    def run_loop(self):
        while not self._halted:
            opcode = self._memory[self._instruction_pointer]
            operation = self._opcode_mapping(opcode)
            self._instruction_pointer += operation()

    def write(self, address: int, value: int):
        self._memory[address] = value

    def read(self, address: int) -> int:
        return self._memory[address]
