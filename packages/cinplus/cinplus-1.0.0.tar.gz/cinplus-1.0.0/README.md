# CinPlus

`CinPlus` (short for `Console Input Plus`) is a Python module that extends the basic input function with 16 different parameters and many combinations. It is inspired by `pwinput` and many other modules. It helps enhance user input experience.

## Installation

To use the `CinPlus` module, simply execute this command on your terminal:
```bash
pip install cinplus
```

## Function Parameters

```python
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
)
```

## Usage Example

```python
import cinplus

cinplus.custominput(
    "Enter your password: ", # The prompt
    8, # Max characters: 8.
    True, # Input length has to be equal to limit.
    True, # Is masked (hidden).
    "*", # The mask to hide each character with.
    True, # Have a shortcut to clear the input.
    24, # The shortcut key in ASCII code to clear the input with. Ctrl+X
    'upper', # The input is uppercase-sensitive.
    (255, 128, 0), # The RGB code to color the prompt with.
    (0, 0, 255), # The RGB code to color the input with.
    True, # Have a shortcut to break the input loop.
    3, # The shortcut key in ASCII code to break the input loop with. Ctrl+C
    False, # Don't raise a KeyboardInterrupt error when interrupt key pressed.
    True, # Check if the input is empty.
    None, # No Regex pattern to match the example with.
    True, # Remove any whitespaces from the input.
)
```

## License

This module is licensed under the Mozilla Public License 2.0. For more details, please refer to the LICENSE file.