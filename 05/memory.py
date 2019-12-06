class Memory:
    def __init__(self):
        self._memory = []

    def load(self, content: list):
        self._memory = content

    def peek(self, address: int) -> int:
        return self._memory[address]

    def peek_range(self, address: int, num: int) -> list:
        return self._memory[address:address+num]

    def poke(self, address: int, value: int):
        self._memory[address] = value

    @property
    def size(self):
        return len(self._memory)
