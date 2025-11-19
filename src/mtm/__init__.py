# src/mtm/__init__.py
from .tape import Tape, Direction
from .machine import MultiTapeTuringMachine

__all__ = ["Tape", "Direction", "MultiTapeTuringMachine"]
