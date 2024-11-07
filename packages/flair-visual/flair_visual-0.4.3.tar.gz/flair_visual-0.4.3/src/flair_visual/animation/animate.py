from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import functools
import bisect
from typing import Optional

from flair_visual.animation.runtime.qpustate import QPUStateABC
from flair_visual.animation.base import FieldOfView, GatePainter, quera_color_code
import tqdm


def animate_qpu_state(
    state: QPUStateABC,
    display_fov: Optional[FieldOfView] = None,
    dilation_rate: float = 0.05,
    fps: int = 30,
    gate_display_dilation: float = 1.0,
    fig_args={},
    save_mpeg: bool = False,
    filename: str = "vqpu_animation",
    start_block: int = 0,
    n_blocks: int = None,
):
    qpu_fov = state.qpu_fov

    if display_fov is None:
        display_fov = qpu_fov

    if start_block >= len(state.block_durations) or start_block < 0:
        raise ValueError("Start block index is out of range")

    if n_blocks is None:
        n_blocks = len(state.block_durations) - start_block

    if n_blocks < 0:
        raise ValueError("Number of block to animate must be non-negative")

    slm_sites = state.get_slm_sites()

    # figure:
    new_fig_args = {"figsize": (14, 8), **fig_args}
    fig, mpl_axs = plt.subplot_mosaic(
        mosaic=[["Reg", "Info"], ["Reg", "Gate"], ["Reg", "Gate"]],
        gridspec_kw={"width_ratios": [3, 1]},
        **new_fig_args,
    )

    # mpl_axs["Reg"].axis("equal")  # Axis equal must come before axis limits
    mpl_axs["Reg"].set_xlim(left=display_fov.xmin, right=display_fov.xmax)
    mpl_axs["Reg"].set_ylim(bottom=display_fov.ymin, top=display_fov.ymax)
    mpl_axs["Reg"].grid(True)
    mpl_axs["Reg"].set(xlabel="x (um)", ylabel="y (um)")

    # slm:
    slm_plt_arg = {
        "facecolors": "none",
        "edgecolors": "k",
        "linestyle": "--",
        "s": 80,
        "alpha": 0.4,
    }
    mpl_axs["Reg"].scatter(
        x=slm_sites[:, 0], y=slm_sites[:, 1], **slm_plt_arg
    )  # this is statically generated, so it will be the background

    # atoms:
    reg_plt_arg = {
        "s": 65,
        "marker": "o",
        "facecolors": quera_color_code.purple,
        "alpha": 1.0,
    }
    reg_panel = mpl_axs["Reg"]
    reg_scat = reg_panel.scatter([], [], **reg_plt_arg)

    # gates:
    gp = GatePainter(mpl_ax=reg_panel, qpu_fov=qpu_fov)

    # annotate_args = {"fontsize": 8, "ha": "center", "alpha": 0.7, "color": quera_color_code.yellow}
    annotate_args = {
        "fontsize": 6,
        "ha": "center",
        "va": "center",
        "alpha": 1.0,
        "color": quera_color_code.yellow,
        "weight": "bold",
    }
    reg_annot_list = [
        reg_panel.annotate(f"{i}", atom_position, **annotate_args)
        for i, atom_position in state.get_atoms_position(time=0.0, include_lost=False)
    ]

    # AODs:
    aod_plot_args = {
        "s": 200,
        "marker": "+",
        "alpha": 0.9,
        "facecolors": quera_color_code.red,
    }
    aod_scat = reg_panel.scatter(x=[], y=[], **aod_plot_args)

    ## Info Panel
    info_text = mpl_axs["Info"].text(x=0.05, y=0.5, s="")
    mpl_axs["Info"].set_xticks([])
    mpl_axs["Info"].set_yticks([])
    mpl_axs["Info"].grid(False)

    ## Event Panel:
    log_text = mpl_axs["Gate"].text(x=0.05, y=0.0, s="", size=6)
    mpl_axs["Gate"].set_xticks([])
    mpl_axs["Gate"].set_yticks([])
    mpl_axs["Gate"].grid(False)

    tstep_mv = 1.0 / (fps * dilation_rate)
    tstep_gate = 1.0 / (fps * dilation_rate * gate_display_dilation)
    blk_t_end = np.cumsum(state.block_durations)

    # determine the dilation part of the timeline, and generate more frame
    chunk_times = []
    curr_t = 0 if start_block == 0 else blk_t_end[start_block - 1]

    for glb_tstart_gate, duration in state.get_gate_events_timing():
        if glb_tstart_gate < curr_t:  # gate start before the current time
            if glb_tstart_gate + duration < curr_t:
                continue
        else:
            dt = glb_tstart_gate - curr_t
            chunk_times.append(np.linspace(curr_t, glb_tstart_gate, int(dt / tstep_mv)))
            curr_t = glb_tstart_gate

        t_gate_end = glb_tstart_gate + duration
        dt = t_gate_end - curr_t
        chunk_times.append(np.linspace(curr_t, t_gate_end, int(dt / tstep_gate)))
        curr_t = t_gate_end

    dt = blk_t_end[-1] - curr_t
    chunk_times.append(np.linspace(curr_t, blk_t_end[-1], int(dt / tstep_mv)))

    times = np.concatenate(chunk_times)

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.1)

    def _update_annote(loc, idx, annote_artist):
        new_loc = (loc[0], loc[1] - 0.06)
        annote_artist.set_position(new_loc)
        txt = f"{idx}"
        annote_artist.set_text(txt)
        return loc

    def update(frame: int, state: QPUStateABC, times: np.ndarray, blk_t_end: np.array):

        # get positions:

        blk_id = bisect.bisect_left(blk_t_end, times[frame])
        lbl = f"Block: [{blk_id}]\n"
        lbl += f"Block dur: {state.block_durations[blk_id]:.2f} us\n"
        lbl += f"Total elapsed time: {times[frame]:.2f} us"
        info_text.set_text(lbl)

        # update atoms location and annotation
        post = np.array(
            [
                _update_annote(
                    atom_position,
                    i,
                    reg_annot_list[i],
                )
                for i, atom_position in state.get_atoms_position(
                    times[frame], include_lost=False
                )
            ]
        )
        post = post if post.size > 0 else np.array([(None, None)])
        reg_scat.set_offsets(post)

        # update log event panels
        lost_events = state.get_atoms_lost_info(times[frame])

        # update log gate:
        gate_events = state.get_gate_events(times[frame])
        gate_events_log = [
            f"Gate: {gate.cls_name} @ {t:.6f} (us)\n"
            for t, gate in state.get_gate_events(times[frame])
        ]
        log_text.set_text("".join(lost_events) + "".join(gate_events_log))

        gate_artists = gp.process_gates([gate for _, gate in gate_events])

        # update AODs
        post = state.sample_aod_traps(times[frame]) or [(None, None)]
        aod_scat.set_offsets(post)

        return [reg_scat, info_text, log_text, aod_scat] + reg_annot_list + gate_artists

    ani = FuncAnimation(
        fig=fig,
        func=functools.partial(update, state=state, times=times, blk_t_end=blk_t_end),
        frames=len(times),
        interval=tstep_mv,
        blit=True,
        repeat=False,
    )
    if save_mpeg:
        n_frame = len(times)
        pbar = tqdm.tqdm(range(n_frame))

        def p_call_back(i, total_n):
            pbar.update()

        ani.save(
            f"{filename}.mp4", writer="ffmpeg", fps=fps, progress_callback=p_call_back
        )
    else:
        return ani
