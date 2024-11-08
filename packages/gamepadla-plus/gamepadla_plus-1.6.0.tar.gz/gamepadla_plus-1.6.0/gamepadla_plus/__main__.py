import typer

from gamepadla_plus.cli import app
from gamepadla_plus.gui import gui


@app.callback(invoke_without_command=True)
def start_gui(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        gui()


def run():
    app()


if __name__ == "__main__":
    app()
