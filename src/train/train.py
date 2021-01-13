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
        AdamOptimizer

        Learning rate = ?
        Epochs = 5000
        """