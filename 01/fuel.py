total_fuel = 0
with open('masses.txt') as f:
    for line in f:
        mass = int(line)
        total_fuel += mass // 3 - 2

print(total_fuel)
