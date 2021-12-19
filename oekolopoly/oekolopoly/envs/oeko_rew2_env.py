from oekolopoly.envs.oeko_env import OekoEnv


class OekoEnvRew2(OekoEnv):
    def get_oeko_reward (self, done):
        if done and self.V[self.ROUND] in range(10, 31):
            return self.balance
        else:
            return 1
