import subprocess
from typing import Callable


def clear_screen() -> None:
    subprocess.run("clear", shell=True, check=True)


def star(n: int) -> None:
    print("*" * n)


def padding(lines: int = 1) -> None:
    print("\n" * lines)


def star_box(text: str) -> None:
    length = len(text)
    print("*" * (length + 4))
    print("*" + " " * (length + 2) + "*")
    print(f"* {text} *")
    print("*" + " " * (length + 2) + "*")
    print("*" * (length + 4))


def prompt_for_input(
    prompt: str, *, as_type: type = str, validator_func: Callable[[str], bool] = None
) -> any:
    """
    Validator func returns True if input passes validation.
    """
    user_input = None
    user_error = None
    while user_input is None:
        if user_error is not None:
            star_box(user_error)
            padding()
        resp = input(f"{prompt}\n\n> ")
        try:
            if validator_func is not None and not validator_func(resp):
                user_error = "input did not pass validation"
                clear_screen()
                continue
            user_input = as_type(resp)
        except Exception:
            user_error = f"input value must be {as_type}"
            clear_screen()
    return user_input
