from typing import Optional, List, Any
from qumeas.pauli_container import PauliContainer

class Mole:
    """
    A class representing a molecular system using Qiskit functionalities.

    Attributes
    ----------
    PauliObj : PauliContainer
        Container for Pauli strings, coefficients, state vector, and number of qubits.
    Hamiltonian : sparse matrix
        The Hamiltonian of the molecule, mapped to a qubit basis.
    """

    def __init__(self,
                 atom: Optional[str] = None,
                 molecule: Optional[str] = None,
                 basis: str = 'sto-3g',
                 charge: int = 0,
                 spin: int = 0,
                 qubit_mapper: str = 'jw',
                 frozen: bool = True,
                 norb: Optional[int] = None,
                 nelec: Optional[int] = None,
                 orb_indices: Optional[List[int]] = None
                 ):
        """
        Initialize the Mole class with molecular properties and quantum simulation parameters. Uses Qiskit's PySCFDriver.

        Parameters
        ----------
        atom : Optional[str]
            Cartesian coordinates for the geometry as a string, or `None` if `molecule` is provided.
        molecule : Optional[str]
            Name of the molecule (e.g., 'h2', 'lih'); overrides `atom` if specified. Uses predefined geometry of the molecule.
        basis : str, default='sto-3g'
            Quantum chemitry basis set.
        charge : int, default=0
            Charge.
        spin : int, default=0
            Molecular spin. 
        qubit_mapper : str, default='jw'
            Qubit mapping method ('jw' for Jordan-Wigner, 'bk' for Bravyi-Kitaev).
        frozen : bool, default=True
            Whether to freeze core orbitals.
        norb : Optional[int]
            Number of active spatial orbitals.
        nelec : Optional[int]
            Number of active electrons.
        orb_indices : Optional[List[int]]
            Indices of orbitals to include in the active space.

        Raises
        ------
        ValueError
            If neither `atom` nor `molecule` is provided, or if `qubit_mapper` is not 'jw' or 'bk'.
        """
        
        self.PauliObj = PauliContainer()
        
        if molecule:
            atom = self._get_atom(molecule)
        elif atom is None:
            raise ValueError("Either 'atom' or 'molecule' must be provided.")
        
        self.qubit_mapper = qubit_mapper.lower()
        if self.qubit_mapper not in ['jw', 'bk']:
            raise ValueError("qubit_mapper must be 'jw' (Jordan-Wigner) or 'bk' (Bravyi-Kitaev).")
        
        self.basis = basis
        self.charge = charge
        self.spin = spin
        self.frozen = frozen
        self.norb = norb
        self.nelec = nelec
        self.orb_indices = orb_indices

        self._initialize_driver(atom)

    def _initialize_driver(self, atom: str):
        from qiskit_nature.second_q.drivers import PySCFDriver
        from qiskit_nature.second_q.transformers import FreezeCoreTransformer, ActiveSpaceTransformer
        from qiskit_nature.units import DistanceUnit

        # Using pyscf
        driver = PySCFDriver(atom=atom,
                             unit=DistanceUnit.ANGSTROM,
                             charge=self.charge,
                             spin=self.spin,
                             basis=self.basis)
        problem = driver.run()
        
        if self.frozen:
            fc_transformer = FreezeCoreTransformer()
            problem = fc_transformer.transform(problem)
            
        if self.norb is not None and self.nelec is not None:
            if self.orb_indices is None:
                as_transformer = ActiveSpaceTransformer(self.nelec, self.norb)
            else:
                as_transformer = ActiveSpaceTransformer(self.nelec, self.norb, self.orb_indices)
            problem = as_transformer.transform(problem)
            
        self._map_hamiltonian(problem)


    def _map_hamiltonian(self, problem):
        
        hamiltonian = problem.hamiltonian
        second_q_op = hamiltonian.second_q_op()

        mapper = self._get_mapper(self.qubit_mapper)
        mapped_Ham = mapper.map(second_q_op)
        
        self.PauliObj.pauli_list = mapped_Ham.paulis.to_labels()
        self.PauliObj.pauli_list_coeff = mapped_Ham.coeffs.real
        self.PauliObj.Nqubit = len(self.PauliObj.pauli_list[0])

        self.Hamiltonian = mapped_Ham.to_matrix(sparse = True)
        self._get_state_vector()

        
    def _get_state_vector(self):
        import scipy
        
        eigE_, eigV_ = scipy.sparse.linalg.eigsh(self.Hamiltonian, which='SA', k=1)
        self.PauliObj.total_energy = eigE_[0]
        self.PauliObj.state_vector = eigV_[:,0]
        

    def _get_mapper(self, mapper_type: str):
        from qiskit_nature.second_q.mappers import BravyiKitaevMapper, JordanWignerMapper
        
        mapper_type = mapper_type.lower()        
        if mapper_type == 'bk':
            return BravyiKitaevMapper()
        elif mapper_type == 'jw':
            return JordanWignerMapper()
        else:
            raise ValueError(f"Unsupported qubit mapper: {mapper_type}. Use 'jw' or 'bk'.")
        

    def _get_atom(self, molecule: str):

        molecule_dict = {
            'h2': "H 0 0 0; H 0 0 0.735",
            'lih': "Li 0 0 0; H 0 0 1.45",
            'h2o': 'O 0.0 0.0 0.0; H 0.757 0.586 0.0; H -0.757 0.586 0.0',
            'beh2': 'H 0.0 0.0 -1.4; Be 0.0 0.0 0.0; H 0.0 0.0 1.4',
            'n2': "N 0 0 0; N 0 0 1.1",
            'o2': "O 0 0 0; O 0 0 1.16",
            'nh3': 'H 0.0 0.0 0.0; N 1.0296 0.0 0.0; H 1.0296 1.0296 0.0; H 1.0296 1.0296 -1.0296',
            'co': 'C 0.0 0.0 0.648; O 0.0 0.0 -0.486',
            'ch4': 'C 0.0 0.0 0.0; H 0.885 0.0 0.626; H 0.0 -0.885 -0.626; H 0.0 0.885 -0.626; H -0.885 0.0 0.626',
            'c6h6': 'C 0.0 1.3968 0.0; C 0.0 -1.3968 0.0; C 1.2097 0.6984 0.0; C -1.2097 -0.6984 0.0; C -1.2097 0.6984 0.0; C 1.2097 -0.6984 0.0; H 0.0 2.4842 0.0; H 2.1514 1.2421 0.0; H -2.1514 -1.2421 0.0; H -2.1514 1.2421 0.0; H 2.1514 -1.2421 0.0; H 0.0 -2.4842 0.0',
            'b2': 'B 0.0 0.0 0.0; B 0.0 0.0 1.59',
            'nh4+': 'N -1.1255 0.6901 -0.1099; H -0.2133 1.1642 0.07; H -1.2866 0.6009 0.9425; H -1.9221 0.0372 -0.2638; H -0.3508 -0.3076 -0.3863'
        }

        if molecule in molecule_dict:
            return molecule_dict[molecule]
        else:
            raise ValueError(f"Molecule '{molecule}' is not defined in the molecular dictionary.")
