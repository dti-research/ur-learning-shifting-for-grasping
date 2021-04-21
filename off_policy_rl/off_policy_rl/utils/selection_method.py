import numpy as np

from enum import Enum

SelectionMethod = Enum('SelectionMethod', [
    'Min',
    'Max',
    'Top5',
    'Prob',
    'PowerProb',
    'Uncertainty',
    'Random',
])
