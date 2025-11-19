# src/mtm/tape.py
from enum import IntEnum
from typing import Dict


class Direction(IntEnum):
    LEFT = -1
    RIGHT = 1
    STAY = 0


class Tape:
    """
    Representa una cinta infinita en ambas direcciones con un cabezal.

    Los símbolos se almacenan en un diccionario índice -> símbolo, para
    representar sólo las celdas no blancas.
    """

    def __init__(self, blank: str = "_", initial_input: str = "") -> None:
        self.blank: str = blank
        self.cells: Dict[int, str] = {}
        for i, ch in enumerate(initial_input):
            self.cells[i] = ch
        self.head: int = 0

    def read(self) -> str:
        """Lee el símbolo bajo el cabezal."""
        return self.cells.get(self.head, self.blank)

    def write(self, symbol: str) -> None:
        """Escribe símbolo bajo el cabezal (si es blanco, limpia la celda)."""
        if symbol == self.blank and self.head in self.cells:
            del self.cells[self.head]
        else:
            self.cells[self.head] = symbol

    def move(self, direction: int) -> None:
        """
        Mueve el cabezal una celda.

        direction debe ser uno de:
            Direction.LEFT (-1), Direction.RIGHT (1), Direction.STAY (0)
        """
        self.head += int(direction)

    def __str__(self) -> str:
        """Vista amigable de la cinta (para depuración)."""
        if not self.cells:
            return f"[{self.blank}]"
        indices = set(self.cells.keys()) | {self.head}
        min_i = min(indices)
        max_i = max(indices)
        out = []
        for i in range(min_i, max_i + 1):
            ch = self.cells.get(i, self.blank)
            if i == self.head:
                out.append(f"[{ch}]")
            else:
                out.append(f" {ch} ")
        return "".join(out)
