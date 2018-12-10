import setup
setup.setup()

import unittest
from fauxit.model.level import Level
from fauxit.model.level_name_validator import LevelNameValidator

class LevelNameValidatorShowTest(unittest.TestCase):
    def test_upper_letters(self):
        name = "FOOBAR"
        self.assertTrue(LevelNameValidator.validate(name, Level.show))

    def test_contains_number(self):
        self.assertTrue(LevelNameValidator.validate("FO10P", Level.show))

    def test_show_lower(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("foobar", Level.show)

    def test_starts_with_number(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("1FOOBAR", Level.show)

    def test_ends_with_number(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOOBAR1", Level.show)

    def test_contains_underscore(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOO_BAR", Level.show)

    def test_contains_dash(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOO-BAR", Level.show)

    def test_contains_period(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOO.BAR", Level.show)

    def test_contains_space(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOO BAR", Level.show)

class LevelNameValidatorSequenceTest(unittest.TestCase):

    def test_upper_letters(self):
        self.assertTrue(LevelNameValidator.validate("RD", Level.sequence))

    def test_seq_contains_number(self):
        self.assertTrue(LevelNameValidator.validate("RD1", Level.sequence))

    def test_single_letter_upper(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("R", Level.sequence)

    def test_seq_lower(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("foobar", Level.sequence)

    def test_seq_starts_with_number(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("1RD", Level.sequence)

    def test_seq_number_after_first_letter(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("R1RD", Level.sequence)

    def test_contains_underscore(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOO_BAR", Level.sequence)

    def test_contains_dash(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOO-BAR", Level.sequence)

    def test_contains_period(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOO.BAR", Level.sequence)

    def test_contains_space(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOO BAR", Level.sequence)

class LevelNameValidatorShotTest(unittest.TestCase):

    def test_numbers(self):
        self.assertTrue(LevelNameValidator.validate("0001", Level.shot))

    def test_starts_with_number(self):
        self.assertTrue(LevelNameValidator.validate("0FOO", Level.shot))

    def test_starts_with_letter(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("A1000",Level.shot)

    def test_number_letter_lowercase(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("0a", Level.shot)

    def test_number_after_first_letter(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("R1RD", Level.shot)

    def test_contains_underscore(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOO_BAR", Level.shot)

    def test_contains_dash(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOO-BAR", Level.shot)

    def test_contains_period(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOO.BAR", Level.shot)

    def test_contains_space(self):
        with self.assertRaises(KeyError):
            LevelNameValidator.validate("FOO BAR", Level.shot)


if __name__ == '__main__':
    unittest.main()