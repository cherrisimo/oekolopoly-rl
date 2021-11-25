from oekolopoly.envs.oeko_env import OekoEnv


class OekoEnvRew2(OekoEnv):
    def get_oeko_reward (self, done):
        if done:
            return self.balance
        else:
            return 1
