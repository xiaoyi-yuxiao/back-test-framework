"""
base interface for rebalancing portfolio weight
实现calculate 方程，只需要返回给定的data数据当中的一些股票以及weight就行
"""
from abc import ABC, abstractmethod


class AlgoBase(ABC):
    @abstractmethod
    def calculate_weight(self, data):
        pass
