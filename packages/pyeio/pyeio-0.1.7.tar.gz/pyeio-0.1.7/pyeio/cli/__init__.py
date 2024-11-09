import typer
from pathlib import Path
from pyeio import opt


app = typer.Typer(name="eio")


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """
    todo
    """
    if ctx.invoked_subcommand is None:
        print("todo: add name and version")


# @app.command()
# def wc()


def count_lines(content: str) -> int:
    return content.count("\n")


def count_words(content: str) -> int:
    return len(content.split())


def count_bytes(content: str) -> int:
    return len(content.encode())


def count_characters(content: str) -> int:
    return len(content)


def longest_line_length(content: str) -> int:
    return max(len(line) for line in content.splitlines()) if content else 0


@app.command()
def wc(
    # libxo: bool = typer.Option(False, "--libxo", help="Generate output via libxo(3)"),
    l: bool = typer.Option(False, "-l", help="Count lines"),
    # w: bool = typer.Option(False, "-w", help="Count words"),
    # c: bool = typer.Option(False, "-c", help="Count bytes"),
    # m: bool = typer.Option(False, "-m", help="Count characters"),
    # L: bool = typer.Option(False, "-L", help="Find longest line"),
    files: list[Path] = typer.Argument(
        None, exists=True, dir_okay=False, readable=True
    ),
):
    """Display line, word, byte, and character counts for files."""
    for file in files:
        result = list()
        if l:
            n_lines = opt.count_lines_in_file(file)
            result.append(str(n_lines))
        result.append(str(file) if file else "-")
        print("\t".join(result))

    # for file in files or [None]:  # Defaults to standard input if no files specified
    #     content = file.read_text() if file else typer.prompt("Enter text (EOF to end)")
    #     result = []

    #     if l:
    #         result.append(f"{count_lines(content)}")
    #     if w:
    #         result.append(f"{count_words(content)}")
    #     if c:
    #         result.append(f"{count_bytes(content)}")
    #     if m:
    #         result.append(f"{count_characters(content)}")
    #     if L:
    #         result.append(f"{longest_line_length(content)}")

    #     result.append(str(file) if file else "-")
    #     print("\t".join(result))
