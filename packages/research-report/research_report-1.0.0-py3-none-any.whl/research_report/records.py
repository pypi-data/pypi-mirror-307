from dataclasses import dataclass


@dataclass
class Try:
    number: int
    status: bool | None = None
    status_message: str | None = None


@dataclass
class Experiment:
    version: str
    tries: list[Try]
    goal: str | None = None
    result: str | None = None


__all__ = ["Try", "Experiment"]
