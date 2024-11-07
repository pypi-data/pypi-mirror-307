# Copyright (c) 2024, QuEra Computing Inc.
# All rights reserved.

import dataclasses
import pandas as pd
from pandas import DataFrame
from io import StringIO

from flair_visual.animation.runtime import qpustate as vis_qpustate


@dataclasses.dataclass
class QuEraSimulationResult:
    flair_visual_version: str
    counts: dict[str, int]
    logs: DataFrame
    atom_animation_state: vis_qpustate.AnimateQPUState

    @classmethod
    def from_json(cls, json: dict) -> "QuEraSimulationResult":
        flair_visual_version = json["flair_visual_version"]
        counts = json["measurementCounts"]
        logs = pd.read_csv(StringIO(json["simulation_details"]["logs"]), index_col=0)
        atom_animation_state = vis_qpustate.AnimateQPUState.from_json(
            json["simulation_details"]["atom_animation_state"]
        )

        return cls(
            flair_visual_version=flair_visual_version,
            counts=counts,
            logs=logs,
            atom_animation_state=atom_animation_state,
        )

    def animate(
        self,
        dilation_rate: float = 0.05,
        fps: int = 30,
        gate_display_dilation: float = 1.0,
        save_mpeg: bool = False,
        filename: str = "vqpu_animation",
        start_block: int = 0,
        n_blocks: int = None,
    ):
        """animate the qpu state

        Args:
            dilation_rate (float): Conversion factor from the qpu time to animation time units. when dilation_rate=1.0, 1 (us) of qpu exec time corresponds to 1 second of animation time.
            fps (int, optional): frame per second. Defaults to 30.
            gate_display_dilation (float, optional): relative dilation rate of a gate event. Defaults to 1. When setting higher value, the gate event will be displayed longer.
            save_mpeg (bool, optional): Save as mpeg. Defaults to False.
            filename (str, optional): The file name of saved mpeg file. Defaults to "vqpu_animation". When `save_mpeg` is False, this argument is ignored.
            start_block (int, optional): The start block to animate. Defaults to 0.
            n_blocks (int, optional): number of blocks to animate. Defaults to None. When None, animate all blocks after `start_block`.
        """
        from flair_visual.animation.animate import animate_qpu_state

        ani = animate_qpu_state(
            state=self.atom_animation_state,
            dilation_rate=dilation_rate,
            fps=fps,
            gate_display_dilation=gate_display_dilation,
            start_block=start_block,
            n_blocks=n_blocks,
            save_mpeg=save_mpeg,
            filename=filename,
        )
        return ani
