import sys
import json

trace = {'occ_c52783 <-> thm_af5e18': 'Explicit directional rule: occ_c52783 -> thm_af5e18 = 0.95', 'occ_c52783 <-> sub_0ae325': 'Explicit directional rule: occ_c52783 -> sub_0ae325 = 0.95', 'occ_c52783 <-> act_7a7a2e': 'Neutral fallback (no semantic overlap)', 'occ_c52783 <-> env_898671': 'Neutral fallback (no semantic overlap)', 'occ_c52783 <-> mod_128b31': "Intrinsic Affinity (0.75): Source explicit affinity for 'Happy'", 'occ_c52783 <-> sty_6ea299': "Intrinsic Affinity (0.75): Source explicit affinity for 'Cartoon'", 'occ_c52783 <-> vis_f80d19': 'Neutral fallback (no semantic overlap)', 'occ_c52783 <-> cmp_3da76e': 'Neutral fallback (no semantic overlap)', 'occ_c52783 <-> pal_292614': 'Explicit directional rule: occ_c52783 -> pal_292614 = 1.0', 'occ_c52783 <-> dec_f43c97': 'Explicit directional rule: occ_c52783 -> dec_f43c97 = 0.95', 'occ_c52783 <-> tex_ff83c5': 'Neutral fallback (no semantic overlap)', 'occ_c52783 <-> eff_b55669': 'Neutral fallback (no semantic overlap)', 'thm_af5e18 <-> sub_0ae325': 'Neutral fallback (no semantic overlap)'}

for k, v in trace.items():
    print(k, v)
