import unittest
from app import checkPassword


class TestCheckPassword(unittest.TestCase):
    def test_length_less_than_8_is_TooShort(self):
        expectedResult: str = "TooShort"
        result: str = checkPassword("Pass")
        self.assertEqual(expectedResult, result)

    def test_length_equals_8_contains_upper_lower_is_Weak(self):
        expectedResult: str = "Weak"
        result: str = checkPassword("PassPass")
        self.assertEqual(expectedResult, result)

    def test_length_greater_8_contains_only_upper_lower_is_Weak(self):
        expectedResult: str = "Weak"
        result: str = checkPassword("PassPassPass")
        self.assertEqual(expectedResult, result)

    def test_length_greater_8_contains_only_special_is_Weak(self):
        expectedResult: str = "Weak"
        result: str = checkPassword("!@#$%^&*!@")
        self.assertEqual(expectedResult, result)

    def test_length_greater_8_contains_only_digit_is_Weak(self):
        expectedResult: str = "Weak"
        result: str = checkPassword("1234567890")
        self.assertEqual(expectedResult, result)

    def test_length_greater_8_contains_upper_lower_special_is_Medium(self):
        expectedResult: str = "Medium"
        result: str = checkPassword("PassPass@")
        self.assertEqual(expectedResult, result)

    def test_length_greater_8_contains_upper_lower_digit_is_Medium(self):
        expectedResult: str = "Medium"
        result: str = checkPassword("PassPass9")
        self.assertEqual(expectedResult, result)

    def test_length_greater_8_contains_special_digit_is_Medium(self):
        expectedResult: str = "Medium"
        result: str = checkPassword("123456!@#$%")
        self.assertEqual(expectedResult, result)

    def test_length_greater_8_contains_upper_lower_special_digit_is_Strong(self):
        expectedResult: str = "Strong"
        result: str = checkPassword("Pass1234!@#$")
        self.assertEqual(expectedResult, result)
