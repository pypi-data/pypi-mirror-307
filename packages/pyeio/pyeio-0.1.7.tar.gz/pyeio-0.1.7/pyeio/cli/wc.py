import typer

app = typer.Typer(name="wc")


@app.callback()
def callback():
    """
    Based on the `wc` utility (see `man wc` for docs), with various optimizations.
    """
    ...
