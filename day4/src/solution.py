import unittest
from typing import Callable


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


def is_number_valid_pt2_criteria(number: str) -> bool:
    if len(number) == 6:  # It is a six-digit number.
        two_adjacent_digits_same = False
        previous_int = None
        twice_previous_int = None
        repeated_int_found = False
        for i in map(int, number):
            if previous_int:
                # Going from left to right, the digits never decrease
                previous_is_equal = previous_int == i
                twice_prev_is_equal = twice_previous_int == i
                # # the two adjacent matching digits are not part of a larger group of matching digits.
                # print(
                #     f"twice_prev_int={twice_previous_int},previous_int={previous_int},current={i}")
                # print(
                #     f"repeated_int_found={repeated_int_found},previous_is_equal={previous_is_equal},twice_prev_is_equal={twice_prev_is_equal}")

                if i < previous_int:
                    # print("num decreased")
                    return False
                if repeated_int_found:
                    pass
                elif previous_is_equal and twice_prev_is_equal:
                    two_adjacent_digits_same = False
                # Two adjacent digits are the same (like 22 in 122345).
                elif previous_is_equal:
                    two_adjacent_digits_same = True
                elif two_adjacent_digits_same:
                    repeated_int_found = True

            twice_previous_int = previous_int
            previous_int = i
        return two_adjacent_digits_same
    return False


def get_valid_pws_count(min_range: int, max_range: int, validator: Callable) -> int:
    return len(get_valid_pws(min_range, max_range, validator))


def get_valid_pws(min_range: int, max_range: int, validator: Callable) -> list:
    return [i for i in range(min_range, max_range + 1) if validator(str(i))]


class TestDay4(unittest.TestCase):

    def test_first_num(self):
        self.assertTrue(is_number_valid('111111'))

    def test_second_num(self):
        self.assertFalse(is_number_valid('223450'))

    def test_third_num(self):
        self.assertFalse(is_number_valid('123789'))

    def test_get_passing_numbers_pt1(self):
        count = get_valid_pws_count(402328, 864247, is_number_valid)
        self.assertEqual(count, 454)

    def test_pt2_first_num(self):
        self.assertTrue(is_number_valid_pt2_criteria('112233'))

    def test_pt2_second_num(self):
        self.assertFalse(is_number_valid_pt2_criteria('123444'))

    def test_pt2_second_and_a_half_num(self):
        self.assertFalse(is_number_valid_pt2_criteria('444123'))

    def test_pt2_third_num(self):
        self.assertTrue(is_number_valid_pt2_criteria('111122'))

    def test_pt2_third_num(self):
        self.assertTrue(is_number_valid_pt2_criteria('445666'))

    def test_pt2_third_num(self):
        self.assertFalse(is_number_valid_pt2_criteria('447989'))

    def test_compare_diff_pt2(self):
        li1 = get_valid_pws(
            402328, 864247, is_number_valid)
        li2 = get_valid_pws(
            402328, 864247, is_number_valid_pt2_criteria)
        # print(f"first_list={len(li1)},second_list={len(li2)}")
        # for i in (list(set(li2) - set(li1))):
        #     print(i)

    def test_pt2_etoe(self):
        answer = get_valid_pws_count(
            402328, 864247, is_number_valid_pt2_criteria)
        self.assertEqual(answer, 288)


if __name__ == '__main__':
    unittest.main()
