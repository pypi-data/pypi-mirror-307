from flair_visual.animation.runtime.ppoly import PPoly
from flair_visual.animation.gate_event import GateEvent
from flair_visual.animation.runtime.atoms import AtomTrajectory
from flair_visual.animation.runtime.aod import AODMoveEvent
from flair_visual.animation.runtime.qpustate import AnimateQPUState
import numpy as np
import json


def run_json_test(obj):
    assert hasattr(obj, "to_json")
    assert hasattr(type(obj), "from_json")

    obj_events_json = json.dumps(obj.to_json())
    obj_events_reconstructed = type(obj).from_json(json.loads(obj_events_json))
    assert obj == obj_events_reconstructed


def test_PPoly():
    x = np.array([0, 1, 2, 3, 4])
    c = np.random.rand(4, 5)
    ppoly = PPoly(c, x)

    run_json_test(ppoly)


def test_GateEvents():
    gate_events = GateEvent("Test", {"Test": 1}, 10.0)
    run_json_test(gate_events)


def test_AtomTrajectory():
    x_x = np.array([0, 1, 2, 3, 4])
    x_c = np.random.rand(4, 5)
    x = PPoly(x_c, x_x)

    y_x = np.array([0, 1, 2, 3, 4])
    y_c = np.random.rand(4, 5)
    y = PPoly(y_c, y_x)

    events = [(0.0, "Test"), (1.0, "Test")]

    atom_trajectory = AtomTrajectory(1, x, y, events)

    run_json_test(atom_trajectory)


def test_AODMoveEvent():
    x_x = np.array([0, 1, 2, 3, 4])
    x_c = np.random.rand(4, 5)
    x = PPoly(x_c, x_x)

    y_x = np.array([0, 1, 2, 3, 4])
    y_c = np.random.rand(4, 5)
    y = PPoly(y_c, y_x)

    aod_move_event = AODMoveEvent(1.0, 1.0, x, y)

    run_json_test(aod_move_event)


def test_AnimateQPUState():
    x_x = np.array([0, 1, 2, 3, 4])
    x_c = np.random.rand(4, 5)
    x = PPoly(x_c, x_x)

    y_x = np.array([0, 1, 2, 3, 4])
    y_c = np.random.rand(4, 5)
    y = PPoly(y_c, y_x)

    animate_qpu_state = AnimateQPUState(
        block_durations=[5.0],
        gate_events=[(3.0, GateEvent("Test", {"Test": 1}, 10.0))],
        atoms=[AtomTrajectory(1, x, y, [(0.0, "Test")])],
        slm_zone=[(0.0, 0.0)],
        aod_moves=[AODMoveEvent(1.0, 1.0, x, y)],
    )

    run_json_test(animate_qpu_state)
