"""
Reads and writes the results .txt files that the pipeline steps pass to each other.
Every file name comes from RUN_NAME in constants.py.
"""
from pathlib import Path
import re

from constants import RUN_NAME

TXT_DIR = Path(__file__).with_name("txt_files")
OPTIMAL_F1_FILE = TXT_DIR / f"{RUN_NAME}_optimal_f1.txt"        # step 1 writes, step 2 reads
FINAL_RESULTS_FILE = TXT_DIR / f"{RUN_NAME}_final_results.txt"  # step 2 writes, step 3 reads
PLOTS_DIR = Path(__file__).with_name("plots") / RUN_NAME         # step 3 writes


def write_results(path, solutions, script_name):
    """Write one block per wavelength. `solutions` is a list of dicts from ABCD.evaluate()."""
    lines = [f"Run: {RUN_NAME} (written by {script_name})"]
    for s in solutions:
        lines += [
            "",
            "=" * 60,
            f"{s['wvlen']} nm - BEST SOLUTION",
            "=" * 60,
            f"f1           = {s['f1']*1e3:.4f} mm",
            f"f2           = {s['f2']*1e3:.4f} mm",
            f"d1           = {s['d1']*1e3:.6f} mm",
            f"d12          = {s['d12']*1e3:.6f} mm",
            f"d2           = {s['d2']*1e3:.3f} mm",
            f"Ideal d2     = {s['d2_ideal']*1e3:.3f} mm",
            "",
            f"Input waist  = {s['w_i']*1e6:.3f} μm",
            f"Max waist    = {s['max_waist']*1e6:.3f} μm",
            f"Cavity waist = {s['w_c']*1e6:.3f} μm",
            f"Output waist = {s['w_o']*1e6:.3f} μm",
            "",
            f"Waist error      = {s['waist_error']*1e6:.6f} μm",
            f"Fractional error = {100*(s['w_o']-s['w_c'])/s['w_c']:.6f} %",
            f"d2 error         = {s['d2_error']*1e3:.6f} mm",
            "",
            f"Output ROC   = {s['R_o']} m",
            "=" * 60,
        ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {path}")


# label in the file -> key in the dict, and unit -> factor to convert to SI
_FIELDS = {"f1": "f1", "f2": "f2", "d1": "d1", "d12": "d12", "d2": "d2", "Ideal d2": "d2_ideal",
           "Input waist": "w_i", "Max waist": "max_waist", "Cavity waist": "w_c", "Output waist": "w_o",
           "Waist error": "waist_error", "d2 error": "d2_error", "Output ROC": "R_o"}
_UNITS = {"mm": 1e-3, "μm": 1e-6, "µm": 1e-6, "m": 1.0, "": 1.0}


def read_results(path):
    """Read a file written by write_results. Returns {wavelength_nm: {key: value in SI units}}."""
    if not path.exists():
        raise SystemExit(f"{path.name} not found in {path.parent}. "
                         f"Run the previous step with RUN_NAME = {RUN_NAME!r} first.")
    results, current = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        header = re.match(r"(\d+) nm - BEST SOLUTION", line)
        if header:
            wvlen = int(header.group(1))
            current = results[wvlen] = {"wvlen": wvlen}
            continue
        field = re.match(r"(.+?)\s*=\s*(\S+)\s*(\S*)$", line.strip())
        if current is not None and field and field.group(1) in _FIELDS:
            current[_FIELDS[field.group(1)]] = float(field.group(2)) * _UNITS[field.group(3)]
    return results
