from typing import Optional, List, Dict, Any, Union
from .helpers import *
from .pauli_container import PauliContainer
from .random_measurement import RandomShadow
from .qiskit_utils import Mole

class QCumulant:
    """
    Compute expectation values for Pauli strings using Cumulant expansion and non-crossing partitioning.
    """
    
    def __init__(self,
                 protocol: Optional[Union[RandomShadow, Mole]] = None,
                 PauliObj: Optional[PauliContainer] = None,
                 measure_basis: Optional[List[Union[str, List[int]]]] = None,
                 measure_outcome_bits: Optional[List[Union[str, List[int]]]] = None,
                 partitions: Optional[List[List[List[int]]]] = None):
        """
        Initialize QCumulant class.

        Parameters
        ----------
        protocol : Optional[Union[RandomShadow, Mole]]
            Provide either a `RandomShadow` or `Mole` object from qumeas.
        PauliObj : Optional[PauliContainer]
            If protocol is not provided, `PauliContainer` object can be passed in. Expectation values can be computed using only the state vector is outbits are not provided along with `PauliObj`.
        measure_basis: List[Union[str, List[int]]]
            Measurement basis. Either list of Pauli operators (strings) or list of list of int representing Paulis, with 1 = 'X', 2 = 'Y', and 3 = 'Z'.
        measure_outcome_bits: List[Union[str, List[int]]]
            Measurement outcome (classical bits). Either a list of string or list of list of int. Binary bits can be passed in as string (e.g. ['0011', '0010']. Also, supports a list, e.g. [[0, 0, 1, 1], [0, 0, 1, 0]] or in this format: [[1, 1, -1, -1],[1, 1, -1, 1]].
        partitions : Optional[List[List[List[int]]]]
            Provide your partitions of `protocol.PauliObj.pauli_list` or `PauliObj.pauli_list`    

        """
        
        # Initialize protocol attributes
        self._initialize_protocol_attributes(protocol, PauliObj)
        
        if measure_basis is not None and measure_outcome_bits is not None:
            measure_basis, measure_outcome_bits = process_measure_bits(measure_basis, measure_outcome_bits)
            self.outbits = [measure_basis, measure_outcome_bits]

        if self.PauliObj.state_vector is None and self.outbits is None:
            raise ValueError("Requires either a state vector or measurment classical bits in Qcumulant")

        self.partitions = partitions

    def _initialize_protocol_attributes(self, protocol, PauliObj):
        
        if isinstance(protocol, (RandomShadow, Mole)):
            self.PauliObj = protocol.PauliObj
        elif isinstance(PauliObj, PauliContainer):
            self.PauliObj = PauliObj
        else:
            raise TypeError(
                "Neither 'protocol.PauliObj' nor 'PauliObj' is an instance of PauliContainer."
                )

        if isinstance(protocol, Mole) or isinstance(PauliObj, PauliContainer):
            self._process_pauli_string()
        
        if isinstance(protocol, RandomShadow):
            self.outbits = protocol.outbits

    def _process_pauli_string(self):
        from .helpers import string2int

        if isinstance(self.PauliObj.pauli_list[0], str):
            self.PauliObj.pauli_list = [string2int(_) for _ in self.PauliObj.pauli_list]
        elif isinstance(self.PauliObj.pauli_list[0], list) and all(isinstance(_, int) for _ in self.PauliObj.pauli_list[0]):
            pass
        else:
            raise TypeError(
                "PauliObj.pauli_list elements must be either str or a list of int")

    def generate_partitions(self, max_size=4, num_threads=1):
        """
        Generate non-crossing partitions for Pauli strings in `PauliObj` (or `protocol.PauliObj`).

        Parameters
        ----------
        max_size : int, optional
            Maximum block size for non-crossing partitions (default is 4).
        num_threads : int, optional
            Number of threads to use for partition generation (default is 1).

        Raises
        ------
        ValueError
            If `PauliObj.pauli_list` is empty.
        """
        from qumeas.libmeas import generate_partition_non_crossing
        
        if not self.PauliObj.pauli_list:
            raise ValueError("pauli_list is required for generating partitions.")
        
        non_ilist_full = [
            [idx for idx, i in enumerate(ham_string) if i != 'I' and i != 0]
            for ham_string in self.PauliObj.pauli_list
        ]
        self.non_ilist_full = non_ilist_full
        
        # Generate partitionings & cumulants
        self.partitions = generate_partition_non_crossing(
            self.non_ilist_full, max_size, num_threads)
        
        self._generate_unique_partitions()


    def _generate_unique_partitions(self):
        """Get unique partitions from partitions of a list of Pauli strings"""
        
        self.cdict = {}
        self.clist = []

        for idx, ham_string in enumerate(self.PauliObj.pauli_list):
            
            if not self.non_ilist_full[idx]:
                continue
            
            for block_list in self.partitions[idx]:
                for blocks in block_list:

                    # Get a compressed key (string)
                    tkey = sblock2ndict(blocks, ham_string)
                    tstring = sblock2ncumu(blocks, ham_string)
                    if tkey not in self.cdict:
                        self.cdict[tkey] = 0.0
                        self.clist.append([tkey, blocks, tstring])
                 
    def compute_expectation_bits(self, return_Elist = False):
        """
        Compute expectation values for the cumulant expansion using quantum measurement bits. This method uses `parition_expectation_bits` function in `libmeas` that uses asynchronous tasks to parallelize each cumulant expectation computation. Each cumulant expectation computation is OpenMP parallelized for optimal performance.

        Parameters
        ----------
        return_Elist : bool, optional
            If True, return both expectation value and a list of expectation values for each Pauli string (default is False).

        Returns
        -------
        Union[float, Tuple[float, List[float]]]
            The computed expectation value and optionally the list of expectation values.
        """
        from qumeas.libmeas import partition_expectation_bits

        cdict = partition_expectation_bits(self.outbits[0], self.outbits[1], self.clist)
        
        return self._compute_expectation(cdict, return_Elist)

    def compute_expectation_state(self, return_Elist = False):
        """
        Compute expectation values for the cumulant expansion using the state vector in `PauliObj` (or `protocol.PauliObj`). This method uses `parition_expectation_state` function in `libmeas` that uses asynchronous tasks to parallelize each cumulant expectation computation. Each cumulant expectation computation is OpenMP parallelized for optimal performance.

        Parameters
        ----------
        return_Elist : bool, optional
            If True, return both expectation value and a list of expectation values for each Pauli string (default is False).

        Returns
        -------
        Union[float, Tuple[float, List[float]]]
            The computed expectation value and optionally the list of expectation values.
        """
        from qumeas.libmeas import partition_expectation_state
        
        cdict = partition_expectation_state(self.PauliObj.Nqubit, self.PauliObj.state_vector,
                                           self.clist)
        return self._compute_expectation(cdict, return_Elist)

    def _compute_expectation(self, cdict, return_Elist):
        
        expectation_list = self._get_expect_list(cdict)
        expectation_val = self._compute_expectation_tot(expectation_list)
        
        return (expectation_val, expectation_list) if return_Elist else expectation_val


    def _compute_expectation_tot(self, expectation_list):
        return sum(coeff * expectation_list[idx] for idx, coeff in enumerate(self.PauliObj.pauli_list_coeff))


    def _get_expect_list(self, cdict):
              
        expec_list = []
        
        for idx, ham_string in enumerate(self.PauliObj.pauli_list):
                    
            if not len(self.non_ilist_full[idx]):
                expec_list.append(1.0)
                continue
            
            sum_expect = 0.0                
            for block_list in self.partitions[idx]:
                
                expect_part = 1.0               
                for blocks in block_list:                    
                    tkey = sblock2ndict(blocks, ham_string)
                    expect_part *= cdict[tkey]                    
                sum_expect += expect_part
                
            expec_list.append(sum_expect)
        
        return expec_list
