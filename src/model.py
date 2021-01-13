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

        Activation Function:        Leaky ReLu=0.2
        Bias + Kernel Regularizer:  L2=0.1

        Model:
        In: 32 x 32 x 1
        L1: kernel (5 x 5), stride (2 x 2), BN + dropout (0.4), Leaky ReLu=0.2, Reg=0.2  = 14 x 14 x  32
        L2: kernel (5 x 5), stride (1 x 1), BN + dropout (0.4), Leaky ReLu=0.2, Reg=0.2  = 10 x 10 x  48
        L3: kernel (5 x 5), stride (1 x 1), BN + dropout (0.3), Leaky ReLu=0.2, Reg=0.2  =  6 x  6 x  64
        L4: kernel (6 x 6), stride (1 x 1), BN + dropout (0.3), Leaky ReLu=0.2, Reg=0.2  =  1 x  1 x 142
        L5: kernel (1 x 1), stride (1 x 1), BN + dropout (0.3), Leaky ReLu=0.2, Reg=0.2  =  1 x  1 x 128
        L6: kernel (1 x 1), stride (1 x 1),                     Sigmoid,        Reg=0.05 =  1 x  1 x  |M|
        Out: 1 x 1 x |M|
        """

        return
