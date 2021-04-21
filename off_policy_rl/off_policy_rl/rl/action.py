from enum import Enum

from off_policy_rl.rl.environment import Environment, Bin

from off_policy_rl.utils.types import ActionPose
from off_policy_rl.utils.selection_method import SelectionMethod

ActionType = Enum('ActionType', [
    'Grasp',
    'Shift',
])

class Action:
    def __init__(self,
                 action: ActionType,
                 bin: Bin,
                 pose: ActionPose,
                 method: SelectionMethod,
                 image # TODO: Make to CV2.mat
                 ):
        self.type = action
        self.bin = bin
        self.pose = pose
        self.method = method
        self.image = image
        self.estimated_reward = None
