from typing import Optional, List, Any
from qumeas.state_prep import StatePreparation

class qiskitStatePreparation(StatePreparation):
    """
    State preparation class using Qiskit
    """
    
    def __init__(self,
                 Nqubit:Optional[int] = None,
                 state_vector: Optional[List[float]] = None,
                 state_preparation_circuit: Optional['QuantumCircuit'] = None,
                 backend: Optional[Any] = None
                 ):
        """
        Initialize the qiskitStatePreparation class.

        Parameters
        ----------
        Nqubit : Optional[int]
            Number of qubits.
        state_vector : Optional[List[float]]
            State vector. If `state_preparation_circuit` is not provided, state_vector is used for initialization.
        state_preparation_circuit : Optional['QuantumCircuit']
            Qiskit QuantumCircuit for state preparation.
        backend : Optional[Any]
            Qiskit backend. Defaults to `statevector` in `AerSimulator`
        """
        super().__init__(Nqubit, state_vector, state_preparation_circuit, backend)

    def get_measurement_circuit(self, pauli_string: List[str]):
        """
        Generate a measurement circuit based on a Pauli string.

        Parameters
        ----------
        pauli_string : List[str]
            Pauli string for which expectation value is sought.

        Returns
        -------
        QuantumCircuit
            Quantum circuit with measurement gates
        """
        import numpy
        from qiskit import QuantumCircuit
        
        measurement_circuit = QuantumCircuit(self.Nqubit, self.Nqubit)
        for idx, i in enumerate(pauli_string):
            if i == 'X' or i == 1:
                measurement_circuit.h(idx)
            elif i == 'Y' or i == 2:
                measurement_circuit.h(idx)
                measurement_circuit.p(-numpy.pi / 2., idx)
                
        return measurement_circuit
        
    def get_circuit(self,
                    measurement_circuit: Optional['QuantumCircuit'] = None,
                    ):
        """
        Construct the quantum circuit for state preparation, including measurement gates.

        Parameters
        ----------
        measurement_circuit : Optional['QuantumCircuit']
            Qiskit QuantumCircuit object with measurement gates.

        Returns
        -------
        QuantumCircuit
            Quantum circuit (Qiskit QuantumCircuit) for state preparation and measurement.
        """
        from qiskit import QuantumCircuit

        qcircuit = QuantumCircuit(self.Nqubit, self.Nqubit)

        # Construct quantum circuit
        if self.state_vector is not None:
            qcircuit.initialize(self.state_vector,
                                reversed(range(self.Nqubit)))            
        elif self.state_preparation_circuit is not None:
            qcircuit = qcircuit.compose(self.state_preparation_circuit)

        # Add measurement circuit if provided
        if measurement_circuit is not None:
            qcircuit = qcircuit.compose(measurement_circuit)
        qcircuit.measure(reversed(range(self.Nqubit)), range(self.Nqubit))

        return qcircuit


    def measure(self,
                pauli_string: List[str],
                shots: Optional[int] = 1,
                seed: Optional[int] = None
                ):
        """
        Measure the quantum state to estimate expectation value of `pauli_string`

        Parameters
        ----------
        pauli_string : List[str]
            Pauli string to measure.
        shots : Optional[int], default=1
            Number of measurement shots. `RandomShadow` as well as `QCumulant` only supports one shot measurements for now.
        seed : Optional[int], default=None
            Seed for the simulator.

        Returns
        -------
        List[Tuple[List[int], int]]
            List of tuples containing classical measurement bits and their counts.
        """
        from qiskit import transpile
        from qiskit_aer import AerSimulator
        
        measurement_circuit = self.get_measurement_circuit(pauli_string)
        qcircuit = self.get_circuit(measurement_circuit = measurement_circuit)
        
        if self.backend is None:
            self.backend = AerSimulator(method = 'statevector', seed_simulator=seed)
            
        qcircuit = transpile(qcircuit, self.backend, optimization_level=0)
        res = self.backend.run(qcircuit, shots = shots).result()
        counts = res.get_counts()
        
        outbit_list = [
            ([1 if bit == '0' else -1 for bit in bitstring], count)
            for bitstring, count in counts.items()
        ]

        return outbit_list
