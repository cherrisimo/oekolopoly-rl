from math import floor
import gym
import numpy as np

def distribute1 (action, points):
    action = list (action)
    action_sum = sum (action)

    if action_sum > 1:
        for i in range (len (action)):
            action[i] = action[i] / action_sum


    r = []
    for n in action:
        r.append (round (n * points))

    while sum (r) > points:
        max_index = r.index (max (r))
        r[max_index] -= 1

    assert sum (r) <= points

    return r


def distribute2 (action, points, used_points_p):
    points = round (points * used_points_p)

    action = list (action)
    action_sum = sum (action)
    if action_sum == 0:
        action = [1] * len (action)
        action_sum = sum (action)

    for i in range (len (action)):
        action[i] /= action_sum

    r = []
    for n in action:
        r.append (round (n * points))

    if sum (r) > points:
        max_index = action.index (max (action))
        r[max_index] -= 1
    elif sum (r) < points:
        max_index = action.index (max (action))
        r[max_index] += 1

    assert sum (r) == points

    return r


class OekoEnvBoxWrapper(gym.ActionWrapper):
    def __init__ (self, env):
        super().__init__(env)
        self.action_space = gym.spaces.Box (
            np.float32 (np.array ([0, -1,  0,  0,  0, -1])),
            np.float32 (np.array ([1,  1,  1,  1,  1,  1]))
        )

    def action (self, act):
        assert self.action_space.contains (act), "AssertionError: action not in action_space"

        if act[1] < 0:
            act[1] = -act[1]
            reduce_production = True
        else:
            reduce_production = False

        regions_act = act[0:5]
        special_act = round (act[5] * 5)
        regions_act = distribute1 (regions_act, self.V[self.POINTS])
        if reduce_production: regions_act[1] = -regions_act[1]

        for i in range (len (regions_act)):
            region_result = self.V[i] + regions_act[i]
            if   region_result < self.Vmin[i]: regions_act[i] = self.Vmin[i] - self.V[i]
            elif region_result > self.Vmax[i]: regions_act[i] = self.Vmax[i] - self.V[i]

        act = np.append (regions_act, special_act)
        act -= self.Amin
        return act


def OekoBoxEnv ():
    env = gym.make('oekolopoly:Oekolopoly-v0')
    env = OekoEnvBoxWrapper (env)
    return env


if __name__ == '__main__':
    env = OekoBoxEnv ()
    env.reset ()
    env.step (np.array ([0.0, -1.00, 0.0, 0.0, 0.0, -1.00]))
    env.step (np.array ([0.0, -0.95, 0.0, 0.0, 0.0, -0.95]))
    env.step (np.array ([0.0,  0.95, 0.0, 0.0, 0.0,  0.95]))
    env.step (np.array ([0.0,  1.00, 0.0, 0.0, 0.0,  1.0]))
