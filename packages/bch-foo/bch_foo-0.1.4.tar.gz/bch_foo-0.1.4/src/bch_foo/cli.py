"""Console script for bch_foo."""
import bch_foo

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for bch_foo."""
    console.print("XXXXXXXX cli")



if __name__ == "__main__":
    app()
