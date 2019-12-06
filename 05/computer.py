from memory import Memory
from instructions import InstructionParser


class Computer:
    def __init__(self):
        self.memory = Memory()

    def load_program(self, filename: str):
        with open(filename) as f:
            self.memory.load([int(opcode)
                              for opcode in f.readline().split(',')])

    def run(self):
        ptr = 0
        while ptr < self.memory.size:
            instruction = InstructionParser.parse(self.memory, ptr)
            instruction.execute(self.memory)
            ptr = instruction.get_next_pointer(ptr)


if __name__ == "__main__":
    c = Computer()
    c.load_program('opcodes.txt')
    c.run()
