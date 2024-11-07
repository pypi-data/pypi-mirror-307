import abc
from collections import Counter, defaultdict
from pydantic import Field, BaseModel, PrivateAttr
from dataclasses import InitVar, dataclass as python_dataclass, field as python_field
from functools import cached_property
from typing import Callable, ClassVar, Literal, Set, Union
from typing import (
    Type,
    Dict,
    List,
    Tuple,
    Generic,
    TypeVar,
    Optional,
    Any,
)
import numpy as np


class NoiseModelParameters(BaseModel, frozen=True, extra="forbid"):
    reset_error: float = 4e-3
    measurement_error: float = 3e-3
    reset_loss: float = 0e-3
    idle_error: Tuple[float, float, float] = (1e-7, 1e-7, 6e-7)
    idle_loss: float = 0
    entangling_error: Tuple[float, float, float] = (
        0.005 / 8,
        0.005 / 8,
        0.005 / 4,
    )
    single_qubit_entangling_error: Tuple[float, float, float] = (
        0.005 / 8,
        0.005 / 8,
        0.005 / 4,
    )
    entangling_loss: float = 0
    entangling_storage_error: Tuple[float, float, float] = (
        0,
        0,
        0,
    )
    entangling_storage_loss: float = 0
    global_raman_error: Tuple[float, float, float] = (1e-4, 1e-4, 1e-4)
    local_raman_error: Tuple[float, float, float] = (5e-4, 5e-4, 5e-4)
    local_raman_background_error: Tuple[float, float, float] = (1e-4, 1e-4, 1e-4)
    trap_transfer_added_error: Tuple[float, float, float] = (5e-4, 5e-4, 5e-4)
    trap_transfer_added_loss: float = 5e-4


class NoiseMetrics(BaseModel, frozen=True, extra="forbid"):
    """Metrics for generating the noise in the circuit"""

    idle_time: float
    hash_num_transfers: Tuple[Tuple[int, int], ...]
    lost_atoms: Tuple[int, ...]

    @cached_property
    def num_transfers(self) -> Dict[int, int]:
        return defaultdict(int, self.hash_num_transfers)


class Operation(BaseModel, frozen=True):
    name: str = Field(init=False)
    time: float
    noise_metrics: NoiseMetrics


class CZ(Operation):
    name: Literal["CZ"] = Field(init=False, default="CZ")
    participants: Tuple[Union[Tuple[int], Tuple[int, int]], ...]


class GlobalRz(Operation):
    name: Literal["GlobalRz"] = Field(init=False, default="GlobalRz")
    phi: float


class GlobalW(Operation):
    name: Literal["GlobalW"] = Field(init=False, default="GlobalW")
    theta: float
    phi: float


class LocalRz(Operation):
    name: Literal["LocalRz"] = Field(init=False, default="LocalRz")
    participants: Tuple[int, ...]
    phi: float


class LocalW(Operation):
    name: Literal["LocalW"] = Field(init=False, default="LocalW")
    participants: Tuple[int, ...]
    theta: float
    phi: float


class Measurement(Operation):
    name: Literal["Measurement"] = Field(init=False, default="Measurement")
    measure_tag: str = Field(default="m")
    participants: Tuple[int, ...]


def init_dispatch_table(cls):
    """Needed to initialize the dispatch table for the survival probability calculator"""
    cls._init_dispatch_table()
    return cls


