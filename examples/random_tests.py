import random
import unittest

from fluenttest import test_case


class WhenShufflingSequence(test_case.TestCase, unittest.TestCase):
    @classmethod
    def arrange(cls):
        super(WhenShufflingSequence, cls).arrange()
        cls.input_sequence = list(range(10))
        cls.result_sequence = cls.input_sequence[:]

    @classmethod
    def act(cls):
        random.shuffle(cls.result_sequence)

    def test_should_not_loose_elements(self):
        self.assertEqual(sorted(self.result_sequence),
                         sorted(self.input_sequence))


class WhenShufflingImmutableSequence(test_case.TestCase, unittest.TestCase):
    allowed_exceptions = TypeError

    @classmethod
    def act(cls):
        random.shuffle((1, 2, 3))

    def test_should_raise_type_error(self):
        self.assertIsInstance(self.exception, TypeError)


class WhenSelectingARandomElement(test_case.TestCase, unittest.TestCase):
    @classmethod
    def arrange(cls):
        super(WhenSelectingARandomElement, cls).arrange()
        cls.sequence = list(range(10))

    @classmethod
    def act(cls):
        cls.selected = random.choice(cls.sequence)

    def test_should_retrieve_an_element_from_sequence(self):
        self.assertIn(self.selected, self.sequence)


class WhenSamplingASequence(test_case.TestCase, unittest.TestCase):
    @classmethod
    def arrange(cls):
        super(WhenSamplingASequence, cls).arrange()
        cls.sequence = list(range(10))

    @classmethod
    def act(cls):
        cls.result = random.sample(cls.sequence, 5)

    def test_should_retrieve_elements_from_sequence(self):
        self.assertTrue(all(elm in self.sequence for elm in self.result))


class WhenAskingForLargeSample(test_case.TestCase, unittest.TestCase):
    allowed_exceptions = ValueError

    @classmethod
    def arrange(cls):
        super(WhenAskingForLargeSample, cls).arrange()
        cls.sequence = list(range(10))

    @classmethod
    def act(cls):
        cls.result = random.sample(cls.sequence, 20)

    def test_should_raise_value_error(self):
        self.assertIsInstance(self.exception, ValueError)


if __name__ == '__main__':
    unittest.main(verbosity=2)
