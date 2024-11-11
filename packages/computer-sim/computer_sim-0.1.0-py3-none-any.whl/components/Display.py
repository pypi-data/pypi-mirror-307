import numpy as np
from .processor import Processor

class DisplayProcessor(Processor):
    """Processes data for display."""
    def process(self, input_data):
        # Transform input data for display (e.g., mirror or invert bits)
        processed_data = np.zeros_like(input_data)
        processed_data[input_data == 1] = 1
        return processed_data
    
class Display:
    """Handles the display of data on a screen-like output."""
    def __init__(self, shape=(4, 8)):
        self.processor = DisplayProcessor()
        self.resize(shape)
        
    def resize(self, shape):
        """Resize the display matrix."""
        self.shape = shape
        self.matrix = np.zeros(shape=self.shape, dtype=int)
        
    def process_output(self, input_data):
        """Process the motherboard data to display format."""
        # Resize input data to match display shape if needed
        if input_data.shape != self.shape:
            resized_data = np.zeros(self.shape, dtype=int)
            min_rows = min(input_data.shape[0], self.shape[0])
            min_cols = min(input_data.shape[1], self.shape[1])
            resized_data[:min_rows, :min_cols] = input_data[:min_rows, :min_cols]
            input_data = resized_data
            
        self.matrix = self.processor.process(input_data)
        return self.matrix
        
    def render(self, input_data, container):
        """Render the processed display matrix."""
        display_matrix = self.process_output(input_data)
        container.dataframe(display_matrix, use_container_width=True)