@init_dispatch_table
class SurvivalProbabilityCalculator(BaseModel, abc.ABC, extra="forbid"):

    num_qubits: int
    noise_parameters: NoiseModelParameters

    _DISPATCH_TABLE: ClassVar[Dict[Type[Operation], str]]

    @classmethod
    def _init_dispatch_table(cls):
        cls._DISPATCH_TABLE = {
            "CZ": cls.emit_cz,
            "GlobalRz": cls.emit_global_rz,
            "GlobalW": cls.emit_global_w,
            "LocalRz": cls.emit_local_rz,
            "LocalW": cls.emit_local_w,
            "Measurement": cls.emit_measurement,
        }

    def background_survival(self, noise_metrics: NoiseMetrics) -> np.ndarray[float]:
        """Calculate the survival probability of each atom in the background regardless of the gate event.

        Things to consider:
        - Idle loss
        - Transfer loss

        TODO: AOD loss

        """
        # idle loss probability
        idle_survival_prob = np.exp(
            -self.noise_parameters.idle_loss * noise_metrics.idle_time
        )

        # transfer loss probability
        transfer_counts = np.array(
            [
                noise_metrics.num_transfers.get(atom, 0)
                for atom in range(self.num_qubits)
            ]
        )
        transfer_survival_prob = (
            1 - self.noise_parameters.trap_transfer_added_loss
        ) ** transfer_counts

        # combine the two
        survival_prob = transfer_survival_prob * idle_survival_prob

        # any lost atoms have 0 survival probability for this gate
        lost_atoms = np.array(list(noise_metrics.lost_atoms), dtype=int)
        survival_prob[lost_atoms] = 0.0

        return survival_prob

    def emit_cz(self, gate_event: CZ) -> np.ndarray[float]:
        # TODO: survival probability based on one or both atoms being lost during gate.
        # start with the background survival probabilities
        survival_prob = self.background_survival(gate_event.noise_metrics)

        # apply CZ gate loss to all participants
        cz_atoms = np.array(sum(gate_event.participants, ()))
        survival_prob[cz_atoms] *= 1 - self.noise_parameters.entangling_loss

        return survival_prob

    def emit_global_rz(self, gate_event: GlobalW) -> np.ndarray[float]:
        return self.background_survival(gate_event.noise_metrics)

    def emit_global_w(self, gate_event: GlobalW) -> np.ndarray[float]:
        return self.background_survival(gate_event.noise_metrics)

    def emit_local_rz(self, gate_event: LocalRz) -> np.ndarray[float]:
        return self.background_survival(gate_event.noise_metrics)

    def emit_local_w(self, gate_event: LocalW) -> np.ndarray[float]:
        return self.background_survival(gate_event.noise_metrics)

    def emit_measurement(self, gate_event: Measurement) -> np.ndarray[float]:
        return self.background_survival(gate_event.noise_metrics)

    def emit(self, gate_event: Operation) -> np.ndarray[float]:
        result = self._DISPATCH_TABLE[gate_event.name](self, gate_event)
        assert isinstance(result, np.ndarray), f"Result is not a numpy array: {result}"
        assert result.shape == (
            self.num_qubits,
        ), f"Result shape is incorrect: {result}"
        return result


CircuitType = TypeVar("CircuitType")


