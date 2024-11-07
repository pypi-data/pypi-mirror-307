from flair_visual.simulation.cirq_backend import CirqNoiseModelConstructor
from flair_visual.simulation import sample

import numpy as np
import cirq


"""
def test_emit_measurement_noise():

    noise_parameters = sample.NoiseModelParameters()
    cirq_noise_model_constructor = CirqNoiseModelConstructor(
        num_qubits=5, noise_parameters=noise_parameters
    )
    active_qubits = [True for _ in range(4)] + [False]
    generated_circuit = cirq_noise_model_constructor.emit_measurement(
        active_qubits=active_qubits
    )

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(5)
    true_circuit.append(
        [
            cirq.AsymmetricDepolarizingChannel(
                p_x=noise_parameters.measurement_error
            ).on_each(qubits[:4])
        ]
    )

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)


def test_emit_initialize_noise():

    noise_parameters = sample.NoiseModelParameters()
    cirq_noise_model_constructor = CirqNoiseModelConstructor(
        num_qubits=5, noise_parameters=noise_parameters
    )
    generated_circuit = cirq_noise_model_constructor.emit_initialize()

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(5)
    true_circuit.append(
        [
            cirq.AsymmetricDepolarizingChannel(
                p_x=noise_parameters.reset_error
            ).on_each(qubits)
        ]
    )

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)

"""


def test_emit_global_z_rotation_noise():

    noise_parameters = sample.NoiseModelParameters()
    noise_metrics = sample.NoiseMetrics(
        idle_time=0.5, hash_num_transfers=((0, 4), (1, 2), (2, 6)), lost_atoms=()
    )
    global_z_rot = sample.GlobalRz(time=0.1, noise_metrics=noise_metrics, phi=np.pi)
    cirq_noise_model_constructor = CirqNoiseModelConstructor(
        num_qubits=3, noise_parameters=noise_parameters
    )
    active_qubits = np.array([True, False, True])
    generated_circuit = cirq_noise_model_constructor.emit(
        global_z_rot, active_qubits=active_qubits
    )

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(3)

    idle_px, idle_py, idle_pz = noise_parameters.idle_error
    idle_time = noise_metrics.idle_time
    transfer_px, transfer_py, transfer_pz = noise_parameters.trap_transfer_added_error
    transfer_dict = noise_metrics.num_transfers
    global_raman_px, global_raman_py, global_raman_pz = (
        noise_parameters.global_raman_error
    )

    for qubit_id, is_active in enumerate(active_qubits):
        if is_active:
            true_circuit.append(
                cirq.AsymmetricDepolarizingChannel(
                    p_x=idle_px * idle_time,
                    p_y=idle_py * idle_time,
                    p_z=idle_pz * idle_time,
                ).on(qubits[qubit_id])
            )
            num_transfers = transfer_dict[qubit_id]
            true_circuit.append(
                cirq.AsymmetricDepolarizingChannel(
                    p_x=transfer_px * num_transfers,
                    p_y=transfer_py * num_transfers,
                    p_z=transfer_pz * num_transfers,
                ).on(qubits[qubit_id])
            )
            true_circuit.append(
                cirq.AsymmetricDepolarizingChannel(
                    p_x=global_raman_px, p_y=global_raman_py, p_z=global_raman_pz
                ).on(qubits[qubit_id])
            )

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)


def test_emit_global_rotation_noise():

    noise_parameters = sample.NoiseModelParameters()
    noise_metrics = sample.NoiseMetrics(
        idle_time=0.5, hash_num_transfers=((0, 4), (1, 2), (2, 6)), lost_atoms=()
    )
    global_rot = sample.GlobalW(
        time=0.1, noise_metrics=noise_metrics, phi=np.pi, theta=np.pi / 3
    )
    cirq_noise_model_constructor = CirqNoiseModelConstructor(
        num_qubits=3, noise_parameters=noise_parameters
    )
    active_qubits = np.array([True, False, True])
    generated_circuit = cirq_noise_model_constructor.emit(
        global_rot, active_qubits=active_qubits
    )

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(3)

    idle_px, idle_py, idle_pz = noise_parameters.idle_error
    idle_time = noise_metrics.idle_time
    transfer_px, transfer_py, transfer_pz = noise_parameters.trap_transfer_added_error
    transfer_dict = noise_metrics.num_transfers
    global_raman_px, global_raman_py, global_raman_pz = (
        noise_parameters.global_raman_error
    )

    for qubit_id, is_active in enumerate(active_qubits):
        if is_active:
            true_circuit.append(
                cirq.AsymmetricDepolarizingChannel(
                    p_x=idle_px * idle_time,
                    p_y=idle_py * idle_time,
                    p_z=idle_pz * idle_time,
                ).on(qubits[qubit_id])
            )
            num_transfers = transfer_dict[qubit_id]
            true_circuit.append(
                cirq.AsymmetricDepolarizingChannel(
                    p_x=transfer_px * num_transfers,
                    p_y=transfer_py * num_transfers,
                    p_z=transfer_pz * num_transfers,
                ).on(qubits[qubit_id])
            )
            true_circuit.append(
                cirq.AsymmetricDepolarizingChannel(
                    p_x=global_raman_px, p_y=global_raman_py, p_z=global_raman_pz
                ).on(qubits[qubit_id])
            )

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)


