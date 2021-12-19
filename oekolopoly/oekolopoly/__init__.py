from gym.envs.registration import register
import gym

env_dict = gym.envs.registration.registry.env_specs.copy()
for env in env_dict:
    if 'Oekolopoly-v0' in env:
         del gym.envs.registration.registry.env_specs[env]
    if 'OekolopolyRew2-v0' in env:
         del gym.envs.registration.registry.env_specs[env]
    if 'OekolopolyRew3-v0' in env:
         del gym.envs.registration.registry.env_specs[env]
    if 'OekolopolyRew4-v0' in env:
         del gym.envs.registration.registry.env_specs[env]
    if 'OekolopolyRandom-v0' in env:
         del gym.envs.registration.registry.env_specs[env]
    if 'OekolopolyRandomRew2-v0' in env:
         del gym.envs.registration.registry.env_specs[env]

register(
    id='Oekolopoly-v0',
    entry_point='oekolopoly.envs:OekoEnv',
)
register(
    id='OekolopolyRew2-v0',
    entry_point='oekolopoly.envs:OekoEnvRew2',
)
register(
    id='OekolopolyRew3-v0',
    entry_point='oekolopoly.envs:OekoEnvRew3',
)
register(
    id='OekolopolyRew4-v0',
    entry_point='oekolopoly.envs:OekoEnvRew4',
)
register(
    id='OekolopolyRandom-v0',
    entry_point='oekolopoly.envs:OekoEnvRandom',
)
register(
    id='OekolopolyRandomRew2-v0',
    entry_point='oekolopoly.envs:OekoEnvRandomRew2',
)
