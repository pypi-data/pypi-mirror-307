import json
from flair_visual.simulation import sample
import pytest


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


def test_sum():

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
    lhs = sample.Circuit(
        num_qubits=(num_qubits := 10),
        gates=[
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
        ],
    )

    rhs = sample.Circuit(
        num_qubits=(num_qubits := 10),
        gates=[
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
        ],
    )

    rhs_bad = sample.Circuit(
        num_qubits=(num_qubits := 5),
        gates=[
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
        ],
    )

    assert (lhs + rhs) == get_circuit()

    with pytest.raises(ValueError):
        lhs + rhs_bad

    with pytest.raises(ValueError):
        lhs + 1


def test_append():

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

    circuit = sample.Circuit(
        num_qubits=(num_qubits := 10),
        gates=[
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
        ],
    )

    operations = [
        sample.CZ(time=20.0, noise_metrics=noise_metric_1, participants=((0, 2),)),
        sample.Measurement(
            time=30.0,
            noise_metrics=noise_metric_1,
            participants=tuple(range(num_qubits)),
        ),
    ]

    for operation in operations:
        circuit.append(operation)

    assert circuit == get_circuit()


def test_get_sampler():
    assert isinstance(get_circuit().get_sampler("cirq"), sample.AtomLossCircuitSampler)


def test_serialization():
    circuit = get_circuit()

    circuit_json = circuit.model_dump_json()
    deserialized_circuit = sample.Circuit(**json.loads(circuit_json))

    assert circuit == deserialized_circuit
