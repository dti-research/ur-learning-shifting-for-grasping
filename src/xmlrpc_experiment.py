# Copyright (c) 2021, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# Author: Nicolai Anton Lynnerup <nily@dti.dk>

#from experiment.experiment import Experiment

#from off_policy_rl.experiment.experiment import Experiment
from off_policy_rl.rl.experiment import Experiment
from off_policy_rl.utils.types import Pose

import sys
import math
import argparse

from typing import List, Dict

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

parser = argparse.ArgumentParser(
    description='Start XML-RPC server allowing a '
                'client to train the RL pipeline.')
parser.add_argument('--ip', default='192.168.1.100',
                    help='IP adress of the XML-RPC server (default: 192.168.1.100')
parser.add_argument('--port', default=8000,
                    help='Port number of the server (default: 8000)')

args = parser.parse_args()

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/lsfg/experiment',)

class ExperimentProxy():
    """ Proxy class to make the Experiment class methods accesible via XML-RPC.
        An instance of this class is registered in the XML-RPC server below.
        This is made so the train class is separated from the XML-RPC specifics
        allowing for easy conversion between protocols.
    """

    def __init__(self):
        # Create instance of main train class
        self.experiment = Experiment()

    def list_to_pose(self, l):
        """Internal function to convert a Python list to a UR pose

        Args:
            l (list): the pose as a list

        Returns:
            dict: the pose as a dict
        """
        assert type(l) is list
        return {'x' : l[0], 'y' : l[1], 'z' : l[2], 'rx' : l[3], 'ry' : l[4], 'rz' : l[5]}

    def pose_to_list(self, p):
        """Internal function to convert a UR pose to a Python list

        Args:
            p (dict): the pose as a dict

        Returns:
            list: the pose as a list
        """
        assert type(p) is dict
        return [p['x'], p['y'], p['z'], p['rx'], p['ry'], p['rz']]

    def get_number_epochs(self) -> int:
        """Returns the number of epochs specified in the Experiment Config

        Returns:
            int: number of epochs
        """
        return self.experiment.get_number_epochs()

    def get_number_episodes_in_epoch(self, epoch_index: int) -> int:
        """Returns the number of episodes in a specific epoch

        Args:
            epoch_index (int): index of epoch

        Returns:
            int: number of episodes in epoch
        """
        return self.experiment.get_number_episodes_in_epoch(epoch_index)

    def get_pick_bin_frame(self) -> Dict[str, float]:
        """Returns the UR pose of the current picking frame

        Returns:
            pose: The pick bin UR pose
        """
        pose = self.experiment.get_pick_bin_frame()
        return self.list_to_pose(
            [pose.x / 1000, # [mm] to [m]
             pose.y / 1000, # [mm] to [m]
             pose.z / 1000, # [mm] to [m]
             pose.rx,
             pose.ry,
             pose.rz]
        )

    def get_drop_bin_frame(self) -> Dict[str, float]:
        """Returns the UR pose of the current dropping frame

        Returns:
            pose: The drop bin UR pose
        """
        pose = self.experiment.get_drop_bin_frame()
        return self.list_to_pose(
            [pose.x / 1000, # [mm] to [m]
             pose.y / 1000, # [mm] to [m]
             pose.z / 1000, # [mm] to [m]
             pose.rx,
             pose.ry,
             pose.rz]
        )


    def get_random_drop_pose(self) -> Dict[str, float]:
        """Returns a random pose (to be used relative to the bin)

        Returns:
            pose: The pick bin UR pose
        """
        pose = self.experiment.get_random_drop_pose()
        return self.list_to_pose(
            [pose.x / 1000, # [mm] to [m]
             pose.y / 1000, # [mm] to [m]
             pose.z / 1000, # [mm] to [m]
             pose.rx,
             pose.ry,
             pose.rz]
        )

    def start_new_experiment(self) -> None:
        """Initiates a new experiment including new trial folder
        """
        self.experiment.start_new_experiment()

    def infer(self, epoch: int, episode: int) -> None:
        """Makes inference in the current state.
        It is important that the robot is positioned at the camera WP and
        is steady.

        Args:
            epoch (int): index of current epoch
            episode (int): index of current episode

        Returns:
            list: x      [float] m
                  y      [float] m
                  rz     [float] rad
                  d      [int]   index
                  bin.pose.x [float] mm
                  bin.pose.y [float] mm
                  bin.pose.z [float] mm
                  bin.pose.rx [float] rad
                  bin.pose.ry [float] rad
                  bin.pose.rz [float] rad
        """
        action = self.experiment.infer(epoch, episode)
        return [action.pose.x / 1000, # [mm] to [m]
                action.pose.y / 1000, # [mm] to [m]
                action.pose.rz,
                action.pose.d#,
                #self.list_to_pose([
                #    action.bin.frame.x,
                #    action.bin.frame.y,
                #    action.bin.frame.z,
                #    action.bin.frame.rx,
                #    action.bin.frame.ry,
                #    action.bin.frame.rz])
                ]

    def end_episode(self, reward: float) -> None:
        """Ends the current episode and saves it to disk

        Args:
            reward (float): the reward given for the effectuated action
        """
        self.experiment.end_episode(reward)


# Create XML-RPC server
with SimpleXMLRPCServer((args.ip, args.port),
                        requestHandler=RequestHandler,
                        allow_none=True) as server:
    # Allows the client to call e.g. system.listMethods()
    server.register_introspection_functions()

    # Register a complete instance of the Train proxy class for the client to access
    server.register_instance(ExperimentProxy())

    # Run the server's main loop
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server")
        server.server_close()
        sys.exit(0)
