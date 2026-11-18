"""
STEP 2: fine-tune d1 so the beam's waist lands at the cavity (d2 = f2). These are the final numbers.

Reads f1 for each wavelength from step 1's output (txt_files/<RUN_NAME>_optimal_f1.txt), scans d1
over a small window around f1, and keeps the d1 with the smallest d2 error.

Writes txt_files/<RUN_NAME>_final_results.txt, which plot_collimate_results.py (step 3) reads.
"""
import numpy as np

from ABCD import evaluate
from constants import wvln_to_f2, wvln_to_total_distance
from results_io import OPTIMAL_F1_FILE, FINAL_RESULTS_FILE, read_results, write_results

################################ SEARCH SETTINGS ###############################
d1_neg_delta = 0.03      # scan d1 from 3% under f1...
d1_pos_delta = 0.03      # ...to 3% over f1
num_points = 10001
###############################################################################

step1 = read_results(OPTIMAL_F1_FILE)

solutions = []
for wavelen, f2 in wvln_to_f2.items():
    total_distance = wvln_to_total_distance[wavelen]

    # make sure step 1 was run with the same inputs that are in constants.py now
    if wavelen not in step1:
        raise SystemExit(f"No f1 for {wavelen} nm in {OPTIMAL_F1_FILE.name}. Rerun perfectly_collimated.py.")
    s1 = step1[wavelen]
    if abs(s1["f2"] - f2) > 1e-6 or abs(s1["d1"] + s1["d12"] - total_distance) > 1e-6:
        raise SystemExit(f"{wavelen} nm: f2 or total distance in constants.py changed since step 1 ran. "
                         "Rerun perfectly_collimated.py (or change RUN_NAME).")

    f1 = s1["f1"]
    d1_values = np.linspace(f1 * (1 - d1_neg_delta), f1 * (1 + d1_pos_delta), num_points)
    candidates = (evaluate(wavelen, d1, f1, total_distance - d1, f2, f2) for d1 in d1_values)
    solutions.append(min(candidates, key=lambda s: s["d2_error"]))

write_results(FINAL_RESULTS_FILE, solutions, "ideally_collimated.py")
