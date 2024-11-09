import pytest
from qumeas import PauliContainer, RandomShadow, QCumulant

def test_random_measurement():
    # Test expectation value from randomized measurement protocol
    Pauli_strings = ['IIII', 'IIIZ', 'IIZI', 'IIZZ', 'IZII', 'IZIZ', 'YYII', 'YYIZ', 'XXII', 'XXIZ', 'ZIII', 'ZIIZ', 'IIYY', 'IZYY', 'IIXX', 'IZXX', 'YYYY', 'XXYY', 'YYXX', 'XXXX', 'ZIYY', 'ZIXX', 'IZZI', 'YYZI', 'XXZI', 'ZIZI', 'ZZII']
    Pauli_strings_coeff = [-0.72913365, 0.16199478, -0.01324373, 0.05413045, 0.16199478, 0.12444773, 0.01291061, 0.01153635, 0.01291061, 0.01153635, -0.01324373, 0.05706341, 0.01291061, 0.01153635, 0.01291061, 0.01153635, 0.00293297, 0.00293297, 0.00293297, 0.00293297, -0.00137435, -0.00137435, 0.05706341, -0.00137435, -0.00137435, 0.08479611, 0.05413045]
    basis = ['XYZX', 'ZYYZ', 'YYZY', 'ZXXZ', 'YYYY', 'ZYXY', 'ZZXX', 'YYYY', 'YZZX', 'ZXXY', 'YZXY', 'XZYX', 'XZZY', 'XZZX', 'ZXZZ', 'YZZZ', 'YXZZ', 'ZYZX', 'YXYY', 'ZXYZ', 'ZXXZ', 'XZXZ', 'ZXXX', 'XYZY', 'ZXYX', 'YZXY', 'ZXXY', 'ZZYX', 'XXXZ', 'ZZYX', 'ZZXY', 'ZZZX', 'YYYZ', 'ZXXY', 'ZYZY', 'YZXZ', 'YYYX', 'ZYZZ', 'ZZZX', 'XYYY', 'XYZX', 'ZYZZ', 'XZYY', 'ZZXX', 'XXZY', 'ZYYX', 'ZXXX', 'XZYX', 'YZZX', 'XZZZ', 'ZZXX', 'XYYZ', 'ZXZY', 'XZZY', 'XXXY', 'XXXX', 'ZYXZ', 'ZXYZ', 'YZYX', 'XZZY', 'ZXXZ', 'ZYZY', 'XXXY', 'YZZY', 'ZXXZ', 'YYZZ', 'ZYYZ', 'ZZYY', 'XZYZ', 'ZXZZ', 'ZYZY', 'YXZX', 'ZZXX', 'YZZY', 'ZXZY', 'XYXX', 'XZZX', 'YYXZ', 'ZYYY', 'XYYX', 'XXZX', 'ZXYY', 'ZYXY', 'ZZXZ', 'YZYX', 'YZZZ', 'XXZX', 'XZZZ', 'ZYXZ', 'XYYZ', 'XZZX', 'YXXY', 'XXXZ', 'ZYXX', 'XZZZ', 'YYXX', 'XXZY', 'XXYX', 'ZXYY', 'YZZX']
    bits = ['0101', '0111', '1000', '0001', '1011', '0000', '0100', '0100', '1101', '0010', '0101', '0111', '1100', '0101', '0001', '0101', '0001', '0001', '0010', '0111', '0001', '1111', '0100', '1100', '0110', '0111', '0010', '0110', '1111', '0111', '0101', '0100', '1001', '0000', '0000', '1101', '0101', '0101', '0100', '0010', '1001', '0101', '0111', '0110', '0100', '0001', '0100', '0111', '0101', '1101', '0111', '0001', '0000', '1100', '1000', '0100', '0111', '0001', '1111', '1100', '0001', '0001', '0000', '0101', '0111', '0101', '0011', '0111', '1101', '0001', '0000', '0100', '0101', '1100', '0100', '0010', '1101', '1101', '0101', '0111', '1001', '0111', '0111', '0111', '1100', '1101', '0101', '0101', '0011', '1001', '0100', '1110', '0001', '0010', '0101', '0000', '0001', '0011', '0110', '0101']

    myPauli = PauliContainer(Nqubit=4, pauli_list=Pauli_strings, pauli_list_coeff=Pauli_strings_coeff)
    myRandom = RandomShadow(PauliObj=myPauli)
    expectation_val = myRandom.compute_expectation(basis, bits)

    assert pytest.approx(expectation_val, 0.0001) == -1.11548825


