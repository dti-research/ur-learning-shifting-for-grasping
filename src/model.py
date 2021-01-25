# Copyright (c) 2021, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# Author: Nicolai Anton Lynnerup <nily@dti.dk>

# TODO:
# [X] Create overview of model architecture
# [X] Add all parameters
# [X] Create layer block generator
# [ ] Insert layers into Keras Model() instance
# [ ] Create model saver + loader w/ ONNX
# [ ] Add summary function

import tensorflow as tf

class Model:
    def __init__(self, output, training):
        """
        Image size: 110 x 110 x 1 (ROI cut from 640x480 orthographic image)

        Substate, s', creation is done by a sliding window
        w/ kernel (32 x 32), stride (2 x 2)

        Model:
        In: 32 x 32 x 1

        Conv2D Layers:

            Kernel    Stride    Filters   BN      Dropout   Activation       Bias Reg   Kernel Reg   Output
        L1: (5 x 5)   (2 x 2)   32        True    0.4       Leaky ReLu=0.2   L2=0.1     L2=0.1       14 x 14 x  32
        L2: (5 x 5)   (1 x 1)   48        True    0.4       Leaky ReLu=0.2   L2=0.1     L2=0.1       10 x 10 x  48
        L3: (5 x 5)   (1 x 1)   64        True    0.3       Leaky ReLu=0.2   L2=0.1     L2=0.1        6 x  6 x  64
        L4: (6 x 6)   (1 x 1)   142       True    0.3       Leaky ReLu=0.2   L2=0.1     L2=0.1        1 x  1 x 142
        L5: (1 x 1)   (1 x 1)   128       True    0.3       Leaky ReLu=0.2   L2=0.1     L2=0.1        1 x  1 x 128
        L6: (1 x 1)   (1 x 1)   |M|       False   -         Sigmoid          L2=0.05    -             1 x  1 x  |M|

        Out: 1 x 1 x |M|
        """
        M = output # number of primitives

        x = tf.keras.Input(shape=(None, None, 1))

        x = self._Conv2D(x, 32, kernel_size=(5, 5), strides=(2, 2), training=training)
        x = self._Conv2D(x, 48, kernel_size=(5, 5), training=training)
        x = self._Conv2D(x, 64, kernel_size=(5, 5), training=training)
        x = self._Conv2D(x, 142, kernel_size=(6, 6), training=training)
        x = self._Conv2D(x, 128, kernel_size=(1, 1), training=training)
        x = tf.keras.layers.Conv2D(
            M,
            kernel_size=(1,1),
            activation='sigmoid',
            bias_regularizer=tf.keras.regularizers.l2(0.05)
        )(x)

        tf.keras.layers.Reshape

        # TODO: Insert the layers above into a Keras Model() instance

        return

    def _Conv2D(self,
               x,
               filters,
               kernel_size,
               strides = (1, 1),
               padding = 'valid',
               dilation_rate = (1, 1),
               dropout_rate = 0.4,
               l2 = 0.1,
               alpha=0.2,
               training=True):
        """ Generates a Conv2D block including activation function, batch
            normalisation (BN) and dropout

        Args:
            x (image): input image
            filters (int): number of filters to learn
            kernel_size (tuple): See tf.keras.Conv2D.
            strides (tuple, optional): See tf.keras.Conv2D. Defaults to (1, 1).
            padding (str, optional): See tf.keras.Conv2D. Defaults to 'valid'.
            dilation_rate (tuple, optional): See tf.keras.Conv2D. Defaults to (1, 1).
            dropout_rate (float, optional): Float between 0 and 1. Fraction of the input units to drop.. Defaults to 0.4.
            l2 (float, optional): L2 regularization factor. Defaults to 0.1.
            alpha (float, optional): Float >= 0. Negative slope coefficient. Defaults to 0.2.
            training (bool, optional): Used to de-/activate dropout during inference/training. Defaults to True.

        Returns:
            Conv2D layer block w/ activation function, BN and dropout
        """
        x = tf.keras.layers.Conv2D(
            filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            dilation_rate=dilation_rate,
            bias_regularizer=tf.keras.regularizers.l2(l2),
            kernel_regularizer=tf.keras.regularizers.l2(l2)
        )(x)
        # Apply ReLu before BN (see: https://github.com/keras-team/keras/issues/1802#issuecomment-187966878)
        # Allow a small, positive gradient when the unit is not active
        x = tf.keras.layers.LeakyReLU(alpha=alpha)(x)
        # Normalize layer output PDF before becomming input to the next layer
        x = tf.keras.layers.BatchNormalization()(x)
        # Apply Dropout *after* BN (see: https://arxiv.org/abs/1801.05134)
        return tf.keras.layers.Dropout(rate=dropout_rate)(x, training=training)
