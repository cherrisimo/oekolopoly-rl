from oekolopoly.envs.oeko_env import OekoEnv


class OekoEnvRew4(OekoEnv):
    def get_oeko_reward (self, done):
        if done:
            return self.balance
        else:
            production_reward   = 14 - abs (15 - self.V[self.PRODUKTION])
            bevoelkerung_reward = 23 - abs (24 - self.V[self.BEVOELKERUNG])
            return production_reward + bevoelkerung_reward + self.balance
