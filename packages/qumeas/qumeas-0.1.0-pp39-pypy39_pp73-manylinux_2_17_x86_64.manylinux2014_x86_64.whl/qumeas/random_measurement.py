from typing import Optional, List, Any
from .pauli_container import PauliContainer
from .state_prep import StatePreparation

class RandomShadow:
    """
    Class for estimating expectation values of Pauli strings using classical shadow tomography (randomized measurement basis).

    Attributes
    ----------
    PauliObj : PauliContainer
        `PauliContainer` object holding Pauli strings, coefficients, state vector, and number of qubits.
    basis : Optional[List[List[int]]]
        Basis for measurements in classical shadow tomography.
    state_prep : Optional[StatePreparation]
        State preparation object, can be an instance of StatePreparation or qiskitStatePreparation.
    outbits : Optional[List[List[List[int]]]]
        Measurement output bits. Contains list of measurement basis and another list of the corresponding classical bits. In the measurement basis, X,Y,Z are represented as integers 1,2,3 respectively.
    """
    
    def __init__(self,
                 mole: Optional[Any] = None,
                 PauliObj: Optional[PauliContainer] = None,
                 state_prep: Optional[StatePreparation] = None,
                 basis: Optional[List[List[int]]] = None
                 ):
        """
        Initialize RandomShadow class.

        Parameters
        ----------
        mole : Optional[Any]
            `Mole` object that contains a `PauliContainer` instance.
        PauliObj : Optional[PauliContainer]
            `PauliContainer` object holding Pauli strings, coefficients, state vector, and number of qubits.
        state_prep : Optional[StatePreparation]
            State preparation object, can be an instance of StatePreparation or qiskitStatePreparation.
        basis : Optional[List[List[int]]]
            Basis for measurements in classical shadow tomography.

        Raises
        ------
        TypeError
            If neither `mole.PauliObj` nor `PauliObj` is a PauliContainer instance.
        """
        
        if hasattr(mole, 'PauliObj') and isinstance(mole.PauliObj, PauliContainer):
            self.PauliObj = mole.PauliObj
        elif isinstance(PauliObj, PauliContainer):
            self.PauliObj = PauliObj
        else:
            raise TypeError(
                "Neither 'mole.PauliObj' nor 'PauliObj' is an instance of PauliContainer.")

        self._process_pauli_string() 
        self.basis = basis            
        self.state_prep = state_prep
        self.outbits = None

    def _process_pauli_string(self):
        from .helpers import string2int
        
        if isinstance(self.PauliObj.pauli_list[0], str):
            self.PauliObj.pauli_list = [string2int(_) for _ in self.PauliObj.pauli_list]
        elif isinstance(self.PauliObj.pauli_list[0], list) and all(isinstance(_, int) for _ in self.PauliObj.pauli_list[0]):
            pass
        else:
            raise TypeError(
                "PauliObj.pauli_list elements must be either str or a list of int")
        
        
    def get_basis(self,
                  M: int,
                  seed: Optional[int] = None):
        """
        Generate a random basis for measurements.

        Parameters
        ----------
        M : int
            Number of random basis to generate.
        seed : Optional[int], default=None
            Random seed for reproducibility.
        """
        
        self.basis = self._generate_random_basis(M, seed = seed)
        

    def _generate_random_basis(self, M:int,
                               seed: Optional[int] = None):
        import numpy
        
        basis = []
        for i in range(M):            
            if seed is not None:
                numpy.random.seed(seed+i)
            basis.append([int(numpy.random.choice([1,2,3])) for _ in range(self.PauliObj.Nqubit)])
        
        return basis        

    def measure(self,
                shots: int = 1,
                M: int = 100,
                seed: Optional[int] = None,
                nproc: Optional[int] = 1
                ):

        """
        Perform measurements using the state preparation object (`state_prep`).

        Parameters
        ----------
        shots : int, default=1
            Number of measurement shots. Currently, only supports for one shot measurements.
        M : int, default=100
            Number of random basis in classical shadow tomography
        seed : Optional[int], default=None
            Random seed for reproducibility.
        nproc : Optional[int], default=1
            Number of processes for parallelization accross measurement bases. Each measurement basis can be processed in parallel across multiple processes, with each measurement further parallelized using OpenMP for optimal performance.

        Returns
        -------
        float
            Computed expectation value.
        """
        
        self._prepare_basis_and_state(M, seed)

        if nproc == 1:
            bitplist, bitoutlist = self._serial_measurement(shots, seed=seed)
        else:
            bitplist, bitoutlist = self._parallel_measurement(shots, nproc, seed=seed)
        
        self.outbits = [bitplist, bitoutlist]#, bitcount]

        expectation_val = self.compute_expectation(bitplist, bitoutlist)#, bitcount)
        return expectation_val
    
    def _prepare_basis_and_state(self, M: int,
                                 seed: Optional[int] = None):
        """Generate basis and set state_prep to default qiskitStatePreparation if not set."""
        from qumeas.qiskit_utils import qiskitStatePreparation
        
        if not self.basis:
            self.get_basis(M, seed)
            
        if not self.state_prep and self.PauliObj.Nqubit:
            self.state_prep = qiskitStatePreparation(Nqubit=self.PauliObj.Nqubit, state_vector=self.PauliObj.state_vector)
        

    def _serial_measurement(self, shots: int, seed: Optional[int] = None):
        """Perform measurement in serial mode."""
        
        bitplist, bitoutlist, bitcount = [], [], []
        
        for pbasis in self.basis:
            noutbit = self.state_prep.measure(pbasis, shots=shots, seed = seed)
            for outbit_ in noutbit:
                bitplist.append(pbasis)
                bitoutlist.append(outbit_[0])
                #bitcount.append(outbit_[1])
                
        return bitplist, bitoutlist#, bitcount

    def _parallel_measurement(self, shots: int, nproc: int, seed: Optional[int] = None):
        """Perform measurement in parallel using multiprocessing."""
        from multiprocessing import Pool
        
        results = []
        pool = Pool(nproc)
        outresult = []
        for measure_ in range(len(self.basis)):
            result = pool.apply_async(self.state_prep.measure, [self.basis[measure_], shots, seed])
            results.append(result)
    
        [outresult.append(result.get()) for result in results]
        pool.close()
        bitplist, bitoutlist, bitcount = [], [], []
        
        for pidx, pbasis in enumerate(self.basis):
            for outbit_ in outresult[pidx]:
                bitplist.append(pbasis)
                bitoutlist.append(outbit_[0])
                #bitcount.append(outbit_[1])
                
        return bitplist, bitoutlist#, bitcount

    def compute_expectation(self, measure_basis, measure_outcome_bits):
        """Compute the expectation value from measurement bits.

        Parameters
        ----------
        measure_basis: List[Union[str, List[int]]]
            Measurement basis. Either list of Pauli operators (strings) or list of list of int representing Paulis, with 1 = 'X', 2 = 'Y', and 3 = 'Z'.
        measure_outcome_bits: List[Union[str, List[int]]]
            Measurement outcome (classical bits). Either a list of string or list of list of int. Binary bits can be passed in as string (e.g. ['0011', '0010']. Also, supports a list, e.g. [[0, 0, 1, 1], [0, 0, 1, 0]] or in this format: [[1, 1, -1, -1],[1, 1, -1, 1]].

        Returns
        -------
        float
            Total expectation value.
        """
        from qumeas.libmeas import compute_expectations_basis
        from .helpers import process_measure_bits

        bitplist, bitoutlist = process_measure_bits(measure_basis, measure_outcome_bits)
        expectation_list = compute_expectations_basis(
            bitplist, bitoutlist, self.PauliObj.pauli_list, self.PauliObj.Nqubit
        )
        return sum(coeff * expectation_list[pdx] for pdx, coeff in enumerate(self.PauliObj.pauli_list_coeff))
