import numpy as np
from utils.keypoints import keys
from utils.angle import calculate_angle

class PushUpCounter:
    def __init__(self):
        self.total_reps = 0
        self.position = 'up'
        self.angles = []
    
    def count_pushup(self, frame, keypoints, threshold):
        y, x, _ = frame.shape

        ka = keys['right_elbow']
        kb = keys['nose']

        a = np.squeeze(keypoints[0][0][ka][:2] * [y, x])
        b = np.squeeze(keypoints[0][0][kb][:2] * [y, x])

        elbow = a[0]
        nose = b[0]

        conf_a = keypoints[0][0][ka][2]
        conf_b = keypoints[0][0][kb][2]

        angle = calculate_angle(frame, keypoints, keys['right_wrist'], keys['right_elbow'], keys['right_shoulder'], 0.2)
        self.angles.append(angle)

        if self.angles[-1] == None and len(self.angles) > 2:
            self.angles[-1] = self.angles[-2]
        elif self.angles[-1] == None and len(self.angles) < 2:
            self.angles[-1] = 180
        
        if (conf_a > threshold) and (conf_b > threshold):
            if self.position == 'up':
                if (elbow < nose) and (self.angles[-1] < 100):
                    self.position = 'down'
                    # print(self.position)

            elif self.position == 'down':
                if self.angles[-1] > 150:
                    self.total_reps += 1
                    self.position = 'up'
                    # print(self.position)

        return self.total_reps