class CircuitConstructorABC(BaseModel, abc.ABC, Generic[CircuitType]):
    """Class that constructs clean circuits from gate events"""

    num_qubits: int
    _EMIT_DISPATCH_TABLE: ClassVar[Dict[Type[Operation], Callable]]
    _APPLY_DISPATCH_TABLE: ClassVar[Dict[Type[Operation], Callable]]

    _lazy_gate_cache: Dict[Operation, CircuitType] = PrivateAttr(default_factory=dict)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        cls._EMIT_DISPATCH_TABLE = {
            "CZ": cls.emit_cz,
            "GlobalRz": cls.emit_global_rz,
            "GlobalW": cls.emit_global_w,
            "LocalRz": cls.emit_local_rz,
            "LocalW": cls.emit_local_w,
            "Measurement": cls.emit_measurement,
        }
        cls._APPLY_DISPATCH_TABLE = {
            "CZ": cls.apply_cz_loss,
            "GlobalRz": cls.apply_global_rz_loss,
            "GlobalW": cls.apply_global_w_loss,
            "LocalRz": cls.apply_local_rz_loss,
            "LocalW": cls.apply_local_w_loss,
            "Measurement": cls.apply_measurement_loss,
        }

        return super().__pydantic_init_subclass__(**kwargs)

    @staticmethod
    @abc.abstractmethod
    def remove_lost_qubits(
        circuit: CircuitType, active_qubits: np.ndarray[Any, bool]
    ) -> CircuitType:
        pass

    @abc.abstractmethod
    def emit_initialize(self) -> CircuitType:
        pass

    @abc.abstractmethod
    def emit_cz(self, gate_event: CZ) -> CircuitType:
        pass

    @abc.abstractmethod
    def emit_global_rz(self, gate_event: GlobalRz) -> CircuitType:
        pass

    @abc.abstractmethod
    def emit_global_w(self, gate_event: GlobalW) -> CircuitType:
        pass

    @abc.abstractmethod
    def emit_local_rz(self, gate_event: LocalRz) -> CircuitType:
        pass

    @abc.abstractmethod
    def emit_local_w(self, gate_event: LocalW) -> CircuitType:
        pass

    @abc.abstractmethod
    def emit_measurement(self, gate_event: Measurement) -> CircuitType:
        pass

    def apply_initialize_loss(
        self, circuit: CircuitType, active_qubits: np.ndarray[Any, bool]
    ) -> CircuitType:
        return self.remove_lost_qubits(circuit, active_qubits)

    def apply_cz_loss(
        self,
        circuit: CircuitType,
        active_qubits: np.ndarray[Any, bool],
    ) -> CircuitType:
        return self.remove_lost_qubits(circuit, active_qubits)

    def apply_global_rz_loss(
        self, circuit: CircuitType, active_qubits: np.ndarray[Any, bool]
    ) -> CircuitType:
        return self.remove_lost_qubits(circuit, active_qubits)

    def apply_global_w_loss(
        self, circuit: CircuitType, active_qubits: np.ndarray[Any, bool]
    ) -> CircuitType:
        return self.remove_lost_qubits(circuit, active_qubits)

    def apply_local_rz_loss(
        self, circuit: CircuitType, active_qubits: np.ndarray[Any, bool]
    ) -> CircuitType:
        return self.remove_lost_qubits(circuit, active_qubits)

    def apply_local_w_loss(
        self, circuit: CircuitType, active_qubits: np.ndarray[Any, bool]
    ) -> CircuitType:
        return self.remove_lost_qubits(circuit, active_qubits)

    @abc.abstractmethod
    def apply_measurement_loss(
        self, circuit: CircuitType, active_qubits: np.ndarray[Any, bool]
    ) -> CircuitType:
        pass

    @staticmethod
    @abc.abstractmethod
    def join(circuits: List[CircuitType]) -> CircuitType:
        pass

    def apply_losses(
        self,
        gate_event: Operation,
        result: CircuitType,
        active_qubits: np.ndarray[Any, bool],
    ) -> CircuitType:
        return self._APPLY_DISPATCH_TABLE[gate_event.name](self, result, active_qubits)

    def emit(
        self, gate_event: Operation, active_qubits: np.ndarray[Any, bool]
    ) -> CircuitType:

        if gate_event not in self._lazy_gate_cache:
            result = self._EMIT_DISPATCH_TABLE[gate_event.name](self, gate_event)
            self._lazy_gate_cache[gate_event] = result
        else:
            result = self._lazy_gate_cache[gate_event]

        return self.apply_losses(gate_event, result, active_qubits)


@python_dataclass
class CZNoiseResults(Generic[CircuitType]):
    storage_error: CircuitType
    entangled_error: CircuitType
    single_error: CircuitType
    participants: Tuple[Union[Tuple[int], Tuple[int, int]], ...]


