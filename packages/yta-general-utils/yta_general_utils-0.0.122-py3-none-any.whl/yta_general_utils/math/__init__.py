import numpy as np


class Math:
    """
    Class to simplify and encapsulate functionality related
    to math that could be more complex than the contained 
    in the basic python math module.
    """
    @staticmethod
    def sigmoid(value):
        """
        TODO: Write doc about this
        """
        return 1.0 / (1 + np.exp(-value))