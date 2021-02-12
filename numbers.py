#!/usr/bin/env python3

"""
Script to print numbers from 1 to X in alphabetical order
"""

import argparse
import unittest

DEFAULT_MAX = 100

SMALL = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = [None, None, "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

def number_to_word(number):
    if number < len(SMALL):
        return SMALL[number]
    digits = list(reversed([int(x) for x in str(number)]))
    if number < 100:
        if digits[0] == 0:
            return TENS[digits[1]]
        return "%s %s" % (TENS[digits[1]], SMALL[digits[0]])
    if number < 1000:
        two_digits = 10 * digits[1] + digits[0]
        hundred = SMALL[digits[2]] + " hundred"
        if two_digits == 0:
            return hundred
        return "%s %s" % (hundred, number_to_word(two_digits))
    if number < 1_000_000:
        three_digits = 100 * digits[2] + 10 * digits[1] + digits[0]
        thousands = digits[3]
        if len(digits) > 4:
            thousands = thousands + digits[4] * 10
        if len(digits) > 5:
            thousands = thousands + digits[5] * 100
        thousands_string = "%s thousand" % number_to_word(thousands)
        if three_digits == 0:
            return thousands_string


    raise ValueError("Unexpected number %s" % (number,))

def run_tests():
    """
    Tests
    """

    class Tester(unittest.TestCase):

        def one_test(self, number, expected_word):
            actual_word = number_to_word(number)
            self.assertEqual(expected_word, actual_word)

        def test_small(self):
            self.one_test(0, "zero")
            self.one_test(2, "two")
            self.one_test(7, "seven")
            self.one_test(9, "nine")
            self.one_test(15, "fifteen")

        def test_tens(self):
            self.one_test(20, "twenty")
            self.one_test(21, "twenty one")
            self.one_test(35, "thirty five")
            self.one_test(99, "ninety nine")

        def test_hundreds(self):
            self.one_test(100, "one hundred")
            self.one_test(500, "five hundred")
            self.one_test(520, "five hundred twenty")
            self.one_test(329, "three hundred twenty nine")

        def test_thousand(self):
            self.one_test(1000, "one thousand")
            self.one_test(4000, "four thousand")
            self.one_test(45000, "forty five thousand")
            self.one_test(451000, "four hundred fifty one thousand")

    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(Tester))

def show(max_number):
    numbers = [number_to_word(x) for x in range(1, max_number+1)]
    for number in sorted(numbers):
        print(number)


def main():


    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["test", "show"])
    parser.add_argument("--max-number", type=int)
    args = parser.parse_args()

    max_number = args.max_number
    if max_number is None:
        max_number = DEFAULT_MAX
    
    if args.action == "test":
        run_tests()
    elif args.action == "show":
        show(max_number)
    else:
        raise ValueError("Unexpected action %s" % (args.action))

if __name__ == "__main__":
    main()
