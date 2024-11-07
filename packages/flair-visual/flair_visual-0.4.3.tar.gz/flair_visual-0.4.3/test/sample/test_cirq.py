from cirq.testing import assert_same_circuits
import math
from flair_visual.simulation.cirq_backend import (
    CirqCircuitManipulationMixin,
    CirqCleanCircuitConstructor,
    CirqNoiseModelConstructor,
    W,
)
from flair_visual.simulation import sample
import cirq
import numpy as np


DUMMY_NOISE_METRICS = sample.NoiseMetrics(
    idle_time=0.0, hash_num_transfers=(), lost_atoms=()
)


def test_cirq_rotation_gate():
    theta = 0.1023901
    phi = 0.123123

    gate_1 = W(theta=theta, phi=phi)
    gate_2 = W(theta=theta, phi=phi)

    assert gate_1 == gate_2

    assert np.array_equal(
        gate_1._unitary_(),
        np.array(
            [
                [
                    np.cos(theta / 2),
                    -1j * np.exp(-1j * phi) * np.sin(theta / 2),
                ],
                [
                    -1j * np.exp(1j * phi) * np.sin(theta / 2),
                    np.cos(theta / 2),
                ],
            ]
        ),
    )


def test_mixin_remove_qubits():

    circuit = cirq.Circuit(
        [
            cirq.CNOT(cirq.LineQubit(0), cirq.LineQubit(1)),
            cirq.H(cirq.LineQubit(0)),
        ]
    )

    result = CirqCircuitManipulationMixin.remove_lost_qubits(
        circuit, np.array([True, False])
    )

    expected_circuit = cirq.Circuit(
        [cirq.Moment(), cirq.Moment([cirq.H(cirq.LineQubit(0))])]
    )

    assert_same_circuits(result, expected_circuit)


def test_mixing_remove_qubits_2():

    active_qubits = np.array([True, True, False, True])

    circuit = cirq.Circuit(
        [
            cirq.CZ(cirq.LineQubit(0), cirq.LineQubit(1)),
            cirq.CZ(cirq.LineQubit(2), cirq.LineQubit(3)),
        ]
    )

    expected_circuit = cirq.Circuit(
        [
            cirq.CZ(cirq.LineQubit(0), cirq.LineQubit(1)),
        ]
    )

    result = CirqCircuitManipulationMixin.remove_lost_qubits(circuit, active_qubits)

    assert_same_circuits(result, expected_circuit)


def test_mixing_remove_qubits_3():

    active_qubits = np.array([True, True, True, True])

    circuit = cirq.Circuit(
        [
            cirq.CZ(cirq.LineQubit(0), cirq.LineQubit(1)),
            cirq.CZ(cirq.LineQubit(2), cirq.LineQubit(3)),
        ]
    )

    result = CirqCircuitManipulationMixin.remove_lost_qubits(circuit, active_qubits)

    assert_same_circuits(result, circuit)


def test_join_circuit():
    circuit1 = cirq.Circuit(
        [cirq.CNOT(cirq.LineQubit(0), cirq.LineQubit(1)), cirq.H(cirq.LineQubit(0))]
    )

    circuit2 = cirq.Circuit(
        [cirq.H(cirq.LineQubit(1)), cirq.CNOT(cirq.LineQubit(1), cirq.LineQubit(2))]
    )

    result = CirqCircuitManipulationMixin.join([circuit1, circuit2])

    expected_circuit = cirq.Circuit(
        [
            cirq.Moment([cirq.CNOT(cirq.LineQubit(0), cirq.LineQubit(1))]),
            cirq.Moment([cirq.H(cirq.LineQubit(0))]),
            cirq.Moment([cirq.H(cirq.LineQubit(1))]),
            cirq.Moment([cirq.CNOT(cirq.LineQubit(1), cirq.LineQubit(2))]),
        ]
    )

    assert_same_circuits(result, expected_circuit)


