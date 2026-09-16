"""Emphasize extrema only inside caller-declared, same-metric groups."""
import re
from fractions import Fraction


def metric_value(value):
    """Read the mean/rate from a supported display cell, never its uncertainty."""
    raw = str(value).strip()
    fraction = re.fullmatch(r'(\d+)\s*/\s*(\d+)(?:\s*\([\d.]+%\))?', raw)
    if fraction:
        numerator, denominator = map(int, fraction.groups())
        if denominator == 0:
            raise ValueError('Zero denominator')
        return Fraction(numerator, denominator)
    scalar = re.fullmatch(r'\$?(-?\d+(?:\.\d+)?)(?:\s*±\s*\d+(?:\.\d+)?)?([%k]?)', raw)
    if not scalar:
        raise ValueError(f'Unsupported metric cell: {raw!r}')
    mean, unit = scalar.groups()
    return Fraction(mean) * {'': 1, '%': Fraction(1, 100), 'k': 1000}[unit]


def best_cells(rows, comparisons):
    """Return zero-based body-cell coordinates, retaining every exact tie."""
    selected = set()
    for coordinates, direction in comparisons:
        if not coordinates or direction not in ('max', 'min'):
            raise ValueError('A comparison needs cells and an explicit max/min direction')
        values = {tuple(coord): metric_value(rows[coord[0]][coord[1]]) for coord in coordinates}
        extreme = (max if direction == 'max' else min)(values.values())
        selected.update(coord for coord, value in values.items() if value == extreme)
    return selected


def row_maxima(rows, columns):
    return [([(r, c) for c in columns], 'max') for r in range(len(rows))]


def column_extrema(rows, directions, row_indices=None):
    indices = range(len(rows)) if row_indices is None else row_indices
    return [([(r, c) for r in indices], direction) for c, direction in directions]
