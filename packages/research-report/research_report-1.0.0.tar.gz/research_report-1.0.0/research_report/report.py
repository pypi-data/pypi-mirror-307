from typing import Iterable

from .records import Experiment, Try


def _get_status_symbol(st: bool | None) -> str:
    dct = {
        None: "",
        True: "\u2714",
        False: "\u2716"
    }

    return dct[st]


def _render_try(try_: Try, front: str | None = None, back: str | None = None) -> str:
    main_part = f"""
        <td>{try_.number}</td>
        <td>{_get_status_symbol(try_.status)}</td>
        <td>{try_.status_message or ""}</td>
    """

    return f"""
        <tr>
            {front or ""}
            {main_part}
            {back or ""}
        </tr>
    """


def _render_experiment(exp: Experiment) -> str:
    if exp.tries is None:
        return ""

    n = len(exp.tries)
    goal = f"""
    <td rowspan="{n}">{exp.version}</td>
    <td rowspan="{n}">{exp.goal or ""}</td>
    """
    result = f"""
    <td rowspan="{n}">{exp.result or ""}</td>
    """

    tries_render = (
        _render_try(try_, goal if not i else None, result if not i else None)
        for i, try_ in enumerate(exp.tries)
    )

    return "\n".join(tries_render)


def make_report(exps: Iterable[Experiment]) -> str:
    exps_render = map(_render_experiment, exps)
    return f"""
    <style>
        td {{
            text-align: left;
            word-wrap: break-word;
        }}
        
        table {{
            width: 50%;
        }}
    </style>
    <table>
        <tr>
            <td>Version</td>
            <td>Goal</td>
            <td>Try</td>
            <td>Status</td>
            <td>Status message</td>
            <td>Result</td>
        </tr>
        {"\n".join(exps_render)}
    </table>
    """


__all__ = ["make_report"]
