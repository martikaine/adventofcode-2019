def is_valid_password(candidate: int) -> bool:
    has_two_adjacent_digits = False
    has_increasing_digits = True

    digits = [int(digit) for digit in str(candidate)]
    previous_digit = digits[0]
    repeat_count = 0
    
    for digit in digits[1:]:
        if digit < previous_digit:
            has_increasing_digits = False
            break
        elif digit == previous_digit:
            repeat_count += 1
        else:
            if repeat_count == 1:
                has_two_adjacent_digits = True
            repeat_count = 0

        previous_digit = digit

    if repeat_count == 1:
        has_two_adjacent_digits = True

    return has_two_adjacent_digits and has_increasing_digits

assert is_valid_password(112233)
assert not is_valid_password(123444)
assert is_valid_password(111122)

valid_passwords = 0

for candidate in range(356261, 846303):
    if is_valid_password(candidate):
        valid_passwords += 1

print(f'task 2: {valid_passwords}')