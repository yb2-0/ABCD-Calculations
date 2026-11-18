"""
INPUTS FOR THE PIPELINE. Everything here is chosen by hand.
Results that the scripts compute (like f1 and d1) are written to txt_files/, not stored here.
"""

'''RUN NAME'''
# Names every output: txt_files/<RUN_NAME>_optimal_f1.txt, txt_files/<RUN_NAME>_final_results.txt,
# plots/<RUN_NAME>/. Change it whenever you change the inputs below, so different setups don't
# overwrite each other.
RUN_NAME = "new_mfd_200"

'''FIBER MODE CONSTANTS'''
# from OZ Optics email. These are calculated values with tolerance \pm 0.5 µm. They aren't experimental results.
wvln_to_MFR = {1112: 3.15, 556: 1.85, 604: 2.0, 798: 2.7, 978: 2.95, 1034: 3.05, 1389: 4.75, 1580: 5.3} # in µm

'''CAVITY CONSTANTS'''
R = 0.5  # Radius of curvature of the second cavity mirror (m)
L = 0.1  # Length between cavity mirrors (m)

'''LENS AND SPACING CHOICES'''
# Every wavelength with an f2 here gets run; to add one, it also needs an MFR and a total distance.
wvln_to_f2 = {1112: 0.35, 556: 0.5, 604: 0.6, 978: 0.75, 1034: 0.6, 1389: 0.5, 1580: 0.35} # in m

# Fixed spacing from the fiber to f2 (d1 + d12) for each wavelength.
wvln_to_total_distance = {1112: 0.20, 556: 0.20, 604: 0.20, 978: 0.20, 1034: 0.20, 1389: 0.20, 1580: 0.20} # in m

# bore 1 is 1112 and 556, bore 2 is 604, bore 3 is 1034 and 978, bore 4 is 1389 and 1580.
# now:

'''f1 CATALOG'''
# Lenses that step 1 (perfectly_collimated.py) chooses f1 from.
f1_options = [0.0015, 0.002, 0.0028, 0.003, 0.0031, 0.0033, 0.004, 0.0045,
              0.00451, 0.0046, 0.0055, 0.0062, 0.00624, 0.0075, 0.008, 0.0096,
              0.011, 0.0139, 0.0153, 0.0184]  # in m
