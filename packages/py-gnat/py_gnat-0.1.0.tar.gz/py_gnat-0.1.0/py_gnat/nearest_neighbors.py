"""NearestNeighborsGNAT Data Structure from OMPL
Original source: 
https://ompl.kavrakilab.org/NearestNeighbors_8h_source.html
Original authors: Mark Moll

Implemented in Python by Zhuoyun Zhong
The script now strictly follows the original C++ implementation
and is not yet optimized for Python.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Callable


# Define the abstract base class for NearestNeighbors
class NearestNeighbors(ABC):
    def __init__(self):
        self.dist_fn = None

    def set_distance_function(
        self, dist_fn: Callable[[object, object], float]
    ):
        self.dist_fn = dist_fn

    @abstractmethod
    def report_sorted_results(self) -> bool:
        pass

    @abstractmethod
    def clear(self, data: object):
        pass

    @abstractmethod
    def add(self, data: object):
        pass

    def add_list(self, data_list: List[object]):
        for data in data_list:
            self.add(data)

    @abstractmethod
    def remove(self, data: object):
        pass

    @abstractmethod
    def nearest(self, data: object) -> object:
        pass

    @abstractmethod
    def nearest_k(self, data: object, k: int) -> List[object]:
        pass

    @abstractmethod
    def nearest_r(self, data: object, radius: float) -> List[object]:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def list(self, data_list: List[object]):
        pass