class NoiseModelConstructorABC(CircuitConstructorABC[CircuitType]):
    noise_parameters: NoiseModelParameters

    @abc.abstractmethod
    def emit_cz(self, gate_event: CZ) -> CZNoiseResults[CircuitType]:
        pass

    def _cz_participation_masks(self, participants, active_qubits):
        non_participants = set(range(self.num_qubits)) - set(sum(participants, ()))
        non_participants = list(non_participants)

        # get participants that are single qubits or a pair of qubits with at least one inactive qubit
        single_qubit_participants = (
            participant
            for participant in participants
            if len(participant) == 1
            or not active_qubits[participant[0]]
            or not active_qubits[participant[1]]
        )
        # get participants that are pairs of active qubits
        entangled_qubit_participants = (
            participant
            for participant in participants
            if len(participant) == 2
            and active_qubits[participant[0]]
            and active_qubits[participant[1]]
        )

        # flatten the generator
        single_qubit_participants = list(sum(single_qubit_participants, ()))
        entangled_qubit_participants = list(sum(entangled_qubit_participants, ()))

        # create a copy of the active qubits
        active_single_qubit = active_qubits.copy()
        active_entangled_qubit = active_qubits.copy()
        # remove qubits that are not participating in the CZ gate
        active_entangled_qubit[non_participants] = False
        active_single_qubit[non_participants] = False
        # remove qubits that are in gate zone and are not paired up
        active_entangled_qubit[single_qubit_participants] = False
        # remove qubits that are in active zone and are not paired up
        active_single_qubit[entangled_qubit_participants] = False

        return active_single_qubit, active_entangled_qubit

    def apply_cz_loss(
        self,
        no_loss_results: CZNoiseResults[CircuitType],
        active_qubits: np.ndarray[Any, bool],
    ) -> CircuitType:

        storage_error = no_loss_results.storage_error
        entangled_error = no_loss_results.entangled_error
        single_error = no_loss_results.single_error
        participants = no_loss_results.participants

        active_single_qubit, active_entangled_qubit = self._cz_participation_masks(
            participants, active_qubits
        )

        entangled_error = self.remove_lost_qubits(
            entangled_error, active_entangled_qubit
        )
        single_error = self.remove_lost_qubits(single_error, active_single_qubit)
        storage_error = self.remove_lost_qubits(storage_error, active_qubits)

        return self.join([storage_error, single_error, entangled_error])

    @abc.abstractmethod
    def generate_trap_idle_error(self, noise_metric: NoiseMetrics) -> CircuitType:
        pass

    @abc.abstractmethod
    def generate_aod_trap_transfer_error(
        self, noise_metric: NoiseMetrics
    ) -> CircuitType:
        pass

    def apply_losses(
        self,
        gate_event: Operation,
        result: Union[CircuitType, CZNoiseResults[CircuitType]],
        idle_error: CircuitType,
        transfer_error: CircuitType,
        active_qubits: np.ndarray[Any, bool],
    ) -> CircuitType:
        result = self._APPLY_DISPATCH_TABLE[gate_event.name](
            self, result, active_qubits
        )
        idle_error = self.remove_lost_qubits(idle_error, active_qubits)
        transfer_error = self.remove_lost_qubits(transfer_error, active_qubits)

        return self.join([idle_error, transfer_error, result])

    def emit(
        self, gate_event: Operation, active_qubits: np.ndarray[Any, bool]
    ) -> CircuitType:
        if gate_event not in self._lazy_gate_cache:
            idle_error = self.generate_trap_idle_error(gate_event.noise_metrics)
            transfer_error = self.generate_aod_trap_transfer_error(
                gate_event.noise_metrics
            )
            result = self._EMIT_DISPATCH_TABLE[gate_event.name](self, gate_event)
            self._lazy_gate_cache[gate_event] = (result, idle_error, transfer_error)
        else:
            (result, idle_error, transfer_error) = self._lazy_gate_cache[gate_event]

        return self.apply_losses(
            gate_event, result, idle_error, transfer_error, active_qubits
        )

    @abc.abstractmethod
    def run(self, noise_model: CircuitType, measure_tags: Set[str]) -> str:
        pass


