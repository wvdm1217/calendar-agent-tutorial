from rich import print
from typer import Typer

app = Typer()

@app.command()
def hello(name: str):
    """Say hello to NAME."""
    print(f"Hello {name}!")