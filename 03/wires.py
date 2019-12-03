class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'


class WireSegment:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end


def load_wires() -> tuple:
    with open('wires.txt') as f:
        return tuple([line.strip('\n').split(',') for line in f])


def parse_wire_to_segments(wire: list) -> list:
    start = Point(0, 0)
    segments = []

    for segment in wire:
        direction = segment[0]
        distance = int(segment[1:])
        end = Point(start.x, start.y)

        if direction == 'L':
            end.x = start.x - distance
        elif direction == 'R':
            end.x = start.x + distance
        elif direction == 'U':
            end.y = start.y + distance
        elif direction == 'D':
            end.y = start.y - distance

        segments.append(WireSegment(start, end))
        start = Point(end.x, end.y)

    return segments


def is_horizontal(wire: WireSegment) -> bool:
    return wire.start.y == wire.end.y


def are_wires_parallel(seg1: WireSegment, seg2: WireSegment) -> bool:
    return (is_horizontal(seg1) and is_horizontal(seg2)) or (not is_horizontal(seg1) and not is_horizontal(seg2))


def find_intersection(seg1: WireSegment, seg2: WireSegment) -> Point:
    # Assume there are no overlapping wires, only single-point crossings.
    if are_wires_parallel(seg1, seg2):
        return None

    if is_horizontal(seg1):
        horizontal = seg1
        vertical = seg2
    else:
        horizontal = seg2
        vertical = seg1

    assert horizontal.start.y == horizontal.end.y
    assert vertical.start.x == vertical.end.x

    # A crossing in the wires occurs if the x coordinate of the vertical wire segment is between the start and end points of the horizontal segment,
    # and the y coordinate of the horizontal segment is also in the range of the vertical segment.
    x_min = min(horizontal.start.x, horizontal.end.x)
    x_max = max(horizontal.start.x, horizontal.end.x)
    y_min = min(vertical.start.y, vertical.end.y)
    y_max = max(vertical.start.y, vertical.end.y)

    if vertical.start.x >= x_min and vertical.start.x <= x_max \
       and horizontal.start.y >= y_min and horizontal.start.y <= y_max:
        return Point(vertical.start.x, horizontal.start.y)
    else:
        return None


def manhanttan_distance(p1: Point, p2: Point) -> int:
    return abs(p2.x-p1.x) + abs(p2.y-p1.y)


def get_steps_to_intersection(wire1: list, wire2: list, intersection: Point) -> int:
    steps = sum([manhanttan_distance(seg.start, seg.end) for seg in wire1[:-1]])
    steps += sum([manhanttan_distance(seg.start, seg.end) for seg in wire2[:-1]])
    steps += manhanttan_distance(wire1[-1].start, intersection)
    steps += manhanttan_distance(wire2[-1].start, intersection)

    return steps


first_wire, second_wire = load_wires()
#first_wire = ['R8', 'U5', 'L5', 'D3']
#second_wire = ['U7', 'R6', 'D4', 'L4']

first_segments = parse_wire_to_segments(first_wire)
second_segments = parse_wire_to_segments(second_wire)

steps = []
distances = []
origin = Point(0, 0)

for i, seg1 in enumerate(first_segments):
    for j, seg2 in enumerate(second_segments):
        intersection = find_intersection(seg1, seg2)

        if intersection is not None:
            distances.append(manhanttan_distance(intersection, origin))
            steps.append(get_steps_to_intersection(
                first_segments[:i], second_segments[:j], intersection))

print(sorted(distances)[0])
print(sorted(steps)[0])
