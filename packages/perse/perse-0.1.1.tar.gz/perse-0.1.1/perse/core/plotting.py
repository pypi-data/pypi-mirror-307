import matplotlib.pyplot as plt
from .base import BaseDataFrame

class PlottingDataFrame(BaseDataFrame):
    """PlottingDataFrame"""
    def plot(self, *args, show=True, **kwargs):
        """Plot data using Pandas' plot method."""
        self.refresh_pandas()
        ax = self._df.plot(*args, **kwargs)
        if show:
            plt.show()
        return ax