from intcode.computer import Computer
from intcode.in_out import ListBasedIO, ConsoleIO


def unique_combinations(sequence: list) -> list:
    if len(sequence) == 1:
        return [sequence]
    else:
        combinations = []
        for i in sequence:
            subset = [item for item in sequence if item != i]

            for subset_combination in unique_combinations(subset):
                combinations.append([i, *subset_combination])

        return combinations


def solve_part_one():
    best = 0
    io = ListBasedIO()
    com = Computer(io)
    for settings in unique_combinations([0, 1, 2, 3, 4]):

        prev_out = 0
        for i in settings:
            io.set_input([i, prev_out])
            com.load_program('program.txt')
            com.run()

            prev_out = io.outputs[0]

        if prev_out > best:
            best = prev_out

    print(best)


def run_feedback_loop(settings: list, filename: str):
    ios = [ListBasedIO()] * 5
    computers = [Computer(ios[i]) for i in range(5)]

    for com in computers:
        com.load_program(filename)

    prev_output = 0

    for i in range(5):
        ios[i].set_input([settings[i], prev_output])
        computers[i].run()
        prev_output = ios[i].outputs[0]

    i = 0
    while not computers[4].is_halted:
        ios[i].set_input([prev_output])
        computers[i].run()
        prev_output = ios[i].outputs[0]
        i += 1
        if i > 4:
            i = 0

    return prev_output


def solve_part_two():
    best = 0

    for settings in unique_combinations([5, 6, 7, 8, 9]):
        output = run_feedback_loop(settings, 'program.txt')
        if output > best:
            best = output

    print(best)


solve_part_one()
#print(run_feedback_loop([9,8,7,6,5], 'test1.txt'))
solve_part_two()
