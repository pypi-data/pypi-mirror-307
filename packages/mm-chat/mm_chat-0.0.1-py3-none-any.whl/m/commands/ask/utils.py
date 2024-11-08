from contextlib import redirect_stderr
from functools import cache
from io import StringIO
from sys import stdin

from typer import Exit


@cache
def _get_session():
    from prompt_toolkit import PromptSession
    from prompt_toolkit.input import create_input

    with redirect_stderr(io := StringIO()):
        session = PromptSession()

    if "Input is not a terminal (fd=0)" in io.getvalue():  # Warning: Input is not a terminal (fd=0).
        return PromptSession(input=create_input(open("/dev/tty")))  # noqa: PTH123, SIM115

    return session


def prompt(*args, **kwargs):
    return _get_session().prompt(*args, **kwargs)


def _input(message: str):
    if stdin.isatty():
        return input(message)

    return prompt(message)


def get_user_message():
    print()

    message = _input(" > ")
    if not message:
        print()
        raise Exit

    print()

    return message
