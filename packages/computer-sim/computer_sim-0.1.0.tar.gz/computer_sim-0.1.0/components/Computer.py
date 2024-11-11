import numpy as np
from .processor import Processor

class ComputerProcessor(Processor):
    """Processes data on the computer's motherboard."""
    def process(self, data):
        # Randomly set a bit to 1 on the motherboard
        row, col = np.random.randint(0, data.shape[0]), np.random.randint(0, data.shape[1])
        data[row, col] = 1
        return data
    
class Computer:
    """Simulates the computer with a motherboard and processor."""
    def __init__(self, shape=(4, 8)):
        self.motherboard = np.zeros(shape, dtype=int)
        self.processor = ComputerProcessor()
    
    def program(self, input_data=None):
        """Run the computer processor to modify the motherboard."""
        if input_data is not None:
            self.motherboard = input_data
        self.motherboard = self.processor.process(self.motherboard)
        return self.motherboard