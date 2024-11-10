from typing import Callable

def bubble_sort(data: list, compare: Callable[[int, int], bool] = lambda x, y: x > y, /, reverse: bool = False):
    def helper(a: bool, b: bool):
        if b:
            return not a
        return a
    while True:
        changes = 0
        for i, item in enumerate(data):
            if i + 1 == len(data):
                continue

            if helper(compare(item, data[i + 1]), reverse):
                data[i], data[i + 1] = data[i + 1], item
                changes += 1
        if changes == 0:
            return data
