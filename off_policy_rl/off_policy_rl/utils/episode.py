# Copyright (c) 2021, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# Author: Nicolai Anton Lynnerup <nily@dti.dk>

from datetime import datetime
from typing import List

from off_policy_rl.rl.action import Action, ActionType
from off_policy_rl.utils.bin import Bin

class Episode:
    def __init__(self, epoch: int, episode: int):
        self.epoch = epoch
        self.episode = episode
        self.id = datetime.now().strftime('%Y.%m.%d_%H:%M:%S')
        self.action: Action
        self.reward: float = 0.0

    def set_reward(self, reward: float) -> None:
        self.reward = reward

    def set_action(self, action: Action) -> None:
        self.action = action

class EpisodeHistory:
    def __init__(self):
        self.data: List[Episode] = []

    def append(self, element: Episode):
        self.data.append(element)

    def iterate_episodes(self, filter_cond=None, stop_cond=None):
        for e in self.data[::-1]:
            if not e.action:
                continue
            if stop_cond and stop_cond(e):
                break
            if filter_cond and not filter_cond(e):
                continue
            yield e.action

    def failed_grasps_since_last_success_in_bin(self, current_bin: Bin):
        tmp = sum(1 for _ in self.iterate_episodes(
            filter_cond=lambda e: e.action.type == ActionType.Grasp and e.reward == 0.0,
            stop_cond=lambda e: e.action.bin.id is not current_bin.id or e.reward == 1.0,
        ))
        print(tmp)
        return tmp
        #return sum(1 for _ in self.iterate_episodes(
        #    filter_cond=lambda e: e.action.type == ActionType.Grasp and e.reward == 0.0,
        #    stop_cond=lambda e: e.action.bin.id is not current_bin.id or e.reward == 1.0,
        #))
