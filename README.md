# ABCD-Calculations

MOSTLY WAS UBER SPECIFIC TO A PROBLEM I WAS SOLVING AND MAY NOT BE HELPFUL AT ALL BEYOND THAT

This repo contains basic infrastructure for ABCD calculations as well as methods to sweep
parameters (e.g. focal lengths and distances) within an acceptable range to get a cavity coupling
system that fits physical requirements.

## The problem

Light from a fiber is coupled into a cavity through two lenses. Each wavelength is solved separately.

```
fiber ──d1──▶ [f1] ──────── d12 ────────▶ [f2] ──────── d2 ────────▶ cavity
└──────────── total_distance ────────────┘
```

- `total_distance = d1 + d12` is a fixed spacing that can be set per wavelength.
- The cavity sits at `d2 = f2`.
- Goal: the beam radius at the cavity should match the cavity mode waist, and the beam's waist
  should land at the cavity, so the beam is collimated there.

## Files

| File | Role |
|---|---|
| `constants.py` | All inputs, chosen by hand. It holds `RUN_NAME`, the fiber mode radius (`wvln_to_MFR`, µm), cavity `R`/`L`, and per-wavelength `wvln_to_f2` and `wvln_to_total_distance`. It also holds the `f1_options` lens catalog. Lengths are in m; wavelength keys are in nm. |
| `ABCD.py` | Core physics: the q-parameter helpers (`flat_q`, `prop_free`, `prop_lens`) and the cavity waist. `runner()` propagates fiber → f1 → f2 → d2. `evaluate()` wraps `runner()` and adds the two errors the pipeline scores on. |
| `results_io.py` | Builds the output file names from `RUN_NAME`, and writes and reads the results `.txt` files that the steps pass along. |
| `perfectly_collimated.py` | Step 1: picks f1. |
| `ideally_collimated.py` | Step 2: fine-tunes d1. Produces the final numbers. |
| `plot_collimate_results.py` | Step 3: plots beam profiles from step 2's results. |
| `txt_files/`, `plots/` | Outputs. See [Older results](#older-results) for files from before run names. |

## Pipeline

Run with the venv active (it needs numpy and matplotlib):

```
source .abcd_venv/bin/activate
```

**0. Edit `constants.py`.** Give `RUN_NAME` a new name for each new setup, then set the inputs.

**1. `python perfectly_collimated.py` → picks f1.**
For each wavelength, it tries every lens in `f1_options` with `d1 = f1` and `d2 = f2`. It keeps
the f1 whose beam radius at the cavity is closest to the cavity waist.
Writes `txt_files/<RUN_NAME>_optimal_f1.txt`.

**2. `python ideally_collimated.py` → the final answer.**
It reads f1 from step 1's file. Then it scans d1 over ±3% of f1 (10,001 points) and keeps the d1
whose output waist lands closest to the cavity (smallest `d2 error`). The result is the layout
to build. Writes `txt_files/<RUN_NAME>_final_results.txt`.

**3. `python plot_collimate_results.py` → beam profile plots.**
It plots beam radius vs. distance for each wavelength, with lens positions and waists marked.
Writes `plots/<RUN_NAME>/`.

Outputs always go to `txt_files/` and `plots/`, whichever folder you run from.

### Run names

- Every file from one run starts with its run name, so you can tell which setup made it. Rerunning
  with the same `RUN_NAME` overwrites that run's files.
- Step 2 stops with an error if step 1's file is missing. It also stops if `f2` or
  `total_distance` in `constants.py` no longer match what step 1 used. Then rerun step 1 or
  change `RUN_NAME`.
- To use a different f1 than step 1 picked (e.g. a lens you already have), edit that wavelength's
  `f1 = ...` line in `<RUN_NAME>_optimal_f1.txt` before running step 2.

### Adding a wavelength

1. Add it to `wvln_to_MFR`, `wvln_to_f2`, and `wvln_to_total_distance` in `constants.py`. Every
   wavelength with an f2 is run.
2. Run steps 1–3.

## Reading a results file

Both steps write the same format, with one block per wavelength:

- **Layout:** `f1`, `f2`, `d1`, `d12`, `d2`.
- **`Ideal d2`:** where the output waist actually lands.
- **Waists:** `Input waist` (fiber), `Max waist` (waist size after f2), `Cavity waist` (the target),
  and `Output waist` (beam radius at d2).
- **Errors:**
  - `Waist error`: |output − cavity waist|.
  - `Fractional error`: (output − cavity waist) / cavity waist, as a signed percentage.
  - `d2 error`: |`d2` − `Ideal d2`|.
- **`Output ROC`:** the wavefront radius of curvature at d2. Large means close to flat.

## Notes

Step 1's choice of f1 doesn't depend on `total_distance`. With `d2 = f2`, the cavity sits at the
back focal plane of f2. The beam radius there depends only on the size of the waist entering f2,
not on where that waist is, so d12 drops out. That's why 200 mm and 250 mm runs pick the same f1.
Step 2's d1 and final waist error do depend on the distance.

## Older results

Files in `txt_files/` and `plots/` that don't follow the `<RUN_NAME>_...` pattern are from before
run names existed.

- The `new_mfd_*` files are the most recent. Running with `RUN_NAME = "new_mfd_200"` at
  200 mm reproduces `new_mfd_optimal_waist.txt` and `new_mfd_final_results.txt` exactly.
  `"new_mfd_250"` at 250 mm reproduces the `_250` versions.
- The rest predate the updated OZ Optics fiber mode radii.

Two earlier approaches were replaced by this pipeline and removed:
- `ABCD_sweep.py`: a grid search over f1 × f2.
- `ABCD_collimate.py`: a joint scan of d1 and d2.

Their plotting scripts were removed too. All of them are in git history before the cleanup commit.
