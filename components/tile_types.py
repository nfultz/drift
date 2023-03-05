from typing import Tuple

import numpy as np  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark), dtype=tile_dt)


empty = new_tile(
    walkable=False, transparent=True, dark=(ord(" "), (255, 255, 255), (0, 0, 0)),
)
error = new_tile(
    walkable=False, transparent=True, dark=(ord(" "), (255, 255, 255), (255, 0, 0)),
)
nontraversable = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (110, 110, 30)),
)
desert = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (150, 150, 50)),
)
unique = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (150, 150, 150)),
)
settlement = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
)
explorable = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (180, 70, 180)),
)

