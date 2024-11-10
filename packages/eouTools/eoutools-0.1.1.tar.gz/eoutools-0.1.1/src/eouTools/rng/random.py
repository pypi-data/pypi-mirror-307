import random
from contextlib import contextmanager, asynccontextmanager
from typing import Optional

try:
    import numpy as np
except ImportError as _:
    np = None

@contextmanager
def seed(a: Optional[int | float | str | bytes | bytearray] = None):
    """To be used as a context manager
    Example:
    with seed(23):
        ...

    :param a: The seed you want to use (if not provided, a random one will be generated using random.uniform)"""

    if not a:
        if np:
            a = np.random.uniform(-1, 1)
        else:
            a = random.uniform(-1, 1)

    random.seed(a)
    if np:
        np.random.seed(a)
    yield
    random.seed()
    if np:
        np.random.seed()

@asynccontextmanager
async def aseed(a: Optional[int | float | str | bytes | bytearray] = None):
    """To be used as an asynchronous context manager
    Example:
    async with aseed(23):
        ...

    :param a: The seed you want to use (if not provided, a random one will be generated using random.uniform)"""

    if not a:
        if np:
            a = np.random.uniform(-1, 1)
        else:
            a = random.uniform(-1, 1)

    random.seed(a)
    if np:
        np.random.seed(a)
    yield
    random.seed()
    if np:
        np.random.seed()
