import numpy as np


class TranspositionTable:
    """
    Transposition table implemented as a fixed-size hash map
    Uses 56-bit keys and 8-bit values (non-zero)
    """

    def __init__(self, size):
        assert size > 0
        self.size = size
        self.T = np.zeros(size, dtype=[('key', np.uint64), ('val', np.int16)])  # Structured NumPy array

    def reset(self):
        """Resets the transposition table."""
        self.T.fill((0, 0))  # Zero out both key and value

    def put(self, key, val):
        """Stores a non-null 8-bit value for a 56-bit key."""
        assert key < (1 << 56)
        index = key % self.size
        self.T[index] = (key, val)

    def get(self, key):
        """Retrieves the value associated with a key, or 0 if not found."""
        assert key < (1 << 56)
        index = key % self.size
        entry = self.T[index]
        return entry['val'] if entry['key'] == key else 0
