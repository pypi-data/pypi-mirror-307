from flair_visual.simulation.cirq_backend import (
    CirqCleanCircuitConstructor,
    W,
)
from flair_visual.simulation import sample
from flair_visual.simulation.sample import NoiseMetrics
import numpy as np
import math
import cirq

dummy_noise_metrics = NoiseMetrics(idle_time=0.0, hash_num_transfers=(), lost_atoms=())


def test_emit_cz():

    participants = ((0, 1), (2, 3))
    cz_event = sample.CZ(
        time=0.0, noise_metrics=dummy_noise_metrics, participants=participants
    )
    cirq_clean_circuit_constructor = CirqCleanCircuitConstructor(num_qubits=4)
    active_qubits = np.array([True, True, False, True])
    generated_circuit = cirq_clean_circuit_constructor.emit(
        cz_event, active_qubits=active_qubits
    )

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    true_circuit.append(cirq.CZ(qubits[0], qubits[1]))

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)


def test_emit_cz_single_atom():

    participants = ((0,), (2, 3))
    cz_event = sample.CZ(
        time=0.0, noise_metrics=dummy_noise_metrics, participants=participants
    )
    cirq_clean_circuit_constructor = CirqCleanCircuitConstructor(num_qubits=4)
    active_qubits = np.array([False, True, True, True])
    generated_circuit = cirq_clean_circuit_constructor.emit(
        cz_event, active_qubits=active_qubits
    )

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    true_circuit.append(cirq.CZ(qubits[2], qubits[3]))

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)


def test_emit_global_z_rotation():

    global_z_rot_event = sample.GlobalRz(
        time=0.0, noise_metrics=dummy_noise_metrics, phi=np.pi / 5
    )
    cirq_clean_circuit_constructor = CirqCleanCircuitConstructor(num_qubits=4)
    active_qubits = np.array([True, True, False, True])
    generated_circuit = cirq_clean_circuit_constructor.emit(
        global_z_rot_event, active_qubits=active_qubits
    )

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    for qubit_id, qubit_present in enumerate(active_qubits):
        if qubit_present:
            true_circuit.append(cirq.Rz(rads=np.pi / 5 * math.tau)(qubits[qubit_id]))

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)


def test_emit_local_z_rotation():

    participants = (0, 2, 3)
    local_z_rot_event = sample.LocalRz(
        time=0.0,
        noise_metrics=dummy_noise_metrics,
        participants=participants,
        phi=np.pi / 7,
    )
    cirq_clean_circuit_constructor = CirqCleanCircuitConstructor(num_qubits=4)
    active_qubits = np.array([False, True, True, True])
    generated_circuit = cirq_clean_circuit_constructor.emit(
        local_z_rot_event, active_qubits=active_qubits
    )

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    for qubit_id in participants:
        if active_qubits[qubit_id]:
            true_circuit.append(cirq.Rz(rads=np.pi / 7 * math.tau)(qubits[qubit_id]))

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)


def test_emit_global_rotation():

    global_rot_event = sample.GlobalW(
        time=0.0, noise_metrics=dummy_noise_metrics, theta=np.pi / 3, phi=np.pi / 6
    )
    cirq_clean_circuit_constructor = CirqCleanCircuitConstructor(num_qubits=4)
    active_qubits = np.array([True, True, False, True])
    generated_circuit = cirq_clean_circuit_constructor.emit(
        global_rot_event, active_qubits=active_qubits
    )

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    for qubit_id, qubit_present in enumerate(active_qubits):
        if qubit_present:
            true_circuit.append(
                W(theta=np.pi / 3 * math.tau, phi=np.pi / 6 * math.tau)(
                    qubits[qubit_id]
                )
            )

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)


def test_emit_local_rotation():

    participants = (0, 2, 3)
    local_rot_event = sample.LocalW(
        time=0.0,
        noise_metrics=dummy_noise_metrics,
        participants=participants,
        theta=np.pi / 2,
        phi=np.pi / 7,
    )
    cirq_clean_circuit_constructor = CirqCleanCircuitConstructor(num_qubits=4)
    active_qubits = np.array([False, True, True, True])
    generated_circuit = cirq_clean_circuit_constructor.emit(
        local_rot_event, active_qubits=active_qubits
    )

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    for qubit_id in participants:
        if active_qubits[qubit_id]:
            true_circuit.append(
                W(theta=np.pi / 2 * math.tau, phi=np.pi / 7 * math.tau)(
                    qubits[qubit_id]
                )
            )

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)


"""
# waiting for mapping from FLAIR to event
def test_emit_initialize():

    cirq_clean_circuit_constructor = CirqCleanCircuitConstructor(num_qubits=4)
    generated_circuit = cirq_clean_circuit_constructor.emit_initialize()

    true_circuit = cirq.Circuit()

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)

# Waiting for measurement gate instruction to be implemented by Phillip W.
def test_emit_measurement():

    cirq_clean_circuit_constructor = CirqCleanCircuitConstructor(num_qubits=4)
    active_qubits = np.array([False, False, True, True])
    generated_circuit = cirq_clean_circuit_constructor.emit_measurement()

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    for qubit_id, qubit_present in enumerate(active_qubits):
        if not qubit_present:
            true_circuit.append(cirq.ResetChannel().on(qubits[qubit_id]))
            true_circuit.append(cirq.X(qubits[qubit_id]))

    true_circuit.append(cirq.measure_each(qubits))

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)
"""
