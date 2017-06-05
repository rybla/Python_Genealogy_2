import genealogy
import dot_creator
import genealogy_inspector as gi
import testing
import numpy as np
from tqdm import tqdm

#-------------#
p_start = 1
p_end   = 2
p_it    = 1

r_start = 10
r_end   = 10.5
r_it    = 0.5

tests   = 10
#-------------#

parents_range = np.arange(p_start+p_it,p_end+p_it,p_it)
ratio_range = np.arange(r_start+r_it,r_end+r_it,r_it)

gi.calc_smoothed_percents_range(parents_range,ratio_range,tests)
gi.calc_exp_regressions(parents_range,ratio_range)

# gi.plot_percents_range([parents],ratio_range)
# gi.plot_exp_regressions(parents_range,ratio_range,x50=True)

# gi.plot_d50s(parents,ratio_range)
# gi.plot_d0s(parents_range,ratio_range)

# gi.title("Derivatives at Abundance=0,50")
# gi.legend()
# gi.show()

quit()