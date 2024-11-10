
import copy

import numpy as np
import pandapower as pp

from opfgym import OpfEnv


class SecurityConstrained(OpfEnv):
    def __init__(self, n_minus_one_lines: np.ndarray='all', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if n_minus_one_lines == 'all':
            n_minus_one_lines = self.net.line.index.values
        else:
            n_minus_one_lines = np.array(n_minus_one_lines)

    def calculate_violations(self, original_net=None):
        """ Implement the security constrained power flow by removing the n-1 lines and checking for violations. """
        original_net = original_net if original_net else self.net

        # Calculate the violations for the unchanged network
        valids, viol, penalties = super().calculate_violations(original_net)

        # Remove singular lines and add the resulting violations
        for line_idx in self.n_minus_one_lines:
            net = copy.deepcopy(original_net)
            # Remove the line
            pp.drop_lines(net, [line_idx])
            # Run the power flow (TODO: better use the build-in method -> change API)
            pp.runpp(net)
            # Check for violations in the updated copied network
            new_valids, new_viol, new_penalties = super().calculate_violations(net)
            # Update the violations
            valids = np.logical_and(valids, new_valids)
            viol += new_viol
            penalties += new_penalties

        return valids, viol, penalties

    def get_optimal_objective(self):
        # Overwrite because not solvable with pandapower OPF solver anymore.
        return 0

    def run_optimal_power_flow(self, **kwargs):
        # Overwrite because not solvable with pandapower OPF solver anymore.
        return False


class MultiStage(OpfEnv):
    def __init__(self,
                 steps_per_episode=4,
                 train_data='simbench',
                 test_data='simbench',
                 *args, **kwargs):

        assert steps_per_episode > 1, "At least two steps required for a multi-stage OPF."
        assert 'simbench' in train_data and 'simbench' in test_data, "Only simbench networks are supported because time-series data required."

        super().__init__(steps_per_episode=steps_per_episode,
                         train_data=train_data,
                         test_data=test_data,
                         *args, **kwargs)

    def step(self, action):
        """ Extend step method to sample the next time step of the simbench data. """
        obs, reward, terminated, truncated, info = super().step(action)

        # Increment the simbench step
        new_step = self.current_simbench_step + 1
        self._sampling(step=new_step)

        # Rerun the power flow calculation for the new state if required
        # TODO: This can result in two power flow calculations for each step() call. Is it possible to avoid this?
        # Not really. The reward must be given for the last state, while the observations are for the new state.
        if self.pf_for_obs is True:
            self._run_pf()

        # Create new observation in the new state
        obs = self._get_obs(self.obs_keys, self.add_time_obs)

        # Overwrite the episode definition (terminated and truncated)
        terminated = False; truncated = False

        # After n steps = end of episode
        if self.step_in_episode >= self.steps_per_episode:
            terminated = True

        # Enforce train/test-split
        if self.test:
            # Do not accidentally test on train data!
            if new_step in self.train_steps:
                truncated = True
        else:
            # Do not accidentally train on test data!
            if new_step in self.validation_steps or new_step in self.test_steps:
                truncated = True

        return obs, reward, terminated, truncated, info

    def get_optimal_objective(self):
        # Overwrite because not solvable with pandapower OPF solver.
        return 0

    def run_optimal_power_flow(self, **kwargs):
        # Overwrite because not solvable with pandapower OPF solver.
        return False