def test_emit_local_z_rotation_noise():

    noise_parameters = sample.NoiseModelParameters()
    noise_metrics = sample.NoiseMetrics(
        idle_time=0.5,
        hash_num_transfers=((0, 4), (1, 2), (2, 6), (3, 1)),
        lost_atoms=(),
    )
    participants = (0, 1, 2)

    local_z_rot = sample.LocalRz(
        time=0.1, noise_metrics=noise_metrics, participants=(0, 1, 2), phi=np.pi / 9
    )
    cirq_noise_model_constructor = CirqNoiseModelConstructor(
        num_qubits=4, noise_parameters=noise_parameters
    )
    active_qubits = np.array([True, False, True, True])
    generated_circuit = cirq_noise_model_constructor.emit(
        local_z_rot, active_qubits=active_qubits
    )

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)

    idle_px, idle_py, idle_pz = noise_parameters.idle_error
    idle_time = noise_metrics.idle_time
    transfer_px, transfer_py, transfer_pz = noise_parameters.trap_transfer_added_error
    transfer_dict = noise_metrics.num_transfers
    local_raman_px, local_raman_py, local_raman_pz = noise_parameters.local_raman_error
    bg_local_raman_px, bg_local_raman_py, bg_local_raman_pz = (
        noise_parameters.local_raman_background_error
    )

    for qubit_id, is_active in enumerate(active_qubits):
        if is_active:
            true_circuit.append(
                cirq.AsymmetricDepolarizingChannel(
                    p_x=idle_px * idle_time,
                    p_y=idle_py * idle_time,
                    p_z=idle_pz * idle_time,
                ).on(qubits[qubit_id])
            )
            num_transfers = transfer_dict[qubit_id]
            true_circuit.append(
                cirq.AsymmetricDepolarizingChannel(
                    p_x=transfer_px * num_transfers,
                    p_y=transfer_py * num_transfers,
                    p_z=transfer_pz * num_transfers,
                ).on(qubits[qubit_id])
            )
            if qubit_id in participants:
                true_circuit.append(
                    cirq.AsymmetricDepolarizingChannel(
                        p_x=local_raman_px, p_y=local_raman_py, p_z=local_raman_pz
                    ).on(qubits[qubit_id])
                )
            else:
                true_circuit.append(
                    cirq.AsymmetricDepolarizingChannel(
                        p_x=bg_local_raman_px,
                        p_y=bg_local_raman_py,
                        p_z=bg_local_raman_pz,
                    ).on(qubits[qubit_id])
                )
    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)


def test_emit_local_rotation_noise():

    noise_parameters = sample.NoiseModelParameters()
    noise_metrics = sample.NoiseMetrics(
        idle_time=0.5,
        hash_num_transfers=((0, 4), (1, 2), (2, 6)),
        lost_atoms=(),
    )
    participants = (0, 1, 2)

    local_rot = sample.LocalW(
        time=0.1,
        noise_metrics=noise_metrics,
        participants=(0, 1, 2),
        phi=np.pi / 9,
        theta=-np.pi / 3,
    )
    cirq_noise_model_constructor = CirqNoiseModelConstructor(
        num_qubits=4, noise_parameters=noise_parameters
    )
    active_qubits = np.array([True, False, True, True])
    generated_circuit = cirq_noise_model_constructor.emit(
        local_rot, active_qubits=active_qubits
    )

    true_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)

    idle_px, idle_py, idle_pz = noise_parameters.idle_error
    idle_time = noise_metrics.idle_time
    transfer_px, transfer_py, transfer_pz = noise_parameters.trap_transfer_added_error
    transfer_dict = noise_metrics.num_transfers
    local_raman_px, local_raman_py, local_raman_pz = noise_parameters.local_raman_error
    bg_local_raman_px, bg_local_raman_py, bg_local_raman_pz = (
        noise_parameters.local_raman_background_error
    )

    moment = []
    for qubit_id, is_active in enumerate(active_qubits):
        if is_active:
            moment.append(
                cirq.AsymmetricDepolarizingChannel(
                    p_x=idle_px * idle_time,
                    p_y=idle_py * idle_time,
                    p_z=idle_pz * idle_time,
                ).on(qubits[qubit_id])
            )
    true_circuit.append(cirq.Moment(moment))

    moment = []
    for qubit_id, is_active in enumerate(active_qubits):
        if is_active:
            if qubit_id in transfer_dict:
                num_transfers = transfer_dict[qubit_id]
                moment.append(
                    cirq.AsymmetricDepolarizingChannel(
                        p_x=transfer_px * num_transfers,
                        p_y=transfer_py * num_transfers,
                        p_z=transfer_pz * num_transfers,
                    ).on(qubits[qubit_id])
                )
    true_circuit.append(cirq.Moment(moment))

    moment = []
    for qubit_id, is_active in enumerate(active_qubits):
        if is_active:
            if qubit_id in participants:
                moment.append(
                    cirq.AsymmetricDepolarizingChannel(
                        p_x=local_raman_px, p_y=local_raman_py, p_z=local_raman_pz
                    ).on(qubits[qubit_id])
                )
            else:
                moment.append(
                    cirq.AsymmetricDepolarizingChannel(
                        p_x=bg_local_raman_px,
                        p_y=bg_local_raman_py,
                        p_z=bg_local_raman_pz,
                    ).on(qubits[qubit_id])
                )

    true_circuit.append(cirq.Moment(moment))

    cirq.testing.assert_same_circuits(generated_circuit, true_circuit)


