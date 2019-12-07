import os
import unittest
import copy


def process_opcode(index: int, opcode_list: list) -> bool:
    operation = opcode_list[index]
    if operation == 99:
        return True
    input_one_loc = opcode_list[index+1]
    input_two_loc = opcode_list[index+2]
    input_one = opcode_list[input_one_loc]
    input_two = opcode_list[input_two_loc]
    location = opcode_list[index+3]
    if operation == 1:
        opcode_list[location] = input_one + input_two
        return False
    elif operation == 2:
        opcode_list[location] = input_one * input_two
        return False
    else:
        raise Exception()


def process_opcode_list(opcode_list: list) -> list:
    should_stop = False
    index = 0
    while not should_stop:
        should_stop = process_opcode(index, opcode_list)
        index += 4
    return opcode_list


def parse_file(file_name: str) -> list:
    with open('src/input.txt', 'r') as f:
        contents = f.read()
        return [int(i) for i in contents.split(',')]


def try_different_permutations(file_name: str) -> int:
    opcode_list_original = parse_file(file_name)
    for i in range(0, 99):
        for j in range(0, 99):
            opcode_list = copy.copy(opcode_list_original)
            opcode_list[1] = i
            opcode_list[2] = j
            result = process_opcode_list(opcode_list)
            first_val = result[0]
            if first_val == 19690720:
                return 100*i + j
    return 0


class TestOpcodeProcessing(unittest.TestCase):

    def run_process_test(self, opcodes, expected_opcodes, expected_should_stop=False):
        should_stop = process_opcode(0, opcodes)
        self.assertFalse(should_stop)
        self.assertEqual(opcodes, expected_opcodes)

    def test_basic_opcode_processing(self):
        self.run_process_test([1, 0, 0, 0], [2, 0, 0, 0])

    def test_basic_opcode_processing_2(self):
        self.run_process_test([2, 3, 0, 3, 99], [2, 3, 0, 6, 99])

    def test_basic_opcode_processing_3(self):
        self.run_process_test([2, 4, 4, 5, 99, 0],
                              [2, 4, 4, 5, 99, 9801])

    def test_running_opcode_list(self):
        result = process_opcode_list([1, 9, 10, 3,
                                      2, 3, 11, 0,
                                      99,
                                      30, 40, 50])
        self.assertEqual(result, [3500, 9, 10, 70,
                                  2, 3, 11, 0,
                                  99,
                                  30, 40, 50])

    def test_read_file_problem(self):
        result = parse_file('src/input.txt')
        self.assertEqual(result[0], 1)
        self.assertEqual(result[3], 3)

    def test_full_pt1(self):
        opcode_list = parse_file('src/input.txt')
        opcode_list[1] = 12
        opcode_list[2] = 2

        result = process_opcode_list(opcode_list)
        self.assertEqual(3166704, opcode_list[0])

    def test_full_pt2(self):
        result = try_different_permutations('src/input.txt')
        self.assertEqual(8018, result)


if __name__ == '__main__':
    unittest.main()
