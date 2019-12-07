from enum import Enum
from abc import ABC, abstractmethod
from intcode.memory import Memory
from intcode.in_out import IntcodeIO


class Opcode(Enum):
    add = 1
    multiply = 2
    store = 3
    output = 4
    jump_if_true = 5
    jump_if_false = 6
    less_than = 7
    equals = 8
    halt = 99


class ParameterMode(Enum):
    position = 0
    immediate = 1


class Instruction(ABC):
    def __init__(self, parameters: list, parameter_modes: list):
        self.parameters = parameters
        self.parameter_modes = parameter_modes

    @abstractmethod
    def execute(self, memory: Memory, io: IntcodeIO):
        pass

    def get_next_pointer(self, current_ptr: int) -> int:
        return current_ptr + len(self.parameters) + 1

    def _get_value(self, index: int, memory: Memory) -> int:
        mode = self.parameter_modes[index]
        parameter = self.parameters[index]

        if mode == ParameterMode.position:
            return memory.peek(parameter)
        elif mode == ParameterMode.immediate:
            return parameter


class AddInstruction(Instruction):
    def __init__(self, parameters: list, parameter_modes: list):
        super().__init__(parameters, parameter_modes)

    def execute(self, memory: Memory, io: IntcodeIO):
        value = self._get_value(0, memory) + self._get_value(1, memory)
        memory.poke(self.parameters[2], value)


class MultiplyInstruction(Instruction):
    def __init__(self, memory: Memory, ptr: int):
        super().__init__(memory, ptr)

    def execute(self, memory: Memory, io: IntcodeIO):
        value = self._get_value(0, memory) * self._get_value(1, memory)
        memory.poke(self.parameters[2], value)


class StoreInstruction(Instruction):
    def __init__(self, parameters: list, parameter_modes: list):
        super().__init__(parameters, parameter_modes)

    def execute(self, memory: Memory, io: IntcodeIO):
        value = io.get_input()
        memory.poke(self.parameters[0], value)


class OutputInstruction(Instruction):
    def __init__(self, parameters: list, parameter_modes: list):
        super().__init__(parameters, parameter_modes)

    def execute(self, memory: Memory, io: IntcodeIO):
        io.output(self._get_value(0, memory))


class JumpIfTrueInstruction(Instruction):
    def __init__(self, parameters: list, parameter_modes: list):
        super().__init__(parameters, parameter_modes)
        self.jump_address = -1

    def execute(self, memory: Memory, io: IntcodeIO):
        if self._get_value(0, memory) != 0:
            self.jump_address = self._get_value(1, memory)

    def get_next_pointer(self, current_ptr: int):
        if self.jump_address >= 0:
            return self.jump_address
        else:
            return super().get_next_pointer(current_ptr)


class JumpIfFalseInstruction(Instruction):
    def __init__(self, parameters: list, parameter_modes: list):
        super().__init__(parameters, parameter_modes)
        self.jump_address = -1

    def execute(self, memory: Memory, io: IntcodeIO):
        if self._get_value(0, memory) == 0:
            self.jump_address = self._get_value(1, memory)

    def get_next_pointer(self, current_ptr: int):
        if self.jump_address >= 0:
            return self.jump_address
        else:
            return super().get_next_pointer(current_ptr)


class LessThanInstruction(Instruction):
    def __init__(self, parameters: list, parameter_modes: list):
        super().__init__(parameters, parameter_modes)

    def execute(self, memory: Memory, io: IntcodeIO):
        value = int(self._get_value(0, memory) < self._get_value(1, memory))
        memory.poke(self.parameters[2], value)


class EqualsInstruction(Instruction):
    def __init__(self, parameters: list, parameter_modes: list):
        super().__init__(parameters, parameter_modes)

    def execute(self, memory: Memory, io: IntcodeIO):
        value = int(self._get_value(0, memory) == self._get_value(1, memory))
        memory.poke(self.parameters[2], value)


class HaltInstruction(Instruction):
    def __init__(self, parameters: list, parameter_modes: list):
        super().__init__(parameters, parameter_modes)
        self.end_address = 0

    def execute(self, memory: Memory, io: IntcodeIO):
        self.end_address = memory.size + 1

    def get_next_pointer(self, current_ptr: int):
        return self.end_address


class InstructionParser:
    parameter_counts = {
        Opcode.add: 3,
        Opcode.multiply: 3,
        Opcode.store: 1,
        Opcode.output: 1,
        Opcode.jump_if_true: 2,
        Opcode.jump_if_false: 2,
        Opcode.less_than: 3,
        Opcode.equals: 3,
        Opcode.halt: 0
    }

    @staticmethod
    def parse(memory: Memory, ptr: int) -> Instruction:
        instruction = memory.peek(ptr)
        opcode = Opcode(instruction % 100)

        parameter_count = InstructionParser.parameter_counts[opcode]
        parameter_modes = InstructionParser._parse_parameter_modes(
            instruction, parameter_count)
        parameters = memory.peek_range(ptr+1, parameter_count)

        if opcode == Opcode.add:
            return AddInstruction(parameters, parameter_modes)
        elif opcode == Opcode.multiply:
            return MultiplyInstruction(parameters, parameter_modes)
        elif opcode == Opcode.store:
            return StoreInstruction(parameters, parameter_modes)
        elif opcode == Opcode.output:
            return OutputInstruction(parameters, parameter_modes)
        elif opcode == Opcode.jump_if_true:
            return JumpIfTrueInstruction(parameters, parameter_modes)
        elif opcode == Opcode.jump_if_false:
            return JumpIfFalseInstruction(parameters, parameter_modes)
        elif opcode == Opcode.less_than:
            return LessThanInstruction(parameters, parameter_modes)
        elif opcode == Opcode.equals:
            return EqualsInstruction(parameters, parameter_modes)
        elif opcode == Opcode.halt:
            return HaltInstruction(parameters, parameter_modes)
        else:
            raise ValueError('Unsupported opcode')

    @staticmethod
    def _parse_parameter_modes(instruction: int, parameter_count: int) -> list:
        parameter_modes = [ParameterMode.position] * parameter_count

        modes = instruction // 100
        i = 0
        while modes > 0:
            parameter_modes[i] = ParameterMode(modes % 10)
            modes = modes // 10
            i += 1
        return parameter_modes
