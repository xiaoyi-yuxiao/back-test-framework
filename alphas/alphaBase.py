"""base class for all alphas"""
from abc import ABC, abstractmethod


class AlphaBase(ABC):
    @abstractmethod
    def calculate(self):
        """
        must be implemented for any alpha class
        :return:
        """
        pass
