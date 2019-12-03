def load() -> list:
    with open('opcodes.txt') as f:
        return [int(opcode) for opcode in f.readline().split(',')]

def add(program: list, ptr: int) -> list:
    program[program[ptr+3]] = program[program[ptr+1]] + program[program[ptr+2]] 
    return program

def multiply(program: list, ptr: int) -> list:
    program[program[ptr+3]] = program[program[ptr+1]] * program[program[ptr+2]] 
    return program

def run(program: list) -> int:
    valid_codes = [1, 2, 99]
    
    for ptr in range(0, len(program), 4):
        opcode = program[ptr]
        assert opcode in valid_codes

        if opcode == 1:
            program = add(program, ptr)
        elif opcode == 2:
            program = multiply(program, ptr)
        elif opcode == 99:
            break

    return program[0]

def solve_part_one() -> int:
    program = load()
    program[1] = 12
    program[2] = 2

    return run(program)

def solve_part_two() -> int:
    for noun in range(0, 100):
        for verb in range(0, 100):
            program = load()
            program[1] = noun
            program[2] = verb

            result = run(program)

            if result == 19690720:
                return 100 * noun + verb

print(f'part 1: {solve_part_one()}')
print(f'part 2: {solve_part_two()}')