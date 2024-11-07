
"""
A wrapper for the py-getch module, that provides a C-style getch implementation.

Author: Raghuram Ramanujan
"""
import getch


def get_char():
    return getch.getch()
