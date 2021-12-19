from oekolopoly.envs.oeko_env import OekoEnv
import numpy as np
import random


class OekoEnvRandom (OekoEnv):
    def get_initial_v (self):
        v = [
            np.array([
            1,  #0 Sanierung
            12, #1 Produktion
            4,  #2 Aufklärung
            10, #3 Lebensqualität
            20, #4 Vermehrungsrate
            13, #5 Umweltbelastung 
            21, #6 Bevölkerung
            0,  #7 Politik
            0,  #8 Round
            8,  #9 Points
            ]),
            
            np.array([
            1,  #0 Sanierung
            9, #1 Produktion
            2,  #2 Aufklärung
            7, #3 Lebensqualität
            24, #4 Vermehrungsrate
            8, #5 Umweltbelastung 
            24, #6 Bevölkerung
            0,  #7 Politik
            0,  #8 Round
            8,  #9 Points
            ])
            
        ]
        
        v = random.choice(v)
        print(v)
        # v = np.array([
            # # random.randrange (self.Vmin[0], self.Vmax[0]),  #0 Sanierung
            # # random.randrange (self.Vmin[1], self.Vmax[1]),  #1 Produktion
            # # random.randrange (self.Vmin[2], self.Vmax[2]),  #2 Aufklärung
            # # random.randrange (self.Vmin[3], self.Vmax[3]),  #3 Lebensqualität
            # # random.randrange (self.Vmin[4], self.Vmax[4]),  #4 Vermehrungsrate
            # # random.randrange (self.Vmin[5], self.Vmax[5]),  #5 Umweltbelastung 
            # # random.randrange (self.Vmin[6], self.Vmax[6]),  #6 Bevölkerung
            # # random.randrange (self.Vmin[7], self.Vmax[7]),  #7 Politik
            # # 0,                                              #8 Round
            # # random.randrange (self.Vmin[9], self.Vmax[9]),  #9 Points
            
            # # 1,  #0 Sanierung
            # # 12, #1 Produktion
            # # 4,  #2 Aufklärung
            # # 10, #3 Lebensqualität
            # # 20, #4 Vermehrungsrate
            # # 13, #5 Umweltbelastung 
            # # 21, #6 Bevölkerung
            # # 0,  #7 Politik
            # # 0,  #8 Round
            # # 8,  #9 Points
        # ])

        return v
