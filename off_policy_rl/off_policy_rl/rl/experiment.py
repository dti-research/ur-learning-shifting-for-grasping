# Copyright (c) 2021, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# Author: Nicolai Anton Lynnerup <nily@dti.dk>

import logging
import time
from typing import List

import numpy as np

from off_policy_rl.config.config import Config
from off_policy_rl.rl.action import Action, ActionType
from off_policy_rl.rl.environment import Environment
from off_policy_rl.utils.types import ActionPose, Pose
from off_policy_rl.utils.camera import IntelRealSense
from off_policy_rl.utils.epoch import Epoch
from off_policy_rl.utils.loader import Loader
from off_policy_rl.utils.selection_method import SelectionMethod
from off_policy_rl.utils.saver import Saver

import cv2
import pyrealsense2.pyrealsense2 as rs
from tensorflow.keras import Model, models


log = logging.getLogger(__name__)


class Experiment():
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

    def __init__(self,
                 verbose = True):
        self.camera = IntelRealSense()
        self.verbose = verbose
        self.environment = Environment(Config.Bins)
        self.saver = Saver(Config.data_folder)
        #self.model: Model = Loader.get_model("")
        # history =

    def infer(self, epoch: int, episode: int) -> Action:
        if self.verbose:
            start = time.time()

        method = self.get_selection_method(epoch)
        bin_coordinates = Config.get_bin_coordinates(clearance=50.0) # mm

        rgd, depth = self.camera.get_rectified_rgb_image_and_depth()
        input_images = rgd, depth #self.get_images(frame)

        if method == SelectionMethod.Random:
            pose = ActionPose(
                x  = np.random.uniform(bin_coordinates[0], bin_coordinates[1]), # mm
                y  = np.random.uniform(bin_coordinates[2], bin_coordinates[3]), # mm
                rz = np.random.choice(np.arange(0, np.pi, np.pi/20)).item(), # rad
                d  = np.random.choice(2)
            )

            action = Action(
                action=ActionType.Grasp,
                bin=self.environment.get_current_bin(),
                pose=pose,
                method=method,
                image=input_images,
            )

            return action

        """# Prediction
        result = self.model.predict(input_images)

        pose = Pose(
            x  = result[0],
            y  = result[1],
            rz = result[2],
            d  = result[3]
        )

        action = Action(
            action=ActionType.Grasp,
            bin=0, # TODO!
            pose=pose,
            method=method,
            image=input_images
        )

        if self.verbose:
            log.info(f"NN Inference time [s]: {time.time() - start:.3}")

        return action"""

        raise Exception(f'Selection method not implemented: {method}')


    def get_number_epochs(self) -> int:
        return len(Config.Epochs)

    def get_number_episodes_in_epoch(self, epoch_index: int) -> int:
        return Config.Epochs[epoch_index].number_episodes

    def get_selection_method(self, epoch_index: int) -> SelectionMethod:
        return Config.Epochs[epoch_index].get_selection_method()

    def get_current_bin_frame(self) -> List[float]:
        return self.environment.get_current_bin().frame

    def get_images(self, frames: rs.frame) -> List:
        image = frames.get_color_frame()
        #image = clone(orig_image)

        # TODO: Convert image to CV2 Mat

        return image

        """draw_around_box(image, box=self.box)
        background_color = image.value_from_depth(get_distance_to_box(image, self.box))

        mat_image_resized = cv2.resize(image.mat, self.size_resized)

        mat_images = []
        for a in self.a_space:
            rot_mat = cv2.getRotationMatrix2D(
                (self.size_resized[0] / 2, self.size_resized[1] / 2),
                a * 180.0 / np.pi,
                1.0
            )
            rot_mat[:, 2] += [
                (self.size_rotated[0] - self.size_resized[0]) / 2,
                (self.size_rotated[1] - self.size_resized[1]) / 2
            ]
            dst_depth = cv2.warpAffine(mat_image_resized, rot_mat, self.size_rotated, borderValue=background_color)
            mat_images.append(crop(dst_depth, self.size_cropped))

        mat_images = np.array(mat_images) / np.iinfo(image.mat.dtype).max
        if len(mat_images.shape) == 3:
            mat_images = np.expand_dims(mat_images, axis=-1)

        # mat_images = 2 * mat_images - 1.0
        return mat_images"""
