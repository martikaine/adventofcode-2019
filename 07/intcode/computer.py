from intcode.memory import Memory
from intcode.in_out import IntcodeIO
from intcode.instructions import InstructionParser


class Computer:
    def __init__(self, io: IntcodeIO):
        self.memory = Memory()
        self.io = io
        self.ptr = 0
        self.is_halted = True

    def load_program(self, filename: str):
        self.ptr = 0
        with open(filename) as f:
            self.memory.load([int(opcode)
                              for opcode in f.readline().split(',')])

    def run(self):
        self.is_halted = False

        while True:
            instruction = InstructionParser.parse(self.memory, self.ptr)
            instruction.execute(self.memory, self.io)

            # No input available yet. Freeze here and do not advance the program
            # until run() is called with the IO being able to provide input.
            if self.io.must_await_next_input:
                break

            self.ptr = instruction.get_next_pointer(self.ptr)

            if self.ptr >= self.memory.size:
                self.is_halted = True
                break