def test_cumulant_expansion_random_measurement():
    # Test expectation value using cumulant expansion with random measurement outcomes
    Pauli_strings = ['IIII', 'IIIZ', 'IIZI', 'IIZZ', 'IZII', 'IZIZ', 'YYII', 'YYIZ', 'XXII', 'XXIZ', 'ZIII', 'ZIIZ', 'IIYY', 'IZYY', 'IIXX', 'IZXX', 'YYYY', 'XXYY', 'YYXX', 'XXXX', 'ZIYY', 'ZIXX', 'IZZI', 'YYZI', 'XXZI', 'ZIZI', 'ZZII']
    Pauli_strings_coeff = [-0.72913365, 0.16199478, -0.01324373, 0.05413045, 0.16199478, 0.12444773, 0.01291061, 0.01153635, 0.01291061, 0.01153635, -0.01324373, 0.05706341, 0.01291061, 0.01153635, 0.01291061, 0.01153635, 0.00293297, 0.00293297, 0.00293297, 0.00293297, -0.00137435, -0.00137435, 0.05706341, -0.00137435, -0.00137435, 0.08479611, 0.05413045]
    basis = ['XYZX', 'ZYYZ', 'YYZY', 'ZXXZ', 'YYYY', 'ZYXY', 'ZZXX', 'YYYY', 'YZZX', 'ZXXY', 'YZXY', 'XZYX', 'XZZY', 'XZZX', 'ZXZZ', 'YZZZ', 'YXZZ', 'ZYZX', 'YXYY', 'ZXYZ', 'ZXXZ', 'XZXZ', 'ZXXX', 'XYZY', 'ZXYX', 'YZXY', 'ZXXY', 'ZZYX', 'XXXZ', 'ZZYX', 'ZZXY', 'ZZZX', 'YYYZ', 'ZXXY', 'ZYZY', 'YZXZ', 'YYYX', 'ZYZZ', 'ZZZX', 'XYYY', 'XYZX', 'ZYZZ', 'XZYY', 'ZZXX', 'XXZY', 'ZYYX', 'ZXXX', 'XZYX', 'YZZX', 'XZZZ', 'ZZXX', 'XYYZ', 'ZXZY', 'XZZY', 'XXXY', 'XXXX', 'ZYXZ', 'ZXYZ', 'YZYX', 'XZZY', 'ZXXZ', 'ZYZY', 'XXXY', 'YZZY', 'ZXXZ', 'YYZZ', 'ZYYZ', 'ZZYY', 'XZYZ', 'ZXZZ', 'ZYZY', 'YXZX', 'ZZXX', 'YZZY', 'ZXZY', 'XYXX', 'XZZX', 'YYXZ', 'ZYYY', 'XYYX', 'XXZX', 'ZXYY', 'ZYXY', 'ZZXZ', 'YZYX', 'YZZZ', 'XXZX', 'XZZZ', 'ZYXZ', 'XYYZ', 'XZZX', 'YXXY', 'XXXZ', 'ZYXX', 'XZZZ', 'YYXX', 'XXZY', 'XXYX', 'ZXYY', 'YZZX']
    bits = ['0101', '0111', '1000', '0001', '1011', '0000', '0100', '0100', '1101', '0010', '0101', '0111', '1100', '0101', '0001', '0101', '0001', '0001', '0010', '0111', '0001', '1111', '0100', '1100', '0110', '0111', '0010', '0110', '1111', '0111', '0101', '0100', '1001', '0000', '0000', '1101', '0101', '0101', '0100', '0010', '1001', '0101', '0111', '0110', '0100', '0001', '0100', '0111', '0101', '1101', '0111', '0001', '0000', '1100', '1000', '0100', '0111', '0001', '1111', '1100', '0001', '0001', '0000', '0101', '0111', '0101', '0011', '0111', '1101', '0001', '0000', '0100', '0101', '1100', '0100', '0010', '1101', '1101', '0101', '0111', '1001', '0111', '0111', '0111', '1100', '1101', '0101', '0101', '0011', '1001', '0100', '1110', '0001', '0010', '0101', '0000', '0001', '0011', '0110', '0101']

    myPauli = PauliContainer(Nqubit=4, pauli_list=Pauli_strings, pauli_list_coeff=Pauli_strings_coeff)
    myCumu = QCumulant(PauliObj=myPauli, measure_basis=basis, measure_outcome_bits=bits)

    myCumu.generate_partitions(max_size=2, num_threads=4)
    expectation_val = myCumu.compute_expectation_bits()

    assert pytest.approx(expectation_val, 0.0001) == -1.09296576


def test_cumulant_expansion_state_vector():
    # Test expectation value using cumulant expansion with a state vector
    Pauli_strings = ['IIII', 'IIIZ', 'IIZI', 'IIZZ', 'IZII', 'IZIZ', 'YYII', 'YYIZ', 'XXII', 'XXIZ', 'ZIII', 'ZIIZ', 'IIYY', 'IZYY', 'IIXX', 'IZXX', 'YYYY', 'XXYY', 'YYXX', 'XXXX', 'ZIYY', 'ZIXX', 'IZZI', 'YYZI', 'XXZI', 'ZIZI', 'ZZII']
    Pauli_strings_coeff = [-0.72913365, 0.16199478, -0.01324373, 0.05413045, 0.16199478, 0.12444773, 0.01291061, 0.01153635, 0.01291061, 0.01153635, -0.01324373, 0.05706341, 0.01291061, 0.01153635, 0.01291061, 0.01153635, 0.00293297, 0.00293297, 0.00293297, 0.00293297, -0.00137435, -0.00137435, 0.05706341, -0.00137435, -0.00137435, 0.08479611, 0.05413045]
    state_vector = [-7.00740547e-17+2.19218907e-16j, -5.51473089e-17-1.08265379e-16j,
                    -2.63334581e-16-2.57419584e-16j,  3.30631448e-16-6.69417684e-16j,
                    6.37659070e-18+9.99839007e-18j, -9.99721473e-01+1.39820785e-02j,
                    -5.25016201e-03+7.34286290e-05j,  2.56192699e-17+5.08469704e-16j,
                    -3.61975093e-16+3.01851169e-16j, -5.25016201e-03+7.34286290e-05j,
                    1.75008307e-02-2.44766162e-04j, -4.40672406e-17-9.17420415e-18j,
                    -2.44561606e-16+7.29023410e-16j, -6.92817642e-16-7.35213677e-16j,
                    -1.04233679e-16-3.10075922e-17j, -1.09342202e-16-1.17476009e-15j]

    myPauli = PauliContainer(Nqubit=4, pauli_list=Pauli_strings, pauli_list_coeff=Pauli_strings_coeff, state_vector=state_vector)
    myCumu = QCumulant(PauliObj=myPauli)

    myCumu.generate_partitions(max_size=2, num_threads=4)
    expectation_val = myCumu.compute_expectation_state()

    assert pytest.approx(expectation_val, 0.0001) == -1.09252938
