from typing import Dict, List, Tuple


class LEDMatrix:
    def __init__(self, matrix=None):
        # Initialize a dictionary to store only columns with LEDs that are on
        # self.matrix: Dict[str, List[int]] = matrix or {}
        # {"on": {"0": [1,7]}, "off": {"1": [2,3,4,5,6]}}
        self.matrix: Dict[str, Dict[str, List[int]]] = matrix or {}

    def serialize_to_bitmask(self) -> Dict[str, List[Tuple[int, int]]]:
        """
        Serializes the matrix to a list of size 8, where each entry is an 8-bit integer.
        The index of the list is the column, and the value at each index represents the state of the rows within that column, where each bit corresponds to the row state1 (1 = on, 0 = off).
        """
        on = []
        for column, rows in self.matrix.get("on", {}).items():
            # Convert the list of rows into an 8-bit integer
            num = 0
            for row in rows:
                num |= (1 << (7-row))  # Set the appropriate bit to 1. We use 7-row to invert the row order so it displays on the LEDs correctly
            on.append((int(column), num))
        
        off = []
        for column, rows in self.matrix.get("off", {}).items():
            # Convert the list of rows into an 8-bit integer
            num = 0
            for row in rows:
                num |= (1 << (7-row))  # Set the appropriate bit to 1
            off.append((int(column), num))
        
        return {"on": on, "off": off}

    def pretty_print(self) -> str:
        """
        Prints a pretty ASCII art representation of the LED matrix.
        LEDs that are 'on' are represented by '#', and LEDs that are 'off' are represented by '.'.
        """
        # Initialize an empty 8x8 grid with '*' as default
        grid = [['*' for _ in range(8)] for _ in range(8)]

        # Place '#' for specified positions in "on" and "off"
        for col, rows in self.matrix["on"].items():
            for row in rows:
                grid[row][int(col)] = '#'

        # Generate the string output
        output = '\n'.join(' '.join(row) for row in grid)
        return output

    def __repr__(self):
        return f"LEDMatrix({self.matrix})"
    

m = LEDMatrix({"on": {"0": [1,7]}, "off": {"1": [2,3,4,5,6]}})
print(m.serialize_to_bitmask())
print(m.pretty_print())