import unittest


def is_number_valid(number: str) -> bool:
    if len(number) == 6:  # It is a six-digit number.
        two_adjacent_digits_same = False
        previous_int = None
        for i in map(int, number):
            if previous_int:
                # Going from left to right, the digits never decrease
                if i < previous_int:
                    return False
                # Two adjacent digits are the same (like 22 in 122345).
                if previous_int == i:
                    two_adjacent_digits_same = True
            previous_int = i
        return two_adjacent_digits_same
    return False


class TestDay4(unittest.TestCase):

    def test_first_num(self):
        self.assertTrue(is_number_valid('111111'))

    def test_second_num(self):
        self.assertFalse(is_number_valid('223450'))

    def test_second_num(self):
        self.assertFalse(is_number_valid('123789'))

    def test_get_passing_numbers_pt1(self):
        count = 0
        for i in range(402328, 864247 + 1):
            if is_number_valid(str(i)):
                count += 1
        self.assertEqual(count, 454)


if __name__ == '__main__':
    unittest.main()
