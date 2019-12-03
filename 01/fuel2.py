def calculate_fuel(mass):
    fuel = mass // 3 - 2
    return fuel if fuel > 0 else 0

total_fuel = 0
with open('masses.txt') as f:
    for line in f:
        current_mass = int(line)

        while current_mass > 0:
            fuel = calculate_fuel(current_mass)
            total_fuel += fuel
            current_mass = fuel

print(total_fuel)