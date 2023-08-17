import numpy as np
from utils.keypoints import keys
from utils.angle import calculate_angle

class DeadliftCounter:
    def __init__(self):
        self.total_reps = 0
        self.position = 'up'
        self.angles = []
    
    def count_deadlift(self, frame, keypoints, threshold):
        y, x, _ = frame.shape

        ka = keys['right_elbow']
        kb = keys['right_knee']

        a = np.squeeze(keypoints[0][0][ka][:2] * [y, x])
        b = np.squeeze(keypoints[0][0][kb][:2] * [y, x])

        elbow = a[0]
        knee = b[0]

        conf_a = keypoints[0][0][ka][2]
        conf_b = keypoints[0][0][kb][2]
        
        margin = 50

        angle = calculate_angle(frame, keypoints, keys['right_hip'], keys['right_knee'], keys['right_ankle'], 0.2)

        if angle != None: 
            self.angles.append(angle)
        
        if (conf_a > threshold) and (conf_b > threshold):
            if self.position == 'up':
                if (elbow + margin > knee) and (self.angles[-1] < 120):
                    self.position = 'down'
                    # print(self.position)

            elif self.position == 'down':
                if (elbow < knee) and (self.angles[-1] > 170):
                    self.total_reps += 1
                    self.position = 'up'
                    # print(self.position)

        return self.total_reps
