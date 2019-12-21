from dataclasses import dataclass, field
from enum import IntEnum, unique
from typing import Callable, List, Tuple

@unique
class OpCode(IntEnum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_TRUE = 5
    JUMP_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    SET_RELATIVE_VALUE = 9
    STOP = 99

@unique
class ParameterMode(IntEnum):
    POSITIONAL = 0
    IMMEDIATE = 1
    RELATIVE = 2


ComputerOperation = Callable[[List[ParameterMode]], int]

@dataclass
class Debug:
    input_values: List[int] = field(default_factory=list)
    last_output: int = 0

@dataclass
class Memory:
    memory: List[int]
    instruction_pointer: int
    relative_value: int
class Computer:
    def __init__(self, program: List[int], *, quiet=False, name="Computer"):
        self._memory = Memory(list(program), 0, 0)
        self._debug = Debug()
        self.name = name

        self.input_function: Callable[[], int] = lambda: int(input("Please enter a value: "))
        self.output_function: Callable[[int], None] = print
        self.halt_function: Callable[[], bool] = lambda: False
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
            OpCode.SET_RELATIVE_VALUE: self._set_relative_value,
            OpCode.STOP: self._halt
        }[code]

    def _get_parameters(self, size: int = 3) -> List[int]:
        return self._memory.memory[self._memory.instruction_pointer + 1:
                                   self._memory.instruction_pointer + 1 + size]

    def _add(self, parameter_modes: List[ParameterMode]) -> int:
        address1, address2, destination = self._get_parameters()
        self.write(destination, parameter_modes[2],
                   self.read(address1, parameter_modes[0]) +
                   self.read(address2, parameter_modes[1]))
        return 4

    def _multiply(self, parameter_modes: List[ParameterMode]) -> int:
        address1, address2, destination = self._get_parameters()
        self.write(destination, parameter_modes[2],
                   self.read(address1, parameter_modes[0]) *
                   self.read(address2, parameter_modes[1]))
        return 4

    def _input(self, parameter_modes: List[ParameterMode]) -> int:
        if not self._debug.input_values:
            value = self.input_function()
        else:
            value = self._debug.input_values.pop(0)
        destination = self._get_parameters(1)[0]

        self.write(destination, parameter_modes[0], int(value))
        return 2

    def _output(self, parameter_modes: List[ParameterMode]) -> int:
        destination = self._get_parameters(1)[0]
        self._debug.last_output = self.read(destination, parameter_modes[0])
        self.output_function(self._debug.last_output)
        return 2

    def _jump_if_true(self, parameter_modes: List[ParameterMode]) -> int:
        value, destination = self._get_parameters(2)
        if self.read(value, parameter_modes[0]) != 0:
            self._jump(self.read(destination, parameter_modes[1]))
            return 0
        return 3

    def _jump_if_false(self, parameter_modes: List[ParameterMode]) -> int:
        value, destination = self._get_parameters(2)
        if self.read(value, parameter_modes[0]) == 0:
            self._jump(self.read(destination, parameter_modes[1]))
            return 0
        return 3

    def _less_than(self, parameter_modes: List[ParameterMode]) -> int:
        address1, address2, destination = self._get_parameters(3)
        result = (self.read(address1, parameter_modes[0]) <
                  self.read(address2, parameter_modes[1]))
        self.write(destination, parameter_modes[2], 1 if result else 0)
        return 4

    def _equals(self, parameter_modes: List[ParameterMode]) -> int:
        address1, address2, destination = self._get_parameters(3)
        result = (self.read(address1, parameter_modes[0]) ==
                  self.read(address2, parameter_modes[1]))
        self.write(destination, parameter_modes[2], 1 if result else 0)
        return 4

    def _set_relative_value(self, parameter_modes: List[ParameterMode]) -> int:
        address1 = self._get_parameters(1)[0]
        self._memory.relative_value += self.read(address1, parameter_modes[0])
        return 2

    def _halt(self, _parameter_modes: List[ParameterMode]) -> int:
        return len(self._memory.memory)

    def run_loop(self):
        try:
            while (not self.halt_function() and
                   self._memory.instruction_pointer < len(self._memory.memory)):
                parameter_mode, opcode = self._get_opcode()
                operation = self._opcode_mapping(opcode)
                relative_jump = operation(parameter_mode)
                self._jump(self._memory.instruction_pointer + relative_jump)
        except Exception as exc:
            print(f"Error: {exc}")
            print(self._memory.memory)
            print(self._memory.instruction_pointer)
            raise exc

    def _get_opcode(self) -> Tuple[List[ParameterMode], OpCode]:
        opcode = self.read(self._memory.instruction_pointer)
        parameter = opcode // 100
        flags = [ParameterMode(int(p)) for p in ("000" + str(parameter))[::-1]][:3]
        return flags, OpCode(opcode % 100)

    def write(self, address: int, parameter_mode: ParameterMode, value: int):
        if parameter_mode == ParameterMode.POSITIONAL:
            self.extend_memory_if_necessary(address)
            self._memory.memory[address] = value
        if parameter_mode == ParameterMode.RELATIVE:
            self.extend_memory_if_necessary(address + self._memory.relative_value)
            self._memory.memory[address + self._memory.relative_value] = value

    def read(self,
             address_or_value: int,
             parameter_mode: ParameterMode = ParameterMode.POSITIONAL) -> int:
        if parameter_mode == ParameterMode.IMMEDIATE:
            return address_or_value
        if parameter_mode == ParameterMode.POSITIONAL:
            self.extend_memory_if_necessary(address_or_value)
            return self._memory.memory[address_or_value]
        if parameter_mode == ParameterMode.RELATIVE:
            self.extend_memory_if_necessary(address_or_value + self._memory.relative_value)
            return self._memory.memory[address_or_value + self._memory.relative_value]
        raise RuntimeError("Unknown Parameter Mode")


    def _jump(self, destination: int):
        self._memory.instruction_pointer = destination

    def inject_input(self, *input_values: int):
        self._debug.input_values += [*input_values]

    def get_last_output(self) -> int:
        return self._debug.last_output

    def extend_memory_if_necessary(self, address: int):
        if address >= len(self._memory.memory):
            self._memory.memory += [0] * (address - len(self._memory.memory) + 1)
