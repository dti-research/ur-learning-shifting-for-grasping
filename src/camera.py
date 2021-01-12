# Copyright (c) 2021, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# 
# Original author: Nicolai Anton Lynnerup <nily@dti.dk>

# TODO:
# [ ] Read all camera parameters
#     [X] Device Info
#     [X] Sensor Options
#     [ ] Calibration (both intrinsic and extrinsic)
# [X] Store parameters in a file 
# [ ] Connect to specific camera by S/N
# [ ] Load parameters from file and upload to camera
# [X] Grab frames with software trigger
# [ ] Write recursive function that can stringify dict keys.

import imageio
import numpy as np
import os
import json
import pyrealsense2.pyrealsense2 as rs
import utils

class IntelRealSense:
    def __init__(self, serial = None):
        """Initialises a single Intel RealSense device

        Args:
            serial (string, optional): Used to connect to a specific device. Defaults to None.

        Raises:
            RuntimeError: If no device is found
        """
        if serial is not None:
            raise NotImplementedError

        self._context = rs.context()
        self._device_list = self._context.query_devices()
        if(self._device_list.size() == 0):
            raise RuntimeError('No devices found. Is it connected?')
        self._device = self._device_list.front()
        
        for sensor in self._device.sensors:
            if sensor.is_depth_sensor():
                self._sensor_depth = sensor
            else:
                self._sensor_color = sensor
        
        self._pipeline = rs.pipeline()
        self._config = rs.config()
        self._config.enable_device(self._device.get_info(rs.camera_info.serial_number))
        self._profile = self._pipeline.start(self._config)
        
        self._parameters = self._load_parameters_from_camera()
    
    def __del__(self):
        """ Cleanly shuts down the pipeline once the garbage collector is called
        """
        self._pipeline.stop()

    def get_device(self):
        """ Returns the current device connected. In RS2 a device e.g. a D435
            has two sensors; (1) the depth sensor and (2) the RGB sensor.

        Returns:
            rs.device: Device object from the RS2 API
        """
        return self._device
    
    def get_depth_sensor(self):
        """ Returns the current device's depth sensor

        Returns:
            rs.sensor: Sensor object from RS2 API
        """
        return self._sensor_depth
    
    def get_color_sensor(self):
        """ Returns the current device's RGB sensor

        Returns:
            rs.sensor: Sensor object from RS2 API
        """
        return self._sensor_color
    
    def _load_parameters_from_camera(self):
        """ Internal class method to query the camera for its info, parameters,
            calibration, etc.

        Returns:
            dict: All info, parameters, calibration, etc.
        """
        parameters = dict()
        parameters['info'] = self.get_info()
        parameters['options'] = self.get_options()
        #parameters['calibration'] = {'intrinsic' : self.}
        return parameters

    def save_all_parameters(self, path = None):
        """ Saves all camera parameters to a file optionally specified by
            a path to a folder. The filename is the device name and its S/N


        Args:
            path (str, optional): Path to storage folder. Defaults to None.
        """
        filename = '{}_{}.json'.format(
            self._device.get_info(rs.camera_info.name),
            self._device.get_info(rs.camera_info.serial_number)).lower().replace(' ', '_')

        #str_parameters = utils.stringify_dict(self._parameters)
        
        # Write to disk
        with open(os.path.join(path if path is not None else '', filename), 'w') as f:
            json.dump(self._parameters, f, sort_keys=False, indent=4)
    
    def get_info(self):
        """ Retrieve camera specific information,
            like versions of various internal components

        Returns:
            dict: all rs.camera_info.X
        """
        info = dict()
        info['name'] = self._device.get_info(rs.camera_info.name) 
        info['serial_number'] = self._device.get_info(rs.camera_info.serial_number)
        info['firmware_version'] = self._device.get_info(rs.camera_info.firmware_version)
        info['recommended_firmware_version'] = self._device.get_info(rs.camera_info.recommended_firmware_version)
        info['physical_port'] = self._device.get_info(rs.camera_info.physical_port)
        info['debug_op_code'] = self._device.get_info(rs.camera_info.debug_op_code)
        info['product_id'] = self._device.get_info(rs.camera_info.product_id)
        info['camera_locked'] = self._device.get_info(rs.camera_info.camera_locked)
        info['usb_type_descriptor'] = self._device.get_info(rs.camera_info.usb_type_descriptor)
        info['product_line'] = self._device.get_info(rs.camera_info.product_line)
        info['asic_serial_number'] = self._device.get_info(rs.camera_info.asic_serial_number)
        info['firmware_update_id'] = self._device.get_info(rs.camera_info.firmware_update_id)
        return info

    def get_options(self):
        """ Returns all sensor specific options for all sensors in a device,
            such as gain, exposure, etc.

        Returns:
            dict: Dictionary with rs.option object references and their current
                  value
        """ 
        options = dict()
        for sensor in self._device.sensors:
            sensor_name = sensor.get_info(rs.camera_info.name).lower().replace(' ', '_')
            options[sensor_name] = self.get_sensor_options(sensor)
        
        return options

    def get_sensor_options(self, sensor):
        """ Returns all sensor specific options for one specific sensor within
            the currently connected device.

        Args:
            sensor (rs.sensor): Sensor object from the RS2 API.

        Returns:
            dict: Dictionary containing all options for the specific sensor.
        """
        rs_options = sensor.get_supported_options()
        options = dict()

        for option in rs_options:
            # HACK: Eventhough RS2 returns "supported" options, some are still not
            # supported by the sensor. This avoids this failure.
            if sensor.supports(option):
                options[str(option)] = sensor.get_option(option)
        
        return options
    
    def get_frames(self):
        """ Grab a single image and return it.

        Returns:
            rs.frame: Resulting image grabbed by the device.
        """
        frames = self._pipeline.wait_for_frames()
        return frames

#def print_sensor_config(config):
#    print("\r\n{:<40} {:<15}".format('Option', 'Value'))
#    for option, value in config.items():
#        print("{:<40} {:<15}".format(str(option), value))

if __name__ == "__main__":
    camera = IntelRealSense()
    camera.save_all_parameters('../data')

    frames = camera.get_frames()
    print(frames.get_profile().as_video_stream_profile().get_intrinsics())
    rgb = frames.get_color_frame()
    
    # Write to .png
    color = np.asanyarray(rgb.get_data())
    imageio.imwrite("../data/rgb.png", color)
    
