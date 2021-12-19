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

        return v