def test_clean_initialization():
    constructor = CirqCleanCircuitConstructor(num_qubits=3)

    expected = cirq.Circuit()
    assert_same_circuits(constructor.emit_initialize(), expected)

    expected_loss = expected
    active_qubits = np.array([True, False, True])
    assert_same_circuits(
        constructor.apply_initialize_loss(expected, active_qubits), expected_loss
    )


def test_clean_cz():
    participants = ((0, 1), (2, 3))
    cz_event = sample.CZ(
        time=0.0, noise_metrics=DUMMY_NOISE_METRICS, participants=participants
    )
    constructor = CirqCleanCircuitConstructor(num_qubits=4)

    expected_circuit = cirq.Circuit(
        [
            cirq.CZ(cirq.LineQubit(0), cirq.LineQubit(1)),
            cirq.CZ(cirq.LineQubit(2), cirq.LineQubit(3)),
        ]
    )

    assert_same_circuits(constructor.emit_cz(cz_event), expected_circuit)

    active_qubits = np.array([True, True, False, True])

    expected_circuit_loss = cirq.Circuit(
        [
            cirq.CZ(cirq.LineQubit(0), cirq.LineQubit(1)),
        ]
    )

    assert_same_circuits(
        constructor.apply_cz_loss(expected_circuit, active_qubits),
        expected_circuit_loss,
    )


def test_clean_global_z_rotation():
    global_z_rot_event = sample.GlobalRz(
        time=0.0, noise_metrics=DUMMY_NOISE_METRICS, phi=0.25
    )
    constructor = CirqCleanCircuitConstructor(num_qubits=4)

    expected_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    op = cirq.Rz(rads=0.25 * math.tau)
    expected_circuit.append(op.on_each(qubits))

    assert_same_circuits(
        constructor.emit_global_rz(global_z_rot_event), expected_circuit
    )

    active_qubits = np.array([False, True, False, True])

    expected_circuit_loss = cirq.Circuit()

    expected_circuit_loss.append(op.on_each([qubits[1], qubits[3]]))

    assert_same_circuits(
        constructor.apply_global_rz_loss(expected_circuit, active_qubits),
        expected_circuit_loss,
    )


def test_clean_global_rotation():
    global_rot_event = sample.GlobalW(
        time=0.0, noise_metrics=DUMMY_NOISE_METRICS, phi=0.25, theta=0.5
    )

    constructor = CirqCleanCircuitConstructor(num_qubits=4)

    expected_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    op = W(theta=0.5 * math.tau, phi=0.25 * math.tau)
    expected_circuit.append(op.on_each(qubits))

    assert_same_circuits(constructor.emit_global_w(global_rot_event), expected_circuit)

    active_qubits = np.array([False, True, False, True])

    expected_circuit_loss = cirq.Circuit()
    expected_circuit_loss.append(op.on_each([qubits[1], qubits[3]]))

    assert_same_circuits(
        constructor.apply_global_w_loss(expected_circuit, active_qubits),
        expected_circuit_loss,
    )


def test_clean_local_z_rotation():
    local_rot_z_event = sample.LocalRz(
        time=0.0,
        noise_metrics=DUMMY_NOISE_METRICS,
        qubit=1,
        phi=0.25,
        participants=(1, 3),
    )

    constructor = CirqCleanCircuitConstructor(num_qubits=4)

    expected_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)

    op = cirq.Rz(rads=0.25 * math.tau)
    expected_circuit.append(op.on_each([qubits[1], qubits[3]]))

    assert_same_circuits(constructor.emit_local_rz(local_rot_z_event), expected_circuit)

    active_qubits = np.array([False, True, False, False])

    expected_circuit_loss = cirq.Circuit()
    expected_circuit_loss.append(op.on(qubits[1]))

    assert_same_circuits(
        constructor.apply_local_rz_loss(expected_circuit, active_qubits),
        expected_circuit_loss,
    )


