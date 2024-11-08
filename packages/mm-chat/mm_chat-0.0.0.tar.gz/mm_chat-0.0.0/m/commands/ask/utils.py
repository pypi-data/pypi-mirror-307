from sys import stdin

from typer import Exit


def _get_session():
    from prompt_toolkit import PromptSession

    return PromptSession()


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
