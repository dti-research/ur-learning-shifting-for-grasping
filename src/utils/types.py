from typing import Callable

import numpy as np

ImageT = np.ndarray  # currently RGB color image
RectificationFunctionT = Callable[[ImageT], ImageT]