CleanClassType = TypeVar("CleanClassType", bound=CircuitConstructorABC)
NoiseClassType = TypeVar("NoiseClassType", bound=NoiseModelConstructorABC)


class CircuitConstructorRegistry(BaseModel):
    _CLEAN_CONSTRUCTOR: ClassVar[Dict[str, Type[CircuitConstructorABC]]] = {}
    _NOISE_CONSTRUCTOR: ClassVar[Dict[str, Type[NoiseModelConstructorABC]]] = {}

    def __str__(self) -> str:
        return f"Clean: {self._CLEAN_CONSTRUCTOR}, Noise: {self._NOISE_CONSTRUCTOR}"

    @classmethod
    def register_clean(cls, backend_name: str):

        def _decorator(
            constructor: Type[CleanClassType],
        ) -> Type[CleanClassType]:
            assert issubclass(
                constructor, CircuitConstructorABC
            ), "Clean constructor must be a subclass of CircuitConstructorABC"
            cls._CLEAN_CONSTRUCTOR[backend_name] = constructor

            return constructor

        return _decorator

    @classmethod
    def register_noise(cls, backend_name: str):
        def _noise_decorator(
            constructor: Type[NoiseClassType],
        ) -> Type[NoiseClassType]:

            assert issubclass(
                constructor, NoiseModelConstructorABC
            ), "Noise constructor must be a subclass of NoiseModelConstructorABC"
            cls._NOISE_CONSTRUCTOR[backend_name] = constructor

            return constructor

        return _noise_decorator

    def get_generators(
        self,
        backend_name: str,
        num_qubits: int,
        noise_parameters: NoiseModelParameters = NoiseModelParameters(),
    ) -> Tuple[CircuitConstructorABC, NoiseModelConstructorABC]:
        try:
            clean_constructor = self._CLEAN_CONSTRUCTOR[backend_name](
                num_qubits=num_qubits
            )
        except KeyError:
            raise ValueError(f"Backend {backend_name} not registered")

        try:
            noise_constructor = self._NOISE_CONSTRUCTOR[backend_name](
                num_qubits=num_qubits, noise_parameters=noise_parameters
            )
        except KeyError:
            raise ValueError(f"Backend {backend_name} not registered")

        return clean_constructor, noise_constructor


