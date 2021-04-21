from typing import List

from off_policy_rl.utils.types import Pose

class Bin:
    def __init__(self,
                 size: List[float],
                 frame: Pose):
        self.size = size
        self.frame = frame