def test_clean_local_rotation():
    local_rot_event = sample.LocalW(
        time=0.0,
        noise_metrics=DUMMY_NOISE_METRICS,
        qubit=1,
        phi=0.43,
        theta=0.123,
        participants=(1, 3),
    )

    constructor = CirqCleanCircuitConstructor(num_qubits=4)
    op = W(theta=0.123 * math.tau, phi=0.43 * math.tau)
    expected_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    expected_circuit.append(op.on_each([qubits[1], qubits[3]]))

    assert_same_circuits(constructor.emit_local_w(local_rot_event), expected_circuit)

    active_qubits = np.array([False, True, False, False])

    expected_circuit_loss = cirq.Circuit()
    expected_circuit_loss.append(op.on(qubits[1]))

    assert_same_circuits(
        constructor.apply_local_w_loss(expected_circuit, active_qubits),
        expected_circuit_loss,
    )


def test_clean_measurement():
    measurement_event = sample.Measurement(
        time=0.0, noise_metrics=DUMMY_NOISE_METRICS, qubit=1, participants=(1, 3)
    )

    constructor = CirqCleanCircuitConstructor(num_qubits=4)

    expected_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    expected_circuit.append(cirq.measure([qubits[1], qubits[3]], key="m"))

    assert_same_circuits(
        constructor.emit_measurement(measurement_event), expected_circuit
    )

    active_qubits = np.array([False, True, False, False])

    lost_qubits = [
        cirq.LineQubit(qubit_id)
        for qubit_id, is_active in enumerate(active_qubits)
        if not is_active
    ]

    reset_moment = cirq.Moment(list(map(cirq.reset, lost_qubits)))
    x_gate_moment = cirq.Moment(list(map(cirq.X, lost_qubits)))

    expected_circuit_loss = cirq.Circuit(
        [reset_moment, x_gate_moment, expected_circuit[0]]
    )

    assert_same_circuits(
        constructor.apply_measurement_loss(expected_circuit, active_qubits),
        expected_circuit_loss,
    )


def test_emit_caching():
    participants = ((0, 1), (2, 3))
    cz_event = sample.CZ(
        time=0.0, noise_metrics=DUMMY_NOISE_METRICS, participants=participants
    )
    constructor = CirqCleanCircuitConstructor(num_qubits=4)

    active_qubits = np.array([True, True, False, True])

    expected_circuit = cirq.Circuit(
        [
            cirq.CZ(cirq.LineQubit(0), cirq.LineQubit(1)),
        ]
    )

    assert_same_circuits(constructor.emit(cz_event, active_qubits), expected_circuit)

    # now with cached results
    active_qubits = np.array([True, False, True, True])

    expected_circuit = cirq.Circuit(
        [
            cirq.CZ(cirq.LineQubit(2), cirq.LineQubit(3)),
        ]
    )

    assert_same_circuits(constructor.emit(cz_event, active_qubits), expected_circuit)

    active_qubits = np.array([True, False, False, True])

    expected_circuit = cirq.Circuit([cirq.Moment()])

    assert_same_circuits(constructor.emit(cz_event, active_qubits), expected_circuit)


def test_noisy_initialization():
    noise_parameters = sample.NoiseModelParameters(reset_error=0.1)

    constructor = CirqNoiseModelConstructor(
        num_qubits=3, noise_parameters=noise_parameters
    )
    px = noise_parameters.reset_error

    expected = cirq.Circuit()
    qubits = cirq.LineQubit.range(3)

    expected.append(cirq.AsymmetricDepolarizingChannel(p_x=px).on_each(qubits))
    assert_same_circuits(constructor.emit_initialize(), expected)

    active_qubits = np.array([True, False, True])
    expected_loss = cirq.Circuit(
        [cirq.AsymmetricDepolarizingChannel(p_x=px).on_each([qubits[0], qubits[2]])]
    )

    assert_same_circuits(
        constructor.apply_initialize_loss(expected, active_qubits), expected_loss
    )
