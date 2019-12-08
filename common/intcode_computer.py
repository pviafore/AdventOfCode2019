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
    def __init__(self, program: List[int], *, quiet=False, name="Computer"):
        self._memory = list(program)
        self._instruction_pointer = 0
        self._input_values: List[int] = []
        self._last_output = 0
        self.name = name

        self.input_function: Callable[[], int] = lambda: int(input("Please enter a value: "))
        self.output_function: Callable[[int], None] = print
        if quiet:
            self.output_function = lambda _: None

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

    def _input(self, _paramjeter_mode) -> int:
        if not self._input_values:
            value = self.input_function()
        else:
            value = self._input_values.pop(0)
        destination = self._get_parameters(1)[0]

        self.write(destination, int(value))
        return 2

    def _output(self, parameter_mode) -> int:
        destination = self._get_parameters(1)[0]
        self._last_output = self.read(destination, ParameterMode.FIRST in parameter_mode)
        self.output_function(self._last_output)
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
        return len(self._memory)

    def run_loop(self):
        try:
            while self._instruction_pointer < len(self._memory):
                parameter_mode, opcode = self._get_opcode()
                operation = self._opcode_mapping(opcode)
                relative_jump = operation(parameter_mode)
                self._jump(self._instruction_pointer + relative_jump)
        except Exception as exc:
            print(f"Error: {exc}")
            print(self._memory)
            print(self._instruction_pointer)
            raise exc

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

    def inject_input(self, *input_values: int):
        self._input_values += [x for x in input_values]

    def get_last_output(self) -> int:
        return self._last_output
