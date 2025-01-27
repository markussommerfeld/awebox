#!/usr/bin/python3

import awebox as awe
import matplotlib.pyplot as plt
import numpy as np

# dual kite with point-mass model
options = {}
options['user_options.system_model.architecture'] = {1:0, 2:1, 3:1}
options['user_options.system_model.kite_dof'] = 3
options['user_options.kite_standard'] = awe.ampyx_data.data_dict()

# trajectory should be a single pumping cycle with initial number of one windings
options['user_options.trajectory.type'] = 'power_cycle'
options['user_options.trajectory.system_type'] = 'lift_mode'
options['user_options.trajectory.lift_mode.windings'] = 1

# don't include induction effects
options['user_options.wind.u_ref'] = 5.0 # m/s
options['user_options.induction_model'] = 'not_in_use'

# compute optimal design at reference wind speed
trial = awe.Trial(seed = options, name = 'opt_design')
trial.build()
trial.optimize()

# fix optimal design for wind speed sweep
fixed_params = {}
for name in list(trial.model.variables_dict['theta'].keys()):
    if ('diam' in name) or (name == 'l_s') or (name == 'l_i'):
        fixed_params[name] = trial.optimization.V_final['theta',name].full()
options['user_options.trajectory.fixed_params'] = fixed_params

# set-up sweep options
sweep_opts = [('user_options.wind.u_ref', np.linspace(5,9,5, endpoint=True))]

sweep = awe.Sweep(name = 'dual_kites_power_curve', options = options, seed = sweep_opts)
sweep.build()
sweep.run(apply_sweeping_warmstart = True)
sweep.plot(['comp_stats', 'comp_convergence'])
plt.show()
