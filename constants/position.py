

# I'm really not sure about the enums in Python. Makes getting the values really long-winded (enum.name.value)
#   Experimenting with a regular class with constants instead
class Position:
    """Position on the grid"""
    TOP_LEFT = 0
    TOP_EDGE = 1
    TOP_RIGHT = 2
    LEFT_EDGE = 3
    CENTER = 4
    RIGHT_EDGE = 5
    BOTTOM_LEFT = 6
    BOTTOM_EDGE = 7
    BOTTOM_RIGHT = 8
