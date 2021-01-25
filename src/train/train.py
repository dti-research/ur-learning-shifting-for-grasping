# Copyright (c) 2021, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# Author: Nicolai Anton Lynnerup <nily@dti.dk>

import tensorflow as tf

from model import Model

tf.random.set_seed(42)

class Train():
    def __init__(self):
        self.test = 1

    def run(self):
        """

        Change bin if 12 grasp attempts fails in a row

        Hyperparameters:

                        Parameter:          Value:      Notes:
        Manipulator:    Image distance      0.35m       Distance to workplane when taking image(?)
                        Approach distance   0.12m
                        Grasp Z offset      0.015m
                        Gripper force       20N
        Learning:       Optimizer           Adam
                        - Initial LR        1e-4
                        Epochs              5000

        """
