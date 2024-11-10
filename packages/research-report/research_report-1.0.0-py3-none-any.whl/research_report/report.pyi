from .records import Experiment
from typing import Iterable

__all__ = ['make_report']

def make_report(exps: Iterable[Experiment]) -> str: ...
