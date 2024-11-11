from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt

from blue_objects import file
from blue_objects.graphics.signature import justify_text


def log_image_hist(
    image: np.ndarray,
    range: Tuple[float],
    header: List[str],
    footer: List[str],
    filename: str,
    line_width: int = 80,
    bins: int = 64,
) -> bool:
    plt.figure(figsize=(10, 6))
    plt.hist(
        image.ravel(),
        bins=bins,
        range=range,
    )
    plt.title(
        justify_text(
            " | ".join(header),
            line_width=line_width,
            return_str=True,
        )
    )
    plt.xlabel(
        justify_text(
            " | ".join(footer),
            line_width=line_width,
            return_str=True,
        )
    )
    plt.ylabel("frequency")
    plt.grid(True)

    return file.save_fig(filename, log=True)
