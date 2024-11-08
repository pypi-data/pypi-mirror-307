from sys import stdin

from promplate.prompt.chat import Message, assistant, system, user
from typer import Argument, Typer

from .impl import default_model, get_client
from .utils import get_user_message

app = Typer()


@app.command()
def ask(message: str = Argument(""), model: str = default_model):
    if not message:
        message = get_user_message()

    messages: list[Message] = [user > message]
    if not stdin.isatty():
        messages.insert(0, system > stdin.read())

    while True:
        out = ""
        for i in get_client().generate(messages, model=model):
            out += i
            print(i, end="", flush=True)
        print()

        messages.append(assistant > out)

        messages.append(user > get_user_message())
