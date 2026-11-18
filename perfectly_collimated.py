"""
STEP 1: choose f1 for each wavelength.

f2 and the total distance (d1 + d12) are fixed in constants.py. Every lens in f1_options is tried
with d1 = f1 and d2 = f2, and the f1 whose beam radius at the cavity is closest to the cavity
waist is kept.

Writes txt_files/<RUN_NAME>_optimal_f1.txt, which ideally_collimated.py (step 2) reads.
To use a different f1 for a wavelength, edit its "f1 = ..." line in that file before running step 2.
"""
from ABCD import evaluate
from constants import wvln_to_f2, wvln_to_total_distance, f1_options
from results_io import OPTIMAL_F1_FILE, write_results

solutions = []
for wavelen, f2 in wvln_to_f2.items():
    total_distance = wvln_to_total_distance[wavelen]
    candidates = (evaluate(wavelen, f1, f1, total_distance - f1, f2, f2) for f1 in f1_options)
    solutions.append(min(candidates, key=lambda s: s["waist_error"]))

write_results(OPTIMAL_F1_FILE, solutions, "perfectly_collimated.py")
