def is_valid_password(candidate: int) -> bool:
    has_adjacent_digits = False
    has_increasing_digits = True

    digits = [int(digit) for digit in str(candidate)]
    previous_digit = digits[0]

    for digit in digits[1:]:
        if digit < previous_digit:
            has_increasing_digits = False
            break
        if digit == previous_digit:
            has_adjacent_digits = True

        previous_digit = digit

    return has_adjacent_digits and has_increasing_digits

assert is_valid_password(111111)
assert not is_valid_password(223450)
assert not is_valid_password(123789)

valid_passwords = 0

for candidate in range(356261, 846303):
    if is_valid_password(candidate):
        valid_passwords += 1

print(f'task 1: {valid_passwords}')