def test_emit_cz_noise_emit():

    noise_parameters = sample.NoiseModelParameters()
    noise_metrics = sample.NoiseMetrics(
        idle_time=0.5,
        hash_num_transfers=((0, 4), (1, 2), (2, 6), (3, 1), (4, 9), (5, 3)),
        lost_atoms=(),
    )
    participants = ((0, 1), (2, 3), (4,))

    cz_event = sample.CZ(
        time=0.9, noise_metrics=noise_metrics, participants=participants
    )
    cirq_noise_model_constructor = CirqNoiseModelConstructor(
        num_qubits=6, noise_parameters=noise_parameters
    )

    entangling_error_x, entangling_error_y, entangling_error_z = (
        noise_parameters.entangling_error
    )

    entangling_error_op = cirq.AsymmetricDepolarizingChannel(
        p_x=entangling_error_x,
        p_y=entangling_error_y,
        p_z=entangling_error_z,
    )

    single_error_x, single_error_y, single_error_z = (
        noise_parameters.single_qubit_entangling_error
    )

    single_error_op = cirq.AsymmetricDepolarizingChannel(
        p_x=single_error_x,
        p_y=single_error_y,
        p_z=single_error_z,
    )

    storage_error_x, storage_error_y, storage_error_z = (
        noise_parameters.entangling_storage_error
    )

    storage_error_op = cirq.AsymmetricDepolarizingChannel(
        p_x=storage_error_x,
        p_y=storage_error_y,
        p_z=storage_error_z,
    )

    entangling_participants = sum(cz_event.participants, ())
    entangling_participants_pair = sum(
        (par for par in cz_event.participants if len(par) == 2), ()
    )
    storage_particicpants = set(range(6)) - set(entangling_participants)

    entangling_qubits = list(map(cirq.LineQubit, entangling_participants))
    entangled_qubit_pairs = list(map(cirq.LineQubit, entangling_participants_pair))
    storage_qubits = list(map(cirq.LineQubit, storage_particicpants))

    storage_error = cirq.Circuit(storage_error_op.on_each(storage_qubits))
    entangled_error = cirq.Circuit([entangling_error_op.on_each(entangled_qubit_pairs)])

    single_error = cirq.Circuit([single_error_op.on_each(entangling_qubits)])

    output_result = cirq_noise_model_constructor.emit_cz(cz_event)

    expected_result = sample.CZNoiseResults(
        storage_error=storage_error,
        entangled_error=entangled_error,
        single_error=single_error,
        participants=cz_event.participants,
    )

    assert output_result == expected_result

    active_qubits = np.array([True, False, True, True, False, True])

    # check masks
    active_single_qubit, active_entangled_qubit = (
        cirq_noise_model_constructor._cz_participation_masks(
            cz_event.participants, active_qubits
        )
    )

    assert np.array_equal(
        active_single_qubit, np.array([True, False, False, False, False, False])
    )
    assert np.array_equal(
        active_entangled_qubit, np.array([False, False, True, True, False, False])
    )

    expected_loss_storage = cirq_noise_model_constructor.remove_lost_qubits(
        storage_error, active_qubits
    )
    expected_loss_single = cirq_noise_model_constructor.remove_lost_qubits(
        single_error, active_single_qubit
    )
    expected_loss_entangled = cirq_noise_model_constructor.remove_lost_qubits(
        entangled_error, active_entangled_qubit
    )

    expected_circle = cirq.Circuit(
        [expected_loss_storage, expected_loss_single, expected_loss_entangled]
    )

    result = cirq_noise_model_constructor.apply_cz_loss(output_result, active_qubits)

    assert expected_circle == result
