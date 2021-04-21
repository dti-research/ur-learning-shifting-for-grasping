import os

from off_policy_rl.utils.bin import Bin
from off_policy_rl.utils.epoch import Epoch
from off_policy_rl.utils.selection_method import SelectionMethod
from off_policy_rl.utils.types import Pose

class Config:
    Epochs = [
        Epoch(
            number_episodes=200,
            selection_methods=[SelectionMethod.Random]
        ),
        Epoch(
            number_episodes=10,
            selection_methods=[SelectionMethod.Random, SelectionMethod.Top5],
            probabilities=[0.99, 0.01]
        )
    ]

    # Frames in robot's base frame
    Bins = [
        Bin(
            size=[365,265],
            frame=Pose(
                x  =  306.09,  # mm
                y  = -255.65,  # mm
                z  =   71.78,  # mm
                rx =    2.220, # rad
                ry =   -2.225, # rad
                rz =    0.002  # rad
            )
        ),
        Bin(
            size=[365,265],
            frame=Pose(
                x  =  -96.84,  # mm
                y  = -255.65,  # mm
                z  =   71.78,  # mm
                rx =    2.220, # rad
                ry =   -2.225, # rad
                rz =    0.002  # rad
            )
        )
    ]

    current_bin = 1

    data_folder = "../data"
    model_folder = os.path.join(data_folder, "models")

    @classmethod
    def get_model_path(cls, name: str):
        return os.path.join(Config.model_folder, name)

    @classmethod
    def get_bin_coordinates(cls, clearance: float = None):
        bin_coordinates = [0,365,0,265]

        if clearance != None:
            bin_coordinates[0] += clearance
            bin_coordinates[1] -= clearance
            bin_coordinates[2] += clearance
            bin_coordinates[3] -= clearance

        return bin_coordinates
