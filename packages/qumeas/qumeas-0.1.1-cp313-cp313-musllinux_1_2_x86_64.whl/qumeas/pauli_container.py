from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PauliContainer:
    """
    Container for managing Pauli string data and state vector.

    Attributes
    ----------
    Nqubit : Optional[int]
        Number of qubits.
    pauli_list : List[str]
        List of Pauli strings.
    pauli_list_coeff : List[float]
        Coefficients corresponding to each Pauli string in `pauli_list`.
    state_vector : Optional[List[float]]
        State vector, if available.
    total_energy : Optional[float]
        Total ground state energy.
    """
    Nqubit: Optional[int] = None
    pauli_list: List[str] = field(default_factory=list)
    pauli_list_coeff: List[float] = field(default_factory=list)
    state_vector: Optional[List[float]] = None
    total_energy: Optional[float] = None
