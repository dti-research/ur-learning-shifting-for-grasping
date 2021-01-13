# Copyright (c) 2021, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# 
# Author: Nicolai Anton Lynnerup <nily@dti.dk>

import tensorflow as tf

class Model:
    def __init__(self, input, output, training):
        """
        Image size: 110 x 110 x 1 (ROI cut from 640x480 orthographic image)
        
        Substate, s', creation is done by a sliding window
        w/ kernel (32 x 32), stride (2 x 2)

        Model:
        In: 32 x 32 x 1

        Conv2D Layers:

            Kernel    Stride    BN     Dropout   Activation       Bias Reg   Kernel Reg   Output
        L1: (5 x 5)   (2 x 2)   True   0.4       Leaky ReLu=0.2   L2=0.1     L2=0.1       14 x 14 x  32
        L2: (5 x 5)   (1 x 1)   True   0.4       Leaky ReLu=0.2   L2=0.1     L2=0.1       10 x 10 x  48
        L3: (5 x 5)   (1 x 1)   True   0.3       Leaky ReLu=0.2   L2=0.1     L2=0.1        6 x  6 x  64
        L4: (6 x 6)   (1 x 1)   True   0.3       Leaky ReLu=0.2   L2=0.1     L2=0.1        1 x  1 x 142
        L5: (1 x 1)   (1 x 1)   True   0.3       Leaky ReLu=0.2   L2=0.1     L2=0.1        1 x  1 x 128
        L6: (1 x 1)   (1 x 1)   -      -         Sigmoid          L2=0.05    -             1 x  1 x  |M|
        
        Out: 1 x 1 x |M|
        """

        return
