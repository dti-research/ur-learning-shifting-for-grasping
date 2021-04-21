from typing import List

import numpy as np

from off_policy_rl.utils.selection_method import SelectionMethod

class Epoch:
    def __init__(
        self,
        number_episodes: int,
        selection_methods: List[SelectionMethod],
        probabilities: List[float] = None
    ):
        self.number_episodes = number_episodes

        if len(selection_methods) > 1 and len(selection_methods) != len(probabilities):
            raise AssertionError("The number of Selection Methods must match the number of probabilities")

        self.selection_methods = selection_methods

        if probabilities is not None:
            if sum(probabilities) != 1.0:
                raise AssertionError("The list of probabilities must add to 1.0"
                                     " (current sum: {})".format(sum(probabilities)))
        self.probabilities = probabilities

    def get_selection_method(self) -> SelectionMethod:
        if len(SelectionMethod) > 1:
            return np.random.choice(self.selection_methods, p=self.probabilities)
        return self.selection_methods[-1]
