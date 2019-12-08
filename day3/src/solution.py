import os
import unittest


def get_manhattan_distance(position: tuple) -> int:
    if not position:
        return 100000
    x, y = position
    return abs(x) + abs(y)


def write_range(p_0: int, p_1: int) -> range:
    if p_1 > p_0:
        return range(p_0, p_1 + 1)
    else:
        return range(p_1, p_0 + 1)


def generate_spots_between_positions(pos1: tuple, pos2: tuple) -> list:
    if pos1 == pos2:
        return []
    x_0, y_0 = pos1
    x_1, y_1 = pos2
    if x_0 == x_1:
        y_range = write_range(y_0, y_1)
        x_range = [x_0] * len(y_range)
    else:
        x_range = write_range(x_0, x_1)
        y_range = [y_0] * len(x_range)
    spots_covered = [(x, y)
                     for x, y in zip(x_range, y_range)
                     ]
    return spots_covered


def get_next_position(current_position: tuple, direction: str, magnitude: int) -> tuple:
    x_0, y_0 = current_position
    if direction == 'R':
        return (x_0+magnitude, y_0)
    elif direction == 'L':
        return (x_0-magnitude, y_0)
    elif direction == 'D':
        return (x_0, y_0-magnitude)
    elif direction == 'U':
        return (x_0, y_0+magnitude)
    raise Exception("Invalid direction")


def trace_path(wire_path: str) -> dict:
    current_position = (0, 0)
    positions = {}
    for direction_and_magnitude in wire_path.split(","):
        direction, magnitude = convert_magnitude_and_direction(
            direction_and_magnitude)

        next_position = get_next_position(
            current_position, direction, magnitude)

        spots_covered = generate_spots_between_positions(
            current_position, next_position)

        for spot in spots_covered:
            positions[spot] = True
        current_position = next_position
    return positions


def convert_magnitude_and_direction(direction_and_magnitude: str) -> tuple:
    direction = direction_and_magnitude[0]
    magnitude = int(direction_and_magnitude[1:])
    return direction, magnitude


def get_wire_crossing(wire_path: str, previous_points: dict) -> tuple:
    current_position = (0, 0)
    position = None
    for direction_and_magnitude in wire_path.split(","):
        direction, magnitude = convert_magnitude_and_direction(
            direction_and_magnitude)

        next_position = get_next_position(
            current_position, direction, magnitude)
        spots_covered = generate_spots_between_positions(
            current_position, next_position)

        for spot in spots_covered:
            if previous_points.get(spot, False):
                if spot != (0, 0) and \
                        get_manhattan_distance(position) > get_manhattan_distance(spot):
                    position = spot
        current_position = next_position
    return position


def get_closest_wire_crossing_from_strings(wire1_path: str, wire2_path: str) -> int:
    wire1_positions = trace_path(wire1_path)
    pos = get_wire_crossing(wire2_path, wire1_positions)
    return pos


class TestDay3(unittest.TestCase):

    def test_step_creation(self):
        path = trace_path("R8,U5,L5,D3")
        self.assertTrue(path[(0, 0)])
        self.assertFalse((-5, 0) in path)
        self.assertTrue(path[(3, 3)])

    def test_generate_spots_between(self):
        spots = generate_spots_between_positions((0, 0), (0, 1))
        self.assertEqual([(0, 0), (0, 1)], spots)

        spots = generate_spots_between_positions((0, 0), (0, -1))
        self.assertEqual([(0, -1), (0, 0)], spots)

        spots = generate_spots_between_positions((0, 0), (1, 0))
        self.assertEqual([(0, 0), (1, 0)], spots)

        spots = generate_spots_between_positions((0, 0), (-1, 0))
        self.assertEqual([(-1, 0), (0, 0)], spots)

        spots = generate_spots_between_positions((0, 0), (-5, 0))
        self.assertEqual([(-5, 0), (-4, 0), (-3, 0),
                          (-2, 0), (-1, 0), (0, 0)], spots)

        spots = generate_spots_between_positions((8, 0), (8, 5))
        self.assertEqual(
            [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5)], spots)

        spots = generate_spots_between_positions((8, 5), (3, 5))
        self.assertEqual(
            [(3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5)], spots)

        spots = generate_spots_between_positions((1, 0), (1, 0))
        self.assertEqual([], spots)

    def test_get_next_pos(self):
        next_pos = get_next_position((3, 5), 'R', 5)
        self.assertEqual((8, 5), next_pos)
        next_pos = get_next_position((3, 5), 'L', 5)
        self.assertEqual((-2, 5), next_pos)
        next_pos = get_next_position((3, 5), 'U', 5)
        self.assertEqual((3, 10), next_pos)
        next_pos = get_next_position((3, 5), 'D', 5)
        self.assertEqual((3, 0), next_pos)

    def test_end_to_end_sample(self):
        result = get_closest_wire_crossing_from_strings(
            "R8,U5,L5,D3", "U7,R6,D4,L4")
        self.assertEqual((3, 3), result)

    def run_wire_crossing_test(self, wire_one: str, wire_two: str, expected_val: int) -> None:
        result_pos = get_closest_wire_crossing_from_strings(wire_one, wire_two)
        result_dis = get_manhattan_distance(result_pos)
        self.assertEqual(expected_val, result_dis)

    def test_sample_1_get_crossing(self):
        wire_one = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
        wire_two = 'U62,R66,U55,R34,D71,R55,D58,R83'
        expected_val = 159
        result_dis = self.run_wire_crossing_test(wire_one, wire_two, expected_val)

    def test_sample_2_get_crossing(self):
        wire_one = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
        wire_two = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
        expected_val = 135
        result_dis = self.run_wire_crossing_test(wire_one, wire_two, expected_val)

    def test_pt_1(self):
        with open('src/input.txt', 'r') as f:
            text = f.read()
        wire_one, wire_two, _ = text.split('\n')
        result_pos = get_closest_wire_crossing_from_strings(wire_one, wire_two)
        result_dis = get_manhattan_distance(result_pos)
        self.assertEqual(6, result_dis)


if __name__ == '__main__':
    unittest.main
