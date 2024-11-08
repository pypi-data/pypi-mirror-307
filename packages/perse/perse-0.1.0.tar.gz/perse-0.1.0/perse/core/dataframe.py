# dataframe.py
from .base import BaseDataFrame
from .sql_operations import SQLDataFrame
from .plotting import PlottingDataFrame
from .df_utilities import UtilitiesDataFrame
from .copy import CopyMixin


class DataFrame(SQLDataFrame, PlottingDataFrame, UtilitiesDataFrame, CopyMixin):
    def final_init(self, *args, **kwargs):
        """final_init"""
        super().__init__(*args, **kwargs)
        _ = self.get_table_name()
        return self


    def final_copy(self, *args, **kwargs):
        """final_init"""
        return self.__class__(dl= kwargs['dl'])
