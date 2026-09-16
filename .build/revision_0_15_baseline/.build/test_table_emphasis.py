"""Tests for descriptive table emphasis, not statistical significance."""
import unittest
from fractions import Fraction

from table_emphasis import best_cells, metric_value


class TableEmphasisTests(unittest.TestCase):
    def test_displayed_values(self):
        self.assertEqual(metric_value('19 / 20'), metric_value('95%'))
        self.assertEqual(metric_value('24 / 50 (48%)'), metric_value('48%'))
        self.assertEqual(metric_value('$2.62'), Fraction('2.62'))
        self.assertEqual(metric_value('49.1 ± 24.9%'), Fraction('.491'))
        self.assertEqual(metric_value('9.3 ± 2.6k'), 9300)

    def test_ties_and_minima(self):
        rows = [['a', '2/20', '$4.00'], ['b', '2/20', '$2.00']]
        self.assertEqual(best_cells(rows, [([(0, 1), (1, 1)], 'max'),
                                          ([(0, 2), (1, 2)], 'min')]),
                         {(0, 1), (1, 1), (1, 2)})

    def test_excludes_oracle_and_sample_count(self):
        rows = [['A', 36, 20], ['B', 76, 20], ['Oracle', 100, 20]]
        self.assertEqual(best_cells(rows, [([(0, 1), (1, 1)], 'max')]), {(1, 1)})

    def test_invalid_metric_fails_closed(self):
        for value in ['Baseline', 'NaN', 'Infinity', '1/0', '20 apples', '']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                metric_value(value)

    def test_invalid_group_fails_closed(self):
        for group in [([], 'max'), ([(0, 0)], 'largest')]:
            with self.assertRaises(ValueError):
                best_cells([[1]], [group])


if __name__ == '__main__':
    unittest.main()
