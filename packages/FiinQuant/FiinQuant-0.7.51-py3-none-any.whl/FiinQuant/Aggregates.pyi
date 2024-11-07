from datetime import datetime
import pandas as pd

class Bar:
    def __init__(self, 
                 access_token: str, 
                 ticker: str,  
                 by: str,  
                 from_date: str | datetime,  
                 to_date: str | datetime,  
                 multiplier: int = 1,  
                 limit: int = -1) -> None:...

    def get(self, data_type: str) -> BarData: ...

class BarData:
    def __init__(self, data) -> None:
        self.__private_attribute: pd.DataFrame
        self.Open: pd.Series
        self.Low: pd.Series
        self.High: pd.Series
        self.Close: pd.Series
        self.Volume: pd.Series
        self.Timestamp: pd.Series

    def to_dataFrame(self) -> pd.DataFrame: ...

class BarDataUpdate:
    def __init__(self, data) -> None:
        self.__private_attribute: pd.DataFrame
        self.Ticker: str
        self.Open: pd.Series
        self.Low: pd.Series
        self.High: pd.Series
        self.Close: pd.Series
        self.Volume: pd.Series
        self.Timestamp: pd.Series

    def to_dataFrame(self) -> pd.DataFrame: ...

class IndexBars(Bar) : 
    def get(self) -> BarData: ...

class TickerBars(Bar):
    def get(self) -> BarData: ...

class CoveredWarrantBars(Bar):
    def get(self) -> BarData: ...
    
class DerivativeBars(Bar):
    def get(self) -> BarData: ...



