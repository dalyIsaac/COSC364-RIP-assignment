from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Any

DEBUG_MODE = False

pool = ThreadPoolExecutor()


def logger(*output_args: Any, is_debug=False):
    """Custom logging solution."""
    # `*output_args` collects all the arguments to this function
    # which are not keyword arguments.
    output = ""
    for arg in output_args:
        output += str(arg)
    if is_debug and DEBUG_MODE:
        print(f"{datetime.now()} [DEBUG] {output}")
    elif is_debug is False:
        print(output)
