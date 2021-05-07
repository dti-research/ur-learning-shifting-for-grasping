from typing import List

from off_policy_rl.config.config import Config
from off_policy_rl.utils.bin import Bin
from off_policy_rl.utils.types import Pose


class Environment:
    def __init__(self, bins: List[Bin]):
        assert len(bins) == 2
        self.bins = bins
        #self.current_bin = Config.current_bin
        self.pick_bin = Config.start_bin
        self.drop_bin = int(not self.pick_bin)

    def switch_bins(self):
        self.pick_bin = int(not self.pick_bin)
        self.drop_bin = int(not self.pick_bin)

    def get_pick_bin(self) -> Bin:
        return self.bins[self.pick_bin]

    def get_drop_bin(self) -> Bin:
        return self.bins[self.drop_bin]
