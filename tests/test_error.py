from unittest.mock import patch
from rich.console import Console
from oss_stats.error import error


def test_error():
    test_console = Console(
        stderr=True
    )  # we need to create a test console and mock it with patch

    # replace the current err_console with our test_console, rerouting it
    with patch("oss_stats.error.err_console", new=test_console):
        with test_console.capture() as capture:  # capture the console output
            error("Bad error.")
    str_output = capture.get()  # collect the capture

    assert (
        "Bad error." in str_output
    ), (  # check to see if the capture contains the phrase "Bad Error"
        f"The error 'Bad error' is not processed in the printed error output."
    )
