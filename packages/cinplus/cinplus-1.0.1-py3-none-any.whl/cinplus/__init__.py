from msvcrt import getch as _getch  # For getting a single key press.
from os import system as _system  # For initializing colors.
from re import match as _match  # For matching Regex patterns.


def custominput(  # This is the main function.
    text: str = "",  # The prompt for the input.
    limit: int = None,  # Maximum amount of characters.
    exact: bool = False,  # Does the length of the input have to be the same as the limit?
    masked: bool = False,  # Will the input be hidden with a mask?
    mask: str = "*",  # The mask to hide the input with. Only used if `masked` parameter is set to True.
    clear: bool = True,  # Will there be a shortcut key to clear the input?
    cvk: int = 24,  # The shortcut key in ASCII code to clear the input with. Only used if `clear` parameter is set to True. Default key is Ctrl+X.
    case: str = None,  # Is the input case-sensitive?
    color: tuple = (
        192,  # R(ed)
        192,  # G(reen)
        192,  # B(lue)
    ),  # The RGB color for the prompt. Only supported on terminals with 24-bit True Color support.
    incolor: tuple = (
        192,  # R(ed)
        192,  # G(reen)
        192,  # B(lue)
    ),  # The RGB color for the input. Only supported on terminals with 24-bit True Color support.
    interrupt: bool = True,  # Will Ctrl+C break the loop?
    ivk: int = 3,  # The shortcut key in ASCII code to break the input with. Only used if `interrupt` parameter is set to True. Default key is Ctrl+C.
    rki: bool = False,  # Raise a KeyboardInterrupt when interrupted. Only used if `interrupt` parameter is set to True.
    empty: bool = False,  # Will it check if the string is empty?
    pattern: str = None,  # The Regex pattern to match the input with.
    strip: bool = False,  # Will it remove any whitespaces in the input?
):
    keys = []  # This variable is for storing the keys pressed.
    _system("")  # To initialize the 24-bit True Color codes.
    print(  # Print the prompt along with the specified colors.
        f"\033[38;2;{color[0]};{color[1]};{color[2]}m{text}\033[0m\033[38;2;{incolor[0]};{incolor[1]};{incolor[2]}m",
        end="",  # Do not print a newline.
        flush=True,  # Print immediately.
    )
    while True:
        key = ord(_getch())  # Get the pressed key in it's ordinal form.
        if (
            key == 13  # Check if the key pressed is the Enter key.
            and (
                not exact or len(keys) == limit
            )  # If `exact` parameter is True, check if the length of the input is the same as the limit.
            and (
                case is None
                or (  # If `case` parameter isn't None:
                    case == "lower" and "".join(keys).islower()
                )
                or (  # If `case` parameter is "lower":
                    case == "upper" and "".join(keys).isupper()
                )  # If `case` parameter is "upper":
            )
            and (
                not empty or keys
            )  # If `empty` parameter is set to True, check if the input is not empty.
            and (
                pattern is None or _match(pattern, "".join(keys))
            )  # If `pattern` parameter isn't None, check if the input matches the Regex pattern.
        ):
            break  # Exit the loop.
        elif key in (8, 127) and keys:  # If backspace/delete key pressed:
            keys.pop()  # Remove the last item from the "keys" list
            print(
                "\b \b", end="", flush=True
            )  # Remove the last character from the current line.
        elif (
            key == ivk and interrupt
        ):  # If Ctrl+C pressed and the `interrupt` parameter is set to True:
            if not rki:  # If the parameter `rki` is set to True:
                break  # Exit the loop.
            else:  # Else
                raise KeyboardInterrupt  # Raise a KeyboardInterrupt
        elif (
            key in (224, 0) and ord(_getch()) == 83 and keys
        ):  # If delete key (from Extended Keys) pressed:
            keys.pop()  # Remove the last item from the "keys" list
            print(
                "\b \b", end="", flush=True
            )  # Remove the last character from the current line.
        elif (
            key == cvk and clear and keys
        ):  # If break shortcut key pressed and the `clear` parameter is set to True:
            print(
                f"\r{' '*(len(text)+len(keys))}\r\033[38;2;{color[0]};{color[1]};{color[2]}m{text}\033[0m\033[38;2;{incolor[0]};{incolor[1]};{incolor[2]}m",
                end="",
                flush=True,
            )  # Refresh the prompt.
            keys = []  # Refresh the input.
        elif key >= 32 and (
            limit is None or len(keys) < limit
        ):  # Check if pressed key is a printable character and if the `limit` parameter is not set to None then check if the length of the input is less than the character limit:
            keys.append(chr(key))  # Append the key to the "keys" list.
            print(
                chr(key) if not masked else mask[0], end="", flush=True
            )  # Print the key if `masked` parameter is set to False else print the mask.
    print("\033[0m")  # Reset the colors.
    return "".join(keys).strip() if strip else "".join(keys)  # Return the input.
