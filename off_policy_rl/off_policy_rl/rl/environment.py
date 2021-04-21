from typing import List

from off_policy_rl.config.config import Config
from off_policy_rl.utils.bin import Bin
from off_policy_rl.utils.types import Pose


class Environment:
    def __init__(self, bins: List[Bin]):
        self.bins = bins
        self.current_bin = Config.current_bin

    def get_current_bin(self) -> Bin:
        return self.bins[self.current_bin]

    def set_current_bin(self, index: int) -> None:
        self.current_bin = index
