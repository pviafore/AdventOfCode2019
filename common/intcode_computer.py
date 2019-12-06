from enum import IntEnum, Flag
from typing import Callable, List, Tuple

class OpCode(IntEnum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_TRUE = 5
    JUMP_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    STOP = 99

class ParameterMode(Flag):
    FIRST = 1
    SECOND = 2
    THIRD = 4


ComputerOperation = Callable[[ParameterMode], int]

class Computer:
    def __init__(self, program: List[int]):
        self._halted = False
        self._memory = program
        self._instruction_pointer = 0

    def _opcode_mapping(self, code: OpCode) -> ComputerOperation:
        return {
            OpCode.ADD: self._add,
            OpCode.MULTIPLY: self._multiply,
            OpCode.INPUT: self._input,
            OpCode.OUTPUT: self._output,
            OpCode.JUMP_TRUE: self._jump_if_true,
            OpCode.JUMP_FALSE: self._jump_if_false,
            OpCode.LESS_THAN: self._less_than,
            OpCode.EQUALS: self._equals,
            OpCode.STOP: self._halt
        }[code]

    def _get_parameters(self, size: int = 3) -> List[int]:
        return self._memory[self._instruction_pointer + 1:self._instruction_pointer + 1 + size]

    def _add(self, parameter_mode) -> int:
        address1, address2, destination = self._get_parameters()
        self.write(destination,
                   self.read(address1, ParameterMode.FIRST in parameter_mode) +
                   self.read(address2, ParameterMode.SECOND in parameter_mode))
        return 4

    def _multiply(self, parameter_mode) -> int:
        address1, address2, destination = self._get_parameters()
        self.write(destination,
                   self.read(address1, ParameterMode.FIRST in parameter_mode) *
                   self.read(address2, ParameterMode.SECOND in parameter_mode))
        return 4

    def _input(self, _parameter_mode) -> int:
        value = input("Enter in a value please: ")
        destination = self._get_parameters(1)[0]
        self.write(destination, int(value))
        return 2

    def _output(self, parameter_mode) -> int:
        destination = self._get_parameters(1)[0]
        print(self.read(destination, ParameterMode.FIRST in parameter_mode))
        return 2

    def _jump_if_true(self, parameter_mode) -> int:
        value, destination = self._get_parameters(2)
        if self.read(value, ParameterMode.FIRST in parameter_mode) != 0:
            self._jump(self.read(destination, ParameterMode.SECOND in parameter_mode))
            return 0
        return 3

    def _jump_if_false(self, parameter_mode) -> int:
        value, destination = self._get_parameters(2)
        if self.read(value, ParameterMode.FIRST in parameter_mode) == 0:
            self._jump(self.read(destination, ParameterMode.SECOND in parameter_mode))
            return 0
        return 3

    def _less_than(self, parameter_mode) -> int:
        address1, address2, destination = self._get_parameters(3)
        result = (self.read(address1, ParameterMode.FIRST in parameter_mode) <
                  self.read(address2, ParameterMode.SECOND in parameter_mode))
        self.write(destination, 1 if result else 0)
        return 4

    def _equals(self, parameter_mode) -> int:
        address1, address2, destination = self._get_parameters(3)
        result = (self.read(address1, ParameterMode.FIRST in parameter_mode) ==
                  self.read(address2, ParameterMode.SECOND in parameter_mode))
        self.write(destination, 1 if result else 0)
        return 4

    def _halt(self, _parameter_mode) -> int:
        self._halted = True
        return 0

    def run_loop(self):
        while not self._halted:
            parameter_mode, opcode = self._get_opcode()
            operation = self._opcode_mapping(opcode)
            relative_jump = operation(parameter_mode)
            self._jump(self._instruction_pointer + relative_jump)

    def _get_opcode(self) -> Tuple[ParameterMode, OpCode]:
        opcode = self.read(self._instruction_pointer)
        parameter = opcode // 100
        flags = int('0b' + str(parameter), base=2)
        return ParameterMode(flags), OpCode(opcode % 100)

    def write(self, address: int, value: int):
        self._memory[address] = value

    def read(self, address_or_value: int, immediate_mode=False) -> int:
        return address_or_value if immediate_mode else self._memory[address_or_value]

    def _jump(self, destination: int):
        self._instruction_pointer = destination
