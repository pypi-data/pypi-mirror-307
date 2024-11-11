import numpy as np

class Processor:
    """Base class for processors."""
    def process(self, data):
        raise NotImplementedError("Processor subclasses must implement process()")
