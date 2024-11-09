from funcnodes_core import Shelf
from .logic import NODE_SHELF as logic_shelf
from .math_nodes import NODE_SHELF as math_shelf
from .lists import NODE_SHELF as lists_shelf
from .strings import NODE_SHELF as strings_shelf
from .dicts import NODE_SHELF as dicts_shelf


__version__ = "0.1.11"

NODE_SHELF = Shelf(
    nodes=[],
    subshelves=[
        lists_shelf,
        dicts_shelf,
        strings_shelf,
        math_shelf,
        logic_shelf,
    ],
    name="basics",
    description="basic functionalities",
)
