# Copyright (c) 2021, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# Author: Nicolai Anton Lynnerup <nily@dti.dk>


class Calibration():
    def __init__(self):
        self.coordinates = []

    def set_box_coordinates(self, coordinates):
        self.coordinates = coordinates
        print(coordinates)

    def get_box_coordinates(self):
        return self.coordinates
