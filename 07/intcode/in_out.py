from abc import ABC, abstractmethod


class IntcodeIO(ABC):
    @property
    @abstractmethod
    def must_await_next_input(self):
        pass

    @abstractmethod
    def get_input(self):
        pass

    @abstractmethod
    def output(self, val: str):
        pass


class ConsoleIO(IntcodeIO):
    must_await_next_input = False

    def get_input(self) -> int:
        return int(input('Enter value: '))

    def output(self, val: str):
        print(f'Output: {val}')


# Returns inputs to the computer from a list.
class ListBasedIO(IntcodeIO):
    def __init__(self):
        self.inputs = []
        self.input_index = 0
        self.outputs = []
        self._must_await_next_input = False

    @property
    def must_await_next_input(self):
        return self._must_await_next_input

    def get_input(self) -> int:
        if self.input_index < len(self.inputs):
            inp = self.inputs[self.input_index]
            self.input_index += 1
            self._must_await_next_input = False
            return inp
        else:
            self._must_await_next_input = True
            return None

    def output(self, val: str):
        self.outputs.append(val)

    def set_input(self, inp: list):
        self.input_index = 0
        self.inputs = inp
        self.outputs = []
