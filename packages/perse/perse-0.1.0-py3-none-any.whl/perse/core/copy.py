
import polars as pl

class CopyMixin:
    def copy(self):
        """Deep copy of the DataFrame"""
        copied_dl = self.dl.clone()
        return self.__class__(dl=pl.DataFrame(copied_dl))