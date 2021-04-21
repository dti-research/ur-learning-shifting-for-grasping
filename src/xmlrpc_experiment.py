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

import sys
import math
import argparse

from typing import List

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

    def get_current_bin_frame(self) -> List[float]:
        frame = self.experiment.get_current_bin_frame()
        return [frame.x,
                frame.y,
                frame.z,
                frame.rx,
                frame.ry,
                frame.rz]

    def infer(self, epoch: int, episode: int):
        """Makes inference in the current state.
        It is important that the robot is positioned at the camera WP and
        is steady.

        Args:
            epoch (int): index of current epoch
            episode (int): index of current episode

        Returns:
            list: x      [float]
                  y      [float]
                  rz     [float]
                  d      [int]
                  bin.pose.x [float] mm
                  bin.pose.y [float] mm
                  bin.pose.z [float] mm
                  bin.pose.rx [float] rad
                  bin.pose.ry [float] rad
                  bin.pose.rz [float] rad
        """
        action = self.experiment.infer(epoch, episode)
        return [action.pose.x,
               action.pose.y,
               action.pose.rz,
               action.pose.d,
               action.bin.frame.x,
               action.bin.frame.y,
               action.bin.frame.z,
               action.bin.frame.rx,
               action.bin.frame.ry,
               action.bin.frame.rz]


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
