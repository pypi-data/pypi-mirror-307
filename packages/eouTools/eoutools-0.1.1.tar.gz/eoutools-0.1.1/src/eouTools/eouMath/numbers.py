import math
from functools import cached_property

@lambda _: _()
class NaturalNumbers:
    def __init__(self):
        pass

    def __contains__(self, item: int):
        if isinstance(item, complex):
            if item.imag != 0:
                return False
            item = item.real
        return item >= 0 and item % 1 == 0

@lambda _: _()
class WholeNumbers:
    def __init__(self):
        pass

    def __contains__(self, item: int):
        if isinstance(item, complex):
            if item.imag != 0:
                return False
            item = item.real
        return item % 1 == 0

@lambda _: _()
class PositiveWholeNumbers:
    def __init__(self):
        pass

    def __contains__(self, item: int):
        if isinstance(item, complex):
            if item.imag != 0:
                return False
            item = item.real
        return item % 1 == 0 and item > 0

@lambda _: _()
class NegativeWholeNumbers:
    def __init__(self):
        pass

    def __contains__(self, item: int):
        if isinstance(item, complex):
            if item.imag != 0:
                return False
            item = item.real
        return item % 1 == 0 and item < 0

@lambda _: _()
class RealNumbers:
    def __init__(self):
        pass

    def __contains__(self, item: int):
        if isinstance(item, complex):
            if item.imag != 0:
                return False
            item = item.real
        return True

@lambda _: _()
class PositiveRealNumbers:
    def __init__(self):
        pass

    def __contains__(self, item: int):
        if isinstance(item, complex):
            if item.imag != 0:
                return False
            item = item.real
        if item > 0:
            return True
        return False

@lambda _: _()
class NegativeRealNumbers:
    def __init__(self):
        pass

    def __contains__(self, item: int):
        if isinstance(item, complex):
            if item.imag != 0:
                return False
            item = item.real
        if item < 0:
            return True
        return False

@lambda _: _()
class ComplexNumbers:
    def __init__(self):
        pass

    def __contains__(self, item: int | complex):
        if not isinstance(item, complex):
            item = complex(item, 0)

        return True


class squareRoot:
    def __init__(self, number):
        self._number = number

    @cached_property
    def result(self):
        return math.sqrt(self._number)  # Calculates and caches the result

    @property
    def value(self):
        """Equivalent to squareRoot.result"""
        return self.result

    @cached_property
    def to_str(self):
        return str(self.result)

    @cached_property
    def rounded(self):
        return round(self.result)

    def __get__(self, instance, owner):
        return self.result

    def __float__(self):
        return self.result

    def __int__(self):
        return self.rounded

    def __str__(self):
        return self.to_str

    def __repr__(self):
        return self.to_str

    def __eq__(self, other):
        if isinstance(other, squareRoot):
            return self.value == other.value
        else:
            return self.value == float(other)

    def __lt__(self, other):
        if isinstance(other, squareRoot):
            return self.value < other.value
        else:
            return self.value < float(other)

    def __le__(self, other):
        if isinstance(other, squareRoot):
            return self.value <= other.value
        else:
            return self.value <= float(other)

    def __gt__(self, other):
        if isinstance(other, squareRoot):
            return self.value > other.value
        else:
            return self.value > float(other)

    def __ge__(self, other):
        if isinstance(other, squareRoot):
            return self.value >= other.value
        else:
            return self.value >= float(other)
