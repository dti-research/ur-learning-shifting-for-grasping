class Saver:
    def __init__(self, path):
        self.path = path

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
        if isinstance(x, RobotPose):
            return {'x': x.x, 'y': x.y, 'z': x.z, 'a': x.a, 'b': x.b, 'c': x.c, 'd': x.d}
        if isinstance(x, Affine):
            return {'x': x.x, 'y': x.y, 'z': x.z, 'a': x.a, 'b': x.b, 'c': x.c}
        return x.__dict__
