from dataclasses import dataclass
from multiprocessing.pool import Pool
from typing import Callable, TypeVar


T = TypeVar("T")
O = TypeVar("O")
class RunStrategy:
    """
    Some strategy to run an operation on a collection of items and return a collection of results from those operations.
    """
    def run_all(self, items: list[T], oper: Callable[[T], O]) -> list[O]:
        raise NotImplementedError("Abstract method must be overwriten")


@dataclass
class Parallel(RunStrategy):
    procs: None | int = None
    def run_all(self, items: list[T], oper: Callable[[T], O]) -> list[O]:
        return Pool(self.procs).map(oper, items)


class Sequential(RunStrategy):
    def run_all(self, items: list[T], oper: Callable[[T], O]) -> list[O]:
        return [oper(item) for item in items]
