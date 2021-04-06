# Copyright (c) 2021, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# Author: Nicolai Anton Lynnerup <nily@dti.dk>

from calibration.calibration import Calibration

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
        # Create instance of main train class
        self.calibration = Calibration()

    def set_box_coordinates(self, x_low, x_high, y_low, y_high):
        coordinates = [x_low, x_high, y_low, y_high]
        print(coordinates)
        self.calibration.set_box_coordinates(coordinates)

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
