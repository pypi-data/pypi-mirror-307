import cirq
from flair_visual.simulation import sample
import numpy as np


def get_circuit():

    noise_metric_0 = sample.NoiseMetrics(
        idle_time=0.0,
        hash_num_transfers=((0, 1), (1, 0)),
        lost_atoms=(),
    )

    noise_metric_1 = sample.NoiseMetrics(
        idle_time=1000.0,
        hash_num_transfers=((0, 1), (2, 1)),
        lost_atoms=(),
    )

    return sample.Circuit(
        num_qubits=(num_qubits := 10),
        gates=(
            sample.Gate(
                operation=sample.LocalW(
                    time=0.0,
                    noise_metrics=noise_metric_0,
                    participants=(0,),
                    theta=0.25,
                    phi=0,
                )
            ),
            sample.Gate(
                operation=sample.CZ(
                    time=10.0, noise_metrics=noise_metric_1, participants=((0, 1),)
                )
            ),
            sample.Gate(
                operation=sample.CZ(
                    time=20.0, noise_metrics=noise_metric_1, participants=((0, 2),)
                )
            ),
            sample.Gate(
                operation=sample.Measurement(
                    time=30.0,
                    noise_metrics=noise_metric_1,
                    participants=tuple(range(num_qubits)),
                )
            ),
        ),
    )


def test_active_qubit_states():

    class DummyGenerator:
        def random(self, size):
            return np.ones(size)

    circuit = get_circuit()

    sim_obj = circuit.get_sampler("cirq")

    generator = DummyGenerator()

    state = sim_obj.active_qubit_states(generator)

    gate_events = [gate.operation for gate in circuit.gates]

    expected_state = np.ones((len(gate_events), circuit.num_qubits), dtype=bool)

    expected_state[:, 0] = False
    expected_state[1:, 2] = False

    assert np.array_equal(state, expected_state)


def test_clean_circuit():

    circuit = get_circuit()

    sim_obj = circuit.get_sampler("cirq")

    expected_circuit = cirq.Circuit()

    gate_events = [gate.operation for gate in circuit.gates]

    active_qubits = np.ones(circuit.num_qubits, dtype=bool)
    for i, gate in enumerate(gate_events):
        current_qubits = active_qubits.copy()
        current_qubits[list(gate.noise_metrics.lost_atoms)] = False
        expected_circuit.append(sim_obj.circuit_generator.emit(gate, current_qubits))

    assert expected_circuit == sim_obj.clean_circuit


def test_clean_empty_circuit():
    circuit = sample.Circuit(num_qubits=0, gates=[])

    sim_obj = circuit.get_sampler("cirq")

    assert sim_obj.clean_circuit == cirq.Circuit()
    assert sim_obj.run(10) == {}
