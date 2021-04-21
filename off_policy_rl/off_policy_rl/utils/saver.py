import os
from enum import Enum

import numpy as np

from off_policy_rl.utils.types import ActionPose, Pose

class Saver:
    def __init__(self, path):
        self.path = path
        self.experiment_path = os.join(self.path, )

    def save_image(self):
        raise NotImplementedError()

    def save_episode(self):
        raise NotImplementedError()

    @classmethod
    def _jsonify_episode(cls, x):
        if isinstance(x, np.int64):
            return int(x)
        if isinstance(x, np.float32):
            return float(x)
        if isinstance(x, Enum):
            return x.name
        if isinstance(x, Pose):
            return {'x': x.x, 'y': x.y, 'z': x.z, 'rx': x.rx, 'ry': x.ry, 'rz': x.rz}
        if isinstance(x, ActionPose):
            return {'x': x.x, 'y': x.y, 'rz': x.rz, 'd': x.d}
        return x.__dict__