@python_dataclass
class AtomLossCircuitSampler(Generic[CircuitType]):
    gate_events: List[Operation]
    circuit_generator: CircuitConstructorABC[CircuitType]
    noise_generator: NoiseModelConstructorABC[CircuitType]
    loss_prob_calculator: InitVar[SurvivalProbabilityCalculator]

    survival_probs: np.ndarray[float] = python_field(init=False)
    num_qubits: int = python_field(init=False)
    measure_tags: Set[str] = python_field(init=False, default_factory=set)

    def __post_init__(self, loss_prob_calculator: SurvivalProbabilityCalculator):
        assert self.circuit_generator.num_qubits == loss_prob_calculator.num_qubits

        self.num_qubits = loss_prob_calculator.num_qubits
        assert (
            self.circuit_generator.num_qubits == self.num_qubits
        ), "Circuit generator must have the same number of qubits as the noise generator"
        assert (
            self.noise_generator.num_qubits == self.num_qubits
        ), "Noise generator must have the same number of qubits as the circuit generator"

        self.survival_probs = np.asarray(
            list(map(loss_prob_calculator.emit, self.gate_events))
        )
        self.survival_probs = self.survival_probs.reshape(
            (len(self.gate_events), self.num_qubits)
        )

        assert self.survival_probs.shape == (
            len(self.gate_events),
            self.num_qubits,
        ), "Survival probabilities must be of shape (num_gates, num_qubits)"

        measure_tags = [
            gate.measure_tag
            for gate in self.gate_events
            if isinstance(gate, Measurement)
        ]
        self.measure_tags.update(measure_tags)
        assert len(self.measure_tags) == len(
            measure_tags
        ), "Duplicate measurement tags found in gate events"
        assert (
            self.num_qubits == 0 or len(self.measure_tags) > 0
        ), "No measurement tags found in gate events"

    def active_qubit_states(
        self, generator: Optional[np.random.Generator] = None
    ) -> np.ndarray[Any, bool]:
        """Sample the survival state for each all gate events.

        The comprod is used to calculate the survival state of each atom for each subsequent gate event.
        If an atom is lost in a previous gate event, it will be lost in all subsequent gate events.

        """
        if generator is None:
            generator = np.random.default_rng()

        return (
            (
                generator.random(size=(len(self.gate_events), self.num_qubits))
                <= self.survival_probs
            )
            .cumprod(axis=0)
            .astype(bool)
        )

    @cached_property
    def clean_circuit(self) -> CircuitType:
        # assume qubits are always active for clean circuit
        active_qubits = np.ones_like(self.survival_probs, dtype=bool)
        return self.circuit_generator.join(
            list(map(self.circuit_generator.emit, self.gate_events, active_qubits[:]))
        )

    def generate_model(
        self, generator: Optional[np.random.Generator] = None
    ) -> CircuitType:
        active_qubits = self.active_qubit_states(generator)
        gates = list(
            map(self.circuit_generator.emit, self.gate_events, active_qubits[:])
        )
        noise = list(map(self.noise_generator.emit, self.gate_events, active_qubits[:]))

        circuits = []
        for gate, noise in zip(gates, noise):
            circuits.append(noise)
            circuits.append(gate)

        return self.noise_generator.join(circuits)

    def run(self, shots: int) -> Dict[str, Dict[str, int]]:
        counters = {tag: Counter() for tag in self.measure_tags}
        for _ in range(shots):
            noise_model = self.generate_model()
            results = self.noise_generator.run(noise_model, self.measure_tags)
            for tag, result in results.items():
                counters[tag][result] += 1

        return {tag: dict(counter) for tag, counter in counters.items()}


OperationUnion = Union[CZ, GlobalRz, GlobalW, LocalRz, LocalW, Measurement]


class Gate(BaseModel):
    operation: OperationUnion = Field(union_mode="left_to_right", discriminator="name")


class Circuit(BaseModel, extra="forbid"):
    num_qubits: int
    gates: List[Gate] = Field(default_factory=list)
    CIRCUIT_REGISTRY: ClassVar[CircuitConstructorRegistry] = (
        CircuitConstructorRegistry()
    )

    # TODO: add custom validator to check to make sure no measurements
    #       are done in the middle of the circuit.

    def get_sampler(
        self,
        backend_name: str,
        noise_parameters: NoiseModelParameters = NoiseModelParameters(),
    ) -> "AtomLossCircuitSampler":
        clean, noise = self.CIRCUIT_REGISTRY.get_generators(
            backend_name, self.num_qubits, noise_parameters
        )

        return AtomLossCircuitSampler(
            gate_events=[block.operation for block in self.gates],
            circuit_generator=clean,
            noise_generator=noise,
            loss_prob_calculator=SurvivalProbabilityCalculator(
                num_qubits=self.num_qubits, noise_parameters=noise_parameters
            ),
        )

    def append(self, op: Operation):
        if not isinstance(op, Operation):
            raise ValueError(f"Cannot append {type(op)} to Circuit")

        self.gates.append(Gate(operation=op))

    def __add__(self, other: "Circuit") -> "Circuit":
        if not isinstance(other, Circuit):
            raise ValueError(f"Cannot add {type(other)} to Circuit")

        if self.num_qubits != other.num_qubits:
            raise ValueError("Circuits must have the same number of qubits")

        return Circuit(
            num_qubits=self.num_qubits,
            gates=self.gates + other.gates,
        )
