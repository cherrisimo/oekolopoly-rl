import oekolopoly.envs.get_boxes as gb
import gym
from gym import spaces
import numpy as np


class OekoEnv(gym.Env):
    
    SANIERUNG       = 0
    PRODUKTION      = 1
    AUFKLAERUNG     = 2
    LEBENSQUALITAET = 3
    VERMEHRUNGSRATE = 4
    UMWELTBELASTUNG = 5
    BEVOELKERUNG    = 6
    POLITIK         = 7
    ROUND           = 8
    POINTS          = 9

    V_NAMES = [
        "Sanierung",
        "Produktion",
        "Aufklärung",
        "Lebensqualität",
        "Vermehrungsrate",
        "Umweltbelastung ",
        "Bevölkerung",
        "Politik",
        "Round",
        "Points",
    ]

    ACT_NAMES = [
        'SANIERUNG',
        'PRODUKTION',
        'AUFKLAERUNG',
        'LEBENSQUALITAET',
        'VERMEHRUNGSRATE',
        'EXTRA',
    ]

    OBS_NAMES = [
        'Sanierung',
        'Produktion',
        'Aufklaerung',
        'Lebensqualitaet',
        'Vermehrungsrate',
        'Umweltbelastung',
        'Bevoelkerung',
        'Politik',
    ]

    def __init__(self):
        self.viewer       = None
 
        self.last_v = None                  
        self.init_v = np.array([
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
        ])

        #                      0   1   2   3   4   5   6    7   8   9
        #                      S   Pr  A   L   V   U   B    P   R   AP
        self.Vmin = np.array([ 1,  1,  1,  1,  1,  1,  1, -10,  0,  0])
        self.Vmax = np.array([29, 29, 29, 29, 29, 29, 48,  37, 30, 36])

        self.Amin = np.array([ 0,-28,  0,  0,  0, -5])
        self.Amax = np.array([28, 28, 28, 28, 28,  5])

        self.action_space = spaces.MultiDiscrete([
            29,   # 0 Sanierung
            57,   # 1 Produktion
            29,   # 2 Aufklärung
            29,   # 3 Lebensqualität
            29,   # 4 Vermehrungsrate
            11,   # 5 box9 Aufklärung > Vermehrung
        ])
        
        self.observation_space = spaces.MultiDiscrete([
            29,   # 0 Sanierung 
            29,   # 1 Produktion
            29,   # 2 Aufklärung
            29,   # 3 Lebensqualität
            29,   # 4 Vermehrungsrate
            29,   # 5 Umweltbelastung
            48,   # 6 Bevölkerung
            48,   # 7 Politik
            31,   # 8 Runde
            37,   # 9 Aktionspunkte für nächste Runde
        ])

        self.done = False
        self.done_info = ''
    
    def close(self):
        if self.viewer:
            self.viewer.close ()
            self.viewer = None 
            
    def render (self, mode='human'):
        from gym.envs.classic_control import rendering
        import pyglet

        if self.viewer is None:
            self.viewer_w = 500
            self.viewer_h = 500
            self.viewer = rendering.Viewer(self.viewer_w, self.viewer_h)
            self.viewer.set_bounds (0, self.viewer_w, 0, self.viewer_h)

        t      = 0.0
        t_step = 0.1 # speed of animation
        t_end  = 3.0 

        print ("Action:", self.curr_action)
        if self.done: print ("Done:", self.done_info)

        while t < t_end:
            self.render_rounds (5,  485, min (t, 1.0)) # progress line, shows number of round
            self.render_action (50,  70, min (t, 1.0)) # 2nd balkeniagramm, A (positionHorizontal, positionVertical, time)
            self.render_vector (50, 200, min (t, 1.0)) # 1st balkeniagramm, V

            self.viewer.render (False)
            t += t_step

    def render_rounds (self, x_offset, y_offset, t):
        v0 = self.prev_result[self.ROUND]
        v1 = self.curr_result[self.ROUND]
        v  = v0 + (v1 - v0) * t # t = 1 show final result, t = 0 show first result, t = 0.5 sth inbetween

        x = x_offset
        y = y_offset
        w = 490
        h = 10

        r = 0.94
        g = 0.94
        b = 0.94

        self.viewer.draw_polygon([ # gray
            (x,   y),
            (x+w, y),
            (x+w, y+h),
            (x,   y+h),
        ], color=(r, g, b))

        w = int (v / self.Vmax[self.ROUND] * w)
        r = 0.6
        g = 0.6
        b = 0.6

        self.viewer.draw_polygon([ # dark gray
            (x,   y),
            (x+w, y),
            (x+w, y+h),
            (x,   y+h),
        ], color=(r, g, b))


    def render_action (self, x_offset, y_offset, t):
        w = 40
        x_stride = 50 # distance between start of one to middle of another, distance = 50 - 40
        h_step = 8    # scale

        bg_x = x_offset - 20
        bg_y = y_offset
        bg_w = x_stride * len (self.ACT_NAMES) + 20 * 2
        bg_h = 10 * h_step

        self.viewer.draw_polygon([
            (bg_x,      bg_y),
            (bg_x+bg_w, bg_y),
            (bg_x+bg_w, bg_y+bg_h),
            (bg_x,      bg_y+bg_h),
        ], color=(0.94, 0.94, 0.94))

        for i in range (len (self.ACT_NAMES)):
            x = i * x_stride + x_offset
            y = y_offset

            v0 = self.prev_action[i]
            v1 = self.curr_action[i]
            v  = v0 + (v1 - v0) * t
            h  = int (v * h_step)

            r = 0.2
            g = 0.2
            b = 1.0

            self.viewer.draw_polygon([
                (x,   y),
                (x+w, y),
                (x+w, y+h),
                (x,   y+h),
            ], color=(r, g, b))


    def render_vector (self, x_offset, y_offset, t):
        w = 40
        x_stride = 50
        h_step = 8

        bg_x = x_offset - 20
        bg_y = y_offset
        bg_w = x_stride * len (self.OBS_NAMES) + 20 * 2
        bg_h = 29 * h_step

        self.viewer.draw_polygon([
            (bg_x,      bg_y),
            (bg_x+bg_w, bg_y),
            (bg_x+bg_w, bg_y+bg_h),
            (bg_x,      bg_y+bg_h),
        ], color=(0.94, 0.94, 0.94))

        for i in range (len (self.OBS_NAMES)):
            x = i * x_stride + x_offset
            y = y_offset

            v0 = self.prev_result[i]
            v1 = self.curr_result[i]
            v  = v0 + (v1 - v0) * t
            h  = int (v * h_step)

            r = (v - self.Vmin[i]) / (self.Vmax[i] - self.Vmin[i])
            r = abs ((r - 0.5) * 2)
            g = 1 - r
            b = 0

            self.viewer.draw_polygon([
                (x,   y),
                (x+w, y),
                (x+w, y+h),
                (x,   y+h),
            ], color=(r, g, b))


    def update_values (self, V, action):
    
        done = False
        done_info = None
        extra_points = action[5]
            
        # Update V and boxes
        box1 = gb.get_box1   (self.V[self.SANIERUNG])
        if not done:
            self.V[self.UMWELTBELASTUNG] += box1
            if self.V[self.UMWELTBELASTUNG] not in range (1, 30):
                done = True
                done_info = "Umweltbelastung "+str(self.V[ self.UMWELTBELASTUNG])+" ist außerhalb des zulässigen Ranges"
        
        if not done:
            box2 = gb.get_box2   (self.V[self.SANIERUNG])
            self.V[self.SANIERUNG] += box2
            if self.V[self.SANIERUNG] not in range (1, 30):
                done = True
                done_info = "Sanierung "+str(self.V[ self.SANIERUNG])+" ist außerhalb des zulässigen Ranges"
        
        if not done:
            box3 = gb.get_box3   (self.V[self.PRODUKTION])
            self.V[ self.PRODUKTION] += box3
            if self.V[ self.PRODUKTION] not in range (1, 30):
                done = True
                done_info = "Produktion "+str(self.V[ self.PRODUKTION])+" ist außerhalb des zulässigen Ranges"

        if not done:
            box4 = gb.get_box4   (self.V[self.PRODUKTION])
            self.V[self.UMWELTBELASTUNG] += box4
            if self.V[self.UMWELTBELASTUNG] not in range (1, 30):
                done = True
                done_info = "Umweltbelastung "+str(self.V[ self.UMWELTBELASTUNG])+" ist außerhalb des zulässigen Ranges"
        

        if not done:
            box5 = gb.get_box5   (self.V[self.UMWELTBELASTUNG])
            self.V[self.UMWELTBELASTUNG] += box5
            if self.V[self.UMWELTBELASTUNG] not in range (1, 30):
                done = True
                done_info = "Umweltbelastung "+str(self.V[ self.UMWELTBELASTUNG])+" ist außerhalb des zulässigen Ranges"

        if not done:
            box6 = gb.get_box6   (self.V[self.UMWELTBELASTUNG])
            self.V[self.LEBENSQUALITAET]  += box6
            if self.V[self.LEBENSQUALITAET] not in range (1, 30):
                done = True
                done_info = "Lebensqualitaet "+str(self.V[ self.LEBENSQUALITAET])+" ist außerhalb des zulässigen Ranges"

        if not done:
            box7 = gb.get_box7   (self.V[self.AUFKLAERUNG])
            self.V[self.AUFKLAERUNG] += box7
            if self.V[self.AUFKLAERUNG] not in range (1, 30):
                done = True
                done_info = "Aufklaerung "+str(self.V[ self.AUFKLAERUNG])+" ist außerhalb des zulässigen Ranges"
            
            
        if not done:
            box8 = gb.get_box8   (self.V[self.AUFKLAERUNG])
            self.V[self.LEBENSQUALITAET]  += box8
            if self.V[self.LEBENSQUALITAET] not in range (1, 30):
                done = True
                done_info = "Lebensqualitaet "+str(self.V[ self.LEBENSQUALITAET])+" ist außerhalb des zulässigen Ranges"
        

        if not done:
            if self.V[self.AUFKLAERUNG] in range (21, 24): extra_points = max (-3, min (3, extra_points))
            if self.V[self.AUFKLAERUNG] in range (24, 28): extra_points = max (-4, min (4, extra_points))
            if self.V[self.AUFKLAERUNG] in range (28, 30): extra_points = max (-5, min (5, extra_points))
            if self.V[self.AUFKLAERUNG] < 21: extra_points = 0
            box9 = gb.get_box9   (self.V[self.AUFKLAERUNG], extra_points)
            self.V[self.VERMEHRUNGSRATE] += box9
            if self.V[self.VERMEHRUNGSRATE] not in range (1, 30):
                done = True
                done_info = "Vermehrungsrate "+str(self.V[ self.VERMEHRUNGSRATE])+" ist außerhalb des zulässigen Ranges"


        if not done:
            box10 = gb.get_box10 (self.V[self.LEBENSQUALITAET])
            self.V[ self.LEBENSQUALITAET]  += box10
            if self.V[self.LEBENSQUALITAET] not in range (1, 30):
                done = True
                done_info = "Lebensqualitaet "+str(self.V[ self.LEBENSQUALITAET])+" ist außerhalb des zulässigen Ranges"
            

        if not done:
            box11 = gb.get_box11 (self.V[self.LEBENSQUALITAET])
            self.V[ self.VERMEHRUNGSRATE] += box11
            if self.V[self.VERMEHRUNGSRATE] not in range (1, 30):
                done = True
                done_info = "Vermehrungsrate "+str(self.V[ self.VERMEHRUNGSRATE])+" ist außerhalb des zulässigen Ranges"
        

        if not done:
            box12 = gb.get_box12 (self.V[self.LEBENSQUALITAET])
            self.V[self.POLITIK] += box12
            if self.V[self.POLITIK] not in range (-10, 38):
                done = True
                done_info = "Politik "+str(self.V[ self.POLITIK])+" ist außerhalb des zulässigen Ranges"

        if not done:
            box13 = gb.get_box13 (self.V[self.VERMEHRUNGSRATE])
            boxW  = gb.get_boxW  (self.V[ self.BEVOELKERUNG])
            self.V[self.BEVOELKERUNG] += box13 * boxW
            if self.V[self.BEVOELKERUNG] not in range (1, 49):
                done = True
                done_info = "Bevoelkerung "+str(self.V[ self.BEVOELKERUNG])+" ist außerhalb des zulässigen Ranges"
        

        if not done:
            box14 = gb.get_box14 (self.V[self.BEVOELKERUNG])
            self.V[ self.LEBENSQUALITAET] += box14
            if self.V[self.LEBENSQUALITAET] not in range (1, 30):
                done = True
                done_info = "Lebensqualitaet "+str(self.V[ self.LEBENSQUALITAET])+" ist außerhalb des zulässigen Ranges"

        return  self.V, done, done_info
    
    
    def step (self, action):
        assert self.action_space.contains (action), f"AssertionError: action not in action_space: {action}"

        # Transform action space
        action = action + self.Amin
        self.prev_action = self.curr_action
        self.curr_action = action.copy ()
        
        # Init
        done = False
        self.reward = 0
        self.reward_points = 0
        self.balance = 0
        used_points = 0
        
        # Sum points from action
        used_points += action[self.SANIERUNG]
        used_points += abs (action[self.PRODUKTION])
        used_points += action[self.AUFKLAERUNG]
        used_points += action[self.LEBENSQUALITAET]
        used_points += action[self.VERMEHRUNGSRATE]

        if used_points < 0 or used_points > self.V[self.POINTS]:
            return self.obs, self.reward, done, {'balance': self.balance, 'done_reason': None, 'reward_points': self.reward_points, 'valid_move': False, 'invalid_move_info': "Zu viele Aktionspunkte werden für diese Runde verbraucht."}
        assert used_points >= 0 and used_points <= self.V[self.POINTS], f"AssertionError: action takes too many points: action={action} POINTS={self.V[self.POINTS]})"

        for i in range(5):
            if self.V[i] + action[i] not in range (self.Vmin[i], self.Vmax[i] + 1):
                return self.obs, self.reward, done, {'balance': self.balance, 'done_reason': None, 'reward_points': self.reward_points, 'valid_move': False, 'invalid_move_info': f"Zu viele Aktionspunkte werden in {self.V_NAMES[i]} investiert."}
            assert (self.V[i] + action[i]) in range (self.Vmin[i], self.Vmax[i] + 1), f"AssertionError: action puts region out of action[{i}]: action={action} V={self.V}"

        # The turn is valid

        for i in range(5): self.V[i] += action[i]

        # Update boxes and V accordingly
        self.V, done, done_info = self.update_values(self.V, action)

        # Update points and round 
        self.V[self.POINTS] -= used_points            
        self.V[self.ROUND] += 1

        # Clip values if not in range
        for i in range(8):
            if  self.V[i] not in range (self.Vmin[i],  self.Vmax[i] + 1):
                self.V[i] = max( self.Vmin[i], min( self.Vmax[i],  self.V[i]))
                done = True

        if  self.V[self.ROUND] == 30:
            done = True
            done_info = 'Maximale Anzahl von Runden erreicht'

        # Points for next round
        if done:
            self.V[self.POINTS] = 0
        else:
            boxA  = gb.get_boxA  (self.V[self.BEVOELKERUNG])
            boxB  = gb.get_boxB  (self.V[self.POLITIK])
            boxC  = gb.get_boxC  (self.V[self.PRODUKTION])
            boxV  = gb.get_boxV  (self.V[self.PRODUKTION])
            boxD  = gb.get_boxD  (self.V[self.LEBENSQUALITAET])

            self.V[self.POINTS] += boxA * boxV
            self.V[self.POINTS] += boxB
            self.V[self.POINTS] += boxC
            self.V[self.POINTS] += boxD

        if  self.V[self.POINTS] < 0:
            self.V[self.POINTS] = 0
            done = True
            done_info = 'Minimale Anzahl von Aktionspunkten erreicht'

        if  self.V[self.POINTS] > 36:
            self.V[self.POINTS] = 36
            done = True
            done_info = 'Maximale Anzahl von Aktionspunkten erreicht'

        boxD  = gb.get_boxD  (self.V[self.LEBENSQUALITAET])
        self.a = float ((boxD*3 + self.V[self.POLITIK]) * 10)
        self.reward_points = int (self.a)
        self.b = float(self.V[self.ROUND] + 3)

        if done and self.V[self.ROUND] in range(10, 31):
            self.balance = round (float(self.a / self.b), 2)

        # Transform V in obs
        self.obs = self.V - self.Vmin
        assert self.observation_space.contains(self.obs), f"AssertionError: obs not in observation_space: obs={self.obs}"

        self.reward = self.get_oeko_reward (done) 

        self.prev_result = self.curr_result
        self.curr_result = self.V.copy ()
        
        # print("Reward_points:", self.reward_points)
        # print("Balance:", self.balance)
        # print("Reward:", self.reward)

        self.last_v    = self.V.copy ()                               
        self.done      = done
        self.done_info = done_info
        
        #self.reward = 0
        return self.obs, self.reward, done, {'balance': self.balance, 'done_reason': done_info, 'reward_points': self.reward_points, 'valid_move': True, 'invalid_move_info': ''}

    def get_oeko_reward (self, done):
        if done and self.V[self.ROUND] in range(10, 31):
            return self.balance
        else:
            return 0


    def get_initial_v (self):
        return self.init_v.copy ()


    def set_v (self, init_v):
        self.init_v = init_v


    def reset(self,v=None):
        if v is None:
            self.V = self.get_initial_v()
        else:
            self.V = np.array(v)            # non-default initial values v

        self.curr_action = np.zeros (self.action_space.shape[0], 'int64')
        self.curr_result = self.V.copy ()

        self.obs = self.V - self.Vmin
        assert self.observation_space.contains (self.obs), "AssertionError: obs not in observation_space"
        
        return self.obs
