from flair_visual.simulation import sample
from typing import Any, Dict, List, Set, Union
import numpy as np
import math
import cirq


@cirq.value_equality
class W(cirq.Gate):
    def __init__(self, theta, phi):
        super(W, self)
        self.theta = theta
        self.phi = phi

    def _value_equality_values_(self):
        return self.theta, self.phi

    def __eq__(self, other):
        return other.theta == self.theta and other.phi == self.phi

    def _num_qubits_(self):
        return 1

    def _unitary_(self):
        return np.array(
            [
                [
                    np.cos(self.theta / 2),
                    -1j * np.exp(-1j * self.phi) * np.sin(self.theta / 2),
                ],
                [
                    -1j * np.exp(1j * self.phi) * np.sin(self.theta / 2),
                    np.cos(self.theta / 2),
                ],
            ]
        )

    def _circuit_diagram_info_(self, args):
        return f"R(θ = {self.theta}, φ = {self.phi})"


class CirqCircuitManipulationMixin:

    @staticmethod
    def remove_lost_qubits(circuit: cirq.Circuit, active_qubits: np.ndarray[Any, bool]):
        assert isinstance(circuit, cirq.Circuit)
        if np.all(active_qubits):
            return circuit

        lost_qubits = set(
            cirq.LineQubit(qubit_id)
            for qubit_id, is_active in enumerate(active_qubits)
            if not is_active
        )
        new_moments = []
        for moment in circuit:
            new_moments.append(
                cirq.Moment((op for op in moment if lost_qubits.isdisjoint(op.qubits)))
            )

        return cirq.Circuit(new_moments)

    @staticmethod
    def join(circuits: List[cirq.Circuit]):
        # want to avoid using the `+` operator due to performance degradation
        # so we get the moments out of each circuit and then put them into
        # one bigger circuit
        total_moments = []

        for circuit in circuits:
            total_moments += circuit.moments
        return cirq.Circuit(total_moments)


@sample.CircuitConstructorRegistry.register_clean("cirq")
class CirqCleanCircuitConstructor(
    CirqCircuitManipulationMixin, sample.CircuitConstructorABC[cirq.Circuit]
):

    def emit_initialize(self):
        return cirq.Circuit()

    def apply_initialize_loss(
        self, circuit: cirq.Circuit, active_qubits: np.ndarray[Any, bool]
    ):
        return circuit

    def emit_cz(self, gate_event: sample.CZ):
        qubits = cirq.LineQubit.range(self.num_qubits)
        cz_gates = [
            cirq.CZ(qubits[pairs[0]], qubits[pairs[1]])
            for pairs in gate_event.participants
            if len(pairs) == 2
        ]
        return cirq.Circuit(cz_gates)

    def emit_global_rz(self, gate_event: sample.GlobalRz):
        qubits = cirq.LineQubit.range(self.num_qubits)
        rz_gates = [
            cirq.Rz(rads=gate_event.phi * math.tau)(qubits[qubit_id])
            for qubit_id in range(self.num_qubits)
        ]
        return cirq.Circuit(rz_gates)

    def emit_local_rz(self, gate_event: sample.LocalRz):
        qubits = cirq.LineQubit.range(self.num_qubits)
        rz_gates = [
            cirq.Rz(rads=gate_event.phi * math.tau)(qubits[qubit_id])
            for qubit_id in gate_event.participants
        ]
        return cirq.Circuit(rz_gates)

    def emit_global_w(self, gate_event: sample.GlobalW):
        qubits = cirq.LineQubit.range(self.num_qubits)
        rotation_gates = [
            W(gate_event.theta * math.tau, gate_event.phi * math.tau)(qubits[qubit_id])
            for qubit_id in range(self.num_qubits)
        ]
        return cirq.Circuit(rotation_gates)

    def emit_local_w(self, gate_event: sample.LocalW):
        qubits = cirq.LineQubit.range(self.num_qubits)
        rotation_gates = [
            W(gate_event.theta * math.tau, gate_event.phi * math.tau)(qubits[qubit_id])
            for qubit_id in gate_event.participants
        ]
        return cirq.Circuit(rotation_gates)

    def emit_measurement(self, gate_event: sample.Measurement):
        qubits = tuple(map(cirq.LineQubit, gate_event.participants))
        circuit = cirq.Circuit()

        circuit.append(cirq.measure(qubits, key=gate_event.measure_tag))
        return circuit

    def apply_measurement_loss(self, circuit, active_qubits):
        # apply Reset, X, then M for lost qubits
        # the M has already been applied, you just need to prepend the R and X moments
        if np.all(active_qubits):
            return circuit

        lost_qubits = [
            cirq.LineQubit(qubit_id)
            for qubit_id, is_active in enumerate(active_qubits)
            if not is_active
        ]

        reset_moment = cirq.Moment(list(map(cirq.reset, lost_qubits)))
        x_gate_moment = cirq.Moment(list(map(cirq.X, lost_qubits)))

        return cirq.Circuit([reset_moment, x_gate_moment, *circuit.moments])


