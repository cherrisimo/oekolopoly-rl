# -*- coding: utf-8 -*-
"""
    A small script to run or debug an Oekolopoly agent trained via rl-baselines3-zoo
    without rl-baselines3-zoo.
    This script can be run or debugged from Spyder.
    Instead of enjoy's command line switches use the uppercase variables below
        P_DETERMIN, TIMESTEPS, PATH, MODEL, ...
"""

import os
import sys
#import numpy as np

from stable_baselines3 import PPO
#from stable_baselines3.common.monitor import Monitor
#from gym.wrappers import TimeLimit
from wrappers.wrappers import OekoBoxActionWrapper
from wrappers.wrappers import OekoSimpleActionWrapper

scriptpath = "oekolopoly/"
sys.path.append(os.path.abspath(scriptpath))
from oekolopoly.envs.oeko_env import OekoEnv

P_DETERMIN = False    # predict deterministically or not (recommended: True)
TIMESTEPS = 22
PATH = "oekolopoly_agents/ppo/Oekolopoly-v0_88/"
MODEL = PATH+"best_model"       # works
#MODEL = PATH+"Oekolopoly-v0"    # 'Permission denied' error - but in reality it is a name problem of "Oekolopoly-v0"
#MODEL = PATH+"Oekolopoly_v0"    # works, if "Oekolopoly-v0.zip" is renamed to "Oekolopoly_v0.zip"
#MODEL = "Oekolopoly-v0"         # works as well, but requires nasty copying to current dir

env = OekoBoxActionWrapper(OekoEnv())
#env = OekoSimpleActionWrapper(OekoEnv())
# the type of wrapper is infered from PATH/Oekolopoly-v0/config.yml, field env_wrapper

# The following lines borrowed from enjoy.py (rl-baselines3-zoo):
newer_python_version = sys.version_info.major == 3 and sys.version_info.minor >= 8
custom_objects = {}
if newer_python_version:
    custom_objects = {
        "learning_rate": 0.0,
        "lr_schedule": lambda _: 0.0,
        "clip_range": lambda _: 0.0,
    }
model = PPO.load(MODEL, env=env,custom_objects=custom_objects)  

tot_reward=0
env.seed(42)
obs = env.reset()
print("obs = ",obs)

state = None
for i in range(TIMESTEPS):
    action, state = model.predict(obs,state=state,deterministic=P_DETERMIN)
    #action = [66,2]
    print(action)

    obs, reward, done, info = env.step(action)
    tot_reward += reward # rewards[0]
    env.render()   # may give problems (under Spyder) to close this window
    if done:
        print('i+1={}: Total Reward: {}'.format(i+1,tot_reward))
        tot_reward=0
        obs = env.reset()
    
env.close()

