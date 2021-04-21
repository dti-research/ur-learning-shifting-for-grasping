from typing import Callable

import numpy as np

ImageT = np.ndarray  # currently RGB color image
RectificationFunctionT = Callable[[ImageT], ImageT]

class ActionPose:
    def __init__(self,
                 x:  float,
                 y:  float,
                 rz: float,
                 d:  int
    ):
        self.x = x
        self.y = y
        self.rz = rz
        self.d = d

class Pose:
    def __init__(self,
                 x:  float,
                 y:  float,
                 z:  float,
                 rx: float,
                 ry: float,
                 rz: float
    ):
        self.x  = x
        self.y  = y
        self.z  = z
        self.rx = rx
        self.ry = ry
        self.rz = rz
