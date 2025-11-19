# src/mtm/machine.py
from __future__ import annotations
from typing import Dict, Hashable, Iterable, List, Sequence, Tuple

from .tape import Tape, Direction


State = Hashable  # normalmente str o int
Symbol = str

# Tipo de clave de transición: (estado, (s1,...,sk))
TransitionKey = Tuple[State, Tuple[Symbol, ...]]

# Tipo de valor de transición: (new_state, (w1,...,wk), (m1,...,mk))
TransitionValue = Tuple[State, Tuple[Symbol, ...], Tuple[int, ...]]


class MultiTapeTuringMachine:
    """
    Simulador de Máquina de Turing de k-cintas.

    - states: conjunto de estados
    - input_alphabet: símbolos de entrada
    - tape_alphabet: símbolos de la cinta (incluye input_alphabet y blank)
    - blank: símbolo en blanco
    - transitions: dict que mapea
        (state, (s1,...,sk)) -> (new_state, (w1,...,wk), (m1,...,mk))
      donde mi ∈ {Direction.LEFT, Direction.RIGHT, Direction.STAY} o -1,0,1.
    """

    def __init__(
        self,
        states: Iterable[State],
        input_alphabet: Iterable[Symbol],
        tape_alphabet: Iterable[Symbol],
        blank: Symbol,
        transitions: Dict[TransitionKey, TransitionValue],
        start_state: State,
        accept_states: Iterable[State],
        reject_states: Iterable[State] | None = None,
        num_tapes: int = 1,
        initial_inputs: Sequence[str] | None = None,
    ) -> None:
        # Conjuntos básicos
        self.states = set(states)
        self.input_alphabet = set(input_alphabet)
        self.tape_alphabet = set(tape_alphabet)
        self.blank = blank

        # Transiciones
        self.transitions: Dict[TransitionKey, TransitionValue] = transitions

        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.reject_states = set(reject_states or [])

        self.num_tapes = num_tapes

        # Entradas iniciales por cinta
        if initial_inputs is None:
            initial_inputs = [""] * num_tapes
        if len(initial_inputs) != num_tapes:
            raise ValueError("initial_inputs debe tener longitud num_tapes.")

        # Crear cintas
        self.tapes: List[Tape] = [
            Tape(blank, initial_inputs[i]) for i in range(num_tapes)
        ]

        # Estado inicial
        self.current_state: State = start_state
        self.step_count: int = 0

    # ---------------- Métodos de utilidad ----------------

    def reset(self, initial_inputs: Sequence[str] | None = None) -> None:
        """Reinicia la máquina con nuevas entradas opcionales."""
        if initial_inputs is None:
            initial_inputs = ["" for _ in range(self.num_tapes)]

        if len(initial_inputs) != self.num_tapes:
            raise ValueError("initial_inputs debe tener longitud num_tapes.")

        self.tapes = [Tape(self.blank, s) for s in initial_inputs]
        self.current_state = self.start_state
        self.step_count = 0

    def get_configuration(self) -> dict:
        """Devuelve un snapshot de la configuración actual."""
        return {
            "state": self.current_state,
            "tapes": [str(t) for t in self.tapes],
            "step": self.step_count,
        }

    # ----------------- Paso único de simulación -----------------

    def step(self) -> str:
        """
        Ejecuta un paso de la TM.

        Devuelve:
            - 'RUNNING' si sigue en ejecución,
            - 'ACCEPT', 'REJECT' o 'HALT' si se detiene.
        """
        # Leer símbolos en todas las cintas
        read_symbols = tuple(t.read() for t in self.tapes)
        key: TransitionKey = (self.current_state, read_symbols)

        # Si no hay transición definida, la máquina se detiene
        if key not in self.transitions:
            if self.current_state in self.accept_states:
                return "ACCEPT"
            if self.current_state in self.reject_states:
                return "REJECT"
            return "HALT"

        new_state, write_symbols, moves = self.transitions[key]

        # Escribir
        for t, sym in zip(self.tapes, write_symbols):
            t.write(sym)

        # Mover cabezales
        for t, mv in zip(self.tapes, moves):
            t.move(mv)

        # Actualizar estado
        self.current_state = new_state
        self.step_count += 1

        # Comprobar estados especiales
        if self.current_state in self.accept_states:
            return "ACCEPT"
        if self.current_state in self.reject_states:
            return "REJECT"
        return "RUNNING"

    # --------------- Ejecución completa ----------------

    def run(self, max_steps: int = 10_000) -> str:
        """
        Ejecuta hasta detenerse o hasta max_steps.

        Devuelve el estado final: 'ACCEPT', 'REJECT', 'HALT' o 'RUNNING'
        (si se cortó por max_steps).
        """
        status = "RUNNING"
        while status == "RUNNING" and self.step_count < max_steps:
            status = self.step()
        return status
