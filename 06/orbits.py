def parse_orbit_map(filename: str) -> dict:
    orbit_map = {}
    orbit_map['COM'] = None

    with open(filename) as f:
        for line in f:
            parent, me = line.strip('\n').split(')')
            orbit_map[me] = parent

    return orbit_map

def calculate_total_orbits(orbit_map: dict) -> int:
    count = 0

    for planet in orbit_map.values():
        parent = planet
        while parent != None:
            parent = orbit_map[parent]
            count += 1

    return count

def get_path_to_com(orbit_map: dict, start: str) -> list:
    path = []
    parent = start
    while parent != None:
        path.append(parent)
        parent = orbit_map[parent]

    return path

def calculate_shortest_path(orbit_map: dict) -> int:
    my_path_to_com = get_path_to_com(orbit_map, 'YOU')
    santa_path_to_com = get_path_to_com(orbit_map, 'SAN')
  
    for i, planet in enumerate(my_path_to_com):
        if planet in santa_path_to_com:
            #print(f'first intersection at planet: {planet}')
            my_distance_to_intersection = i - 1
            santa_distance_to_intersection = santa_path_to_com.index(planet) - 1
            
            return my_distance_to_intersection + santa_distance_to_intersection


orbit_map = parse_orbit_map('orbits.txt')
print(calculate_total_orbits(orbit_map))
print(calculate_shortest_path(orbit_map))