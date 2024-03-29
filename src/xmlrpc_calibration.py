# Copyright (c) 2021, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# Author: Nicolai Anton Lynnerup <nily@dti.dk>

from off_policy_rl.calibration.calibration import Calibration

import sys
import argparse
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

parser = argparse.ArgumentParser(
    description='Start XML-RPC server allowing a '
                'client to calibrate the scene')
parser.add_argument('--ip', default='192.168.1.100',
                    help='IP adress of the XML-RPC server (default: 192.168.1.100')
parser.add_argument('--port', default=8000,
                    help='Port number of the server (default: 8000)')

args = parser.parse_args()

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/lsfg/calibration',)

class CalibrationProxy():
    """ Proxy class to make the Calibration class methods accesible via XML-RPC.
        An instance of this class is registered in the XML-RPC server below.
        This is made so the class is separated from the XML-RPC specifics
        allowing for easy conversion between protocols.
    """
    def __init__(self):
        # Create instance of main calibration class
        self.calibration = Calibration()

    def set_box_coordinates(self, x_low: float,
                                  x_high: float,
                                  y_low: float,
                                  y_high: float):
        """Save the calibrated coordinates of the box in the scene.

        Args:
            x_low (float): lower x bound
            x_high (float): higher x bound
            y_low (float): lower y bound
            y_high (float): higher y bound
        """
        coordinates = [x_low, x_high, y_low, y_high]
        self.calibration.set_box_coordinates(coordinates)

    def get_box_coordinates(self):
        """Returns the stored box coordinates

        Returns:
            list: The four coordinate values {x_low, x_high, y_low, y_high}
        """

        coordinates = self.calibration.get_box_coordinates()
        return coordinates[0], coordinates[1], coordinates[2], coordinates[3]

    # TODO: Add methods to make the needed data conversions and function calls



# Create XML-RPC server
with SimpleXMLRPCServer((args.ip, args.port),
                        requestHandler=RequestHandler,
                        allow_none=True) as server:
    # Allows the client to call e.g. system.listMethods()
    server.register_introspection_functions()

    # Register a complete instance of the Train proxy class for the client to access
    server.register_instance(CalibrationProxy())

    # Run the server's main loop
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server")
        server.server_close()
        sys.exit(0)
