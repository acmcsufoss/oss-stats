from rich.console import Console

err_console = Console(stderr=True)


def error(msg) -> None:
    err_console.print(f"[bold white on red]\n ERROR [/]\n\n{msg}")
