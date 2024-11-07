import os
import sys
from datetime import datetime
from typing import Callable

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H%M")

def mute(func : Callable) -> Callable:
    def muted_func(*args, **kwargs):
        stdout, stderr = sys.stdout, sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        result = func(*args, **kwargs)
        sys.stdout, sys.stderr = stdout, stderr
        return result
    return muted_func

def to_sci_notation(val : str | float | int) -> str:
    try:
        val = float(val)
        display_val = f'{val:.1e}'
    except:
        display_val = val
    return  display_val