@sample.CircuitConstructorRegistry.register_noise("cirq")
class CirqNoiseModelConstructor(
    CirqCircuitManipulationMixin, sample.NoiseModelConstructorABC[cirq.Circuit]
):

    def generate_aod_trap_transfer_error(
        self, noise_metrics: sample.NoiseMetrics
    ) -> cirq.Moment:

        num_transfers_dict = noise_metrics.num_transfers
        px, py, pz = self.noise_parameters.trap_transfer_added_error

        qubits = cirq.LineQubit.range(self.num_qubits)
        transfer_errors = []

        # unique number of transfers for the active qubits
        for qubit_id in range(self.num_qubits):
            if qubit_id not in num_transfers_dict:
                continue

            num_transfers = num_transfers_dict[qubit_id]
            transfer_errors.append(
                cirq.AsymmetricDepolarizingChannel(
                    p_x=px * num_transfers,
                    p_y=py * num_transfers,
                    p_z=pz * num_transfers,
                ).on(qubits[qubit_id])
            )

        return cirq.Circuit([transfer_errors])

    def generate_trap_idle_error(
        self, noise_metrics: sample.NoiseMetrics
    ) -> cirq.Moment:

        idle_time = noise_metrics.idle_time
        px, py, pz = self.noise_parameters.idle_error

        qubits = cirq.LineQubit.range(self.num_qubits)
        trap_idle_error = cirq.AsymmetricDepolarizingChannel(
            p_x=px * idle_time, p_y=py * idle_time, p_z=pz * idle_time
        )

        return cirq.Circuit([trap_idle_error.on(qubit) for qubit in qubits])

    def generate_global_w_noise(
        self, gate_event: Union[sample.GlobalW, sample.GlobalW]
    ):

        px, py, pz = self.noise_parameters.global_raman_error

        qubits = cirq.LineQubit.range(self.num_qubits)

        global_rotation_noise_moment = cirq.Moment(
            cirq.AsymmetricDepolarizingChannel(p_x=px, p_y=py, p_z=pz).on_each(qubits)
        )

        return cirq.Circuit([global_rotation_noise_moment])

    def generate_local_w_noise(
        self,
        gate_event: Union[sample.LocalRz, sample.LocalW],
    ):
        participants = gate_event.participants

        gate_px, gate_py, gate_pz = self.noise_parameters.local_raman_error
        background_px, background_py, background_pz = (
            self.noise_parameters.local_raman_background_error
        )

        qubits = cirq.LineQubit.range(self.num_qubits)

        local_rotation_noise_operations = []

        for qubit_id in range(self.num_qubits):
            if qubit_id in participants:
                local_rotation_noise_operations.append(
                    cirq.AsymmetricDepolarizingChannel(
                        p_x=gate_px, p_y=gate_py, p_z=gate_pz
                    ).on(qubits[qubit_id])
                )
            else:
                local_rotation_noise_operations.append(
                    cirq.AsymmetricDepolarizingChannel(
                        p_x=background_px, p_y=background_py, p_z=background_pz
                    ).on(qubits[qubit_id])
                )

        local_rotation_noise_moment = cirq.Moment(local_rotation_noise_operations)

        return cirq.Circuit([local_rotation_noise_moment])

    def emit_cz(self, gate_event: sample.CZ):

        participants = gate_event.participants

        # for atoms that will entangle because of the sample.CZ
        entangling_px, entangling_py, entangling_pz = (
            self.noise_parameters.entangling_error
        )
        entangling_error = cirq.AsymmetricDepolarizingChannel(
            p_x=entangling_px, p_y=entangling_py, p_z=entangling_pz
        )
        # for single atoms that still experience the sample.CZ pulse
        single_entangling_px, single_entangling_py, single_entangling_pz = (
            self.noise_parameters.single_qubit_entangling_error
        )
        single_qubit_error = cirq.AsymmetricDepolarizingChannel(
            p_x=single_entangling_px, p_y=single_entangling_py, p_z=single_entangling_pz
        )
        # for atoms that are not participating in the sample.CZ
        storage_px, storage_py, storage_pz = (
            self.noise_parameters.entangling_storage_error
        )
        storage_error = cirq.AsymmetricDepolarizingChannel(
            p_x=storage_px, p_y=storage_py, p_z=storage_pz
        )

        participants_flat = sum(participants, ())
        participant_qubits = list(map(cirq.LineQubit, participants_flat))

        participant_pair_flat = sum(
            (pair for pair in participants if len(pair) == 2), ()
        )
        participant_pair_qubits = list(map(cirq.LineQubit, participant_pair_flat))

        non_participants = set(range(self.num_qubits)) - set(sum(participants, ()))
        non_participants_qubits = list(map(cirq.LineQubit, non_participants))

        entangled_error = cirq.Circuit(
            [entangling_error.on_each(participant_pair_qubits)]
        )
        single_error = cirq.Circuit(single_qubit_error.on_each(participant_qubits))
        storage_error = cirq.Circuit([storage_error.on_each(non_participants_qubits)])

        return sample.CZNoiseResults(
            storage_error,
            entangled_error,
            single_error,
            participants,
        )

    def emit_initialize(self):
        px = self.noise_parameters.reset_error

        circuit = cirq.Circuit()
        qubits = cirq.LineQubit.range(self.num_qubits)

        circuit.append(cirq.AsymmetricDepolarizingChannel(p_x=px).on_each(qubits))

        return circuit

    def emit_global_rz(self, gate_event: sample.GlobalRz):
        return self.generate_global_w_noise(gate_event)

    def emit_global_w(self, gate_event: sample.GlobalW):
        return self.generate_global_w_noise(gate_event=gate_event)

    def emit_local_rz(self, gate_event: sample.LocalRz):
        return self.generate_local_w_noise(gate_event=gate_event)

    def emit_local_w(self, gate_event: sample.LocalW):
        return self.generate_local_w_noise(gate_event=gate_event)

    def emit_measurement(self, gate_event: sample.Measurement):
        px = self.noise_parameters.measurement_error

        circuit = cirq.Circuit()
        qubits = tuple(map(cirq.LineQubit, gate_event.participants))

        circuit.append(cirq.AsymmetricDepolarizingChannel(p_x=px).on_each(qubits))

        return circuit

    def apply_measurement_loss(self, circuit, active_qubits):
        return self.remove_lost_qubits(circuit, active_qubits)

    def run(self, noise_model: cirq.Circuit, measure_tag: Set[str]) -> Dict[str, str]:
        result = cirq.Simulator().run(noise_model, repetitions=1)

        out = {}
        for tag in measure_tag:
            result_histogram = result.histogram(key=tag)

            result_dict = dict(result_histogram)
            assert len(result_dict) == 1

            ((k, v),) = result_dict.items()
            assert v == 1

            out[tag] = k

        return out
