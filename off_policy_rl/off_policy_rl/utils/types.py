#from dataclasses import dataclass
from typing import Callable, Union

import numpy as np

# 8-bit images
RGB8BitImgT = np.ndarray
RGBA8BitImgT = np.ndarray
BGR8BitImgT = np.ndarray
BGRA8BitImgT = np.ndarray
Grayscale8BitImgT = np.ndarray
Any8BitImgT = Union[RGB8BitImgT, RGBA8BitImgT, BGR8BitImgT, BGRA8BitImgT, Grayscale8BitImgT]
Any8BitColorImgT = Union[RGB8BitImgT, RGBA8BitImgT, BGR8BitImgT, BGRA8BitImgT]
RGBOrGrayscaleBitImgT = Union[RGB8BitImgT, Grayscale8BitImgT]

# Rectification Function Type
RectificationFunctionT = Callable[[Any8BitImgT], Any8BitImgT]

#@dataclass
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
    """Angle-axis rotations
    """
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
