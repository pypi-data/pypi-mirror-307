import os
import pickle
from os import path
from typing import Any, Self, cast, Iterable

from IPython.display import HTML
from reliable_finalizer import reliable_finalizer  # type: ignore

from .records import Experiment, Try
from .report import make_report


class _DisplayStr(str):
    def __repr__(self) -> str:
        return self


class Builder:
    """
    The main class of the module, that provides method for report construction.

    Report consists of experiments. Each experiment has a version, goal and result.
    Each experiment consists of tries. Each try has a number (starting from 0),
    a status (True - success, False - failure) and a status message.

    """
    @classmethod
    def create(cls, persist_path: str) -> Self:
        """
        The primary constructor of the `Builder` class, that unpickles the instance from the file if it exists.
        This is the only constructor you should use in your code: don't use `__new__` directly.
        :param persist_path: path to save file. If this path contains missing directories,
        they will be tried to be created.
        :return: Builder instance
        """
        try:
            with open(persist_path, "rb") as f:
                return cast(Self, pickle.load(f))
        except OSError:
            return cls(persist_path)

    persist_path: str
    experiments: dict[Any, Experiment]
    aliases: dict[str, list[Any]]
    current_experiment: Experiment | None
    current_try: Try | None

    def __init__(self, persist_path: str) -> None:
        self.persist_path = persist_path

        self.experiments = {}
        self.aliases = {}

        self.current_experiment = None
        self.current_try = None

    @property
    def current_version(self) -> str | None:
        """
        :returns: a string combining information about current version and try in the form "{version}/{try}".
        It can be used as a path to file (given the version name is a proper directory name)
        """
        return f"{self.current_experiment.version}/{self.current_try.number}" \
            if self.current_experiment and self.current_try else None

    def _require_experiment(self) -> None:
        if not self.current_experiment:
            raise RuntimeError("No experiment is chosen at the moment. To fix the problem, use `navigate`")

    def navigate(self, version: Any, try_number: int = -1) -> None:
        """
        Chooses an experiment and its try to modify with `Builder`'s methods
        :param version: version or alias of the experiment
        :param try_number: a proper index for list of tries of the chosen experiment (default: -1)
        """
        if version not in self.experiments:
            raise RuntimeError(f"No such experiment: {version!r}")

        self.current_experiment = self.experiments[version]

        try:
            self.current_try = self.current_experiment.tries[try_number]
        except IndexError:
            raise RuntimeError(f"No such try: {try_number}")

    def experiment(self, name: str, navigate: bool = True) -> None:
        """
        Creates a new experiment and its first try
        :param name: version name
        :param navigate: weather to navigate to the newly created experiment or not (default: True)
        """
        if name in self.experiments:
            raise RuntimeError(f"Name {name!r} is already used")

        first_try = Try(0)
        experiment = Experiment(name, [first_try])
        self.aliases[name] = []
        self.experiments[name] = experiment

        if navigate:
            self.current_experiment = experiment
            self.current_try = first_try

        self.save()

    def alias(self, al: Any) -> None:
        """
        Sets an alias for the current experiment. Unlike the version name, alias can be of any type.
        :param al: the alias
        """
        if al in self.experiments:
            raise RuntimeError(f"Name {al!r} is already used")

        self._require_experiment()
        assert self.current_experiment is not None

        self.experiments[al] = self.current_experiment
        self.aliases[self.current_experiment.version].append(al)

    def try_(self, navigate: bool = True) -> None:
        """
        Creates a new try for the current experiment
        :param navigate: weather to navigate to the newly created try or not
        """
        self._require_experiment()
        assert self.current_experiment is not None

        n = len(self.current_experiment.tries)
        new_try = Try(n)
        self.current_experiment.tries.append(new_try)

        if navigate:
            self.current_try = new_try

        self.save()

    def goal(self, text: str) -> None:
        """
        Set the goal of the current experiment
        :param text: goal text to set
        """
        self._require_experiment()
        assert self.current_experiment is not None

        self.current_experiment.goal = text

        self.save()

    def result(self, text: str) -> None:
        """
        Set the result of the current experiment
        :param text: result text tot set
        """
        self._require_experiment()
        assert self.current_experiment is not None

        self.current_experiment.result = text
        self.save()

    def try_status(self, status: bool, status_message: str = "") -> None:
        """
        Set current try's status and optionally status message
        :param status: status to set
        :param status_message: status message to set
        """
        self._require_experiment()
        assert self.current_try is not None

        self.current_try.status = status
        self.current_try.status_message = status_message
        self.save()

    def versions(self) -> str:
        """
        :returns: formatted list of all versions and corresponding aliases
        """
        res = "\n".join(
            repr(version) + (f" (Aliases: [{', '.join(map(repr, aliases))}])" if aliases else "")
            for version, aliases in self.aliases.items()
        )

        return _DisplayStr(res)

    def report(self, *, current_only: bool = False) -> HTML:
        """
        :returns: formatted table of the report
        :param current_only: if True, only the report for the current experiment will be constructed
        """
        experiments: Iterable[Experiment]
        if not current_only:
            experiments = (self.experiments[version] for version in self.aliases)
        else:
            self._require_experiment()
            assert self.current_experiment is not None
            experiments = [self.current_experiment]

        render = make_report(experiments)

        return HTML(render)

    def save(self) -> None:
        """
        Saves the instance of `Builder` to the persistence file. This method is called after every mutating operation
        and when the instance is garbage collected. You can also call it manually.
        """
        dirs, _ = path.split(self.persist_path)
        if dirs:
            os.makedirs(dirs, exist_ok=True)

        with open(self.persist_path, "wb") as f:
            pickle.dump(self, f)

    @reliable_finalizer
    def _save(self) -> None:
        self.save()


def report_builder(persist_path: str) -> Builder:
    return Builder.create(persist_path)


__all__ = ["Builder", "report_builder"]
