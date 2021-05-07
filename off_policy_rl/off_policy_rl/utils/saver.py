import os
import json
from enum import Enum
from datetime import datetime

import imageio
import numpy as np

from off_policy_rl.utils.types import ActionPose, Pose
from off_policy_rl.utils.episode import Episode

class Saver:
    def __init__(self, path):
        self.path = path
        self.experiment_path = os.path.join(self.path, datetime.now().strftime('%Y.%m.%d_%H:%M:%S'))
        if not os.path.exists(self.experiment_path):
            try:
                os.makedirs(self.experiment_path)
            except OSError as e:
                pass

    def save_image(self, episode: Episode):
        tiff_file = os.path.join(
            self.experiment_path,
            "{}_{}_{}.tiff".format(episode.epoch, episode.episode, episode.id)
        )
        imageio.imwrite(tiff_file, episode.action.image[0])

    def save_episode(self, episode: Episode):
        json_file = os.path.join(
            self.experiment_path,
            "{}_{}_{}.json".format(episode.epoch, episode.episode, episode.id)
        )
        with open(json_file, 'w') as output:
            json.dump(episode, output, indent=4, default=Saver._jsonify_episode)

        self.save_image(episode)

    @classmethod
    def _jsonify_episode(cls, x):
        if isinstance(x, np.int64):
            return int(x)
        if isinstance(x, np.float32):
            return float(x)
        if isinstance(x, np.ndarray):
            return "image"
        if isinstance(x, Enum):
            return x.name
        if isinstance(x, Pose):
            return {'x': x.x, 'y': x.y, 'z': x.z, 'rx': x.rx, 'ry': x.ry, 'rz': x.rz}
        if isinstance(x, ActionPose):
            return {'x': x.x, 'y': x.y, 'rz': x.rz, 'd': x.d}
        return x.__dict__
