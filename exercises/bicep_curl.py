import numpy as np
from utils.keypoints import keys
from utils.angle import calculate_angle

class CurlCounter:
    def __init__(self):
        self.total_reps = 0
        self.position = 'down'
        self.angles1 = []
        self.angles2 = []
    
    def count_curl(self, frame, keypoints, threshold):
        y, x, _ = frame.shape

        ka = keys['right_wrist']
        kb = keys['right_shoulder']

        a = np.squeeze(keypoints[0][0][ka][:2] * [y, x]) # Wrist
        b = np.squeeze(keypoints[0][0][kb][:2] * [y, x]) # Shoulder

        ay = a[0]
        by = b[0]

        margin = 50

        conf_a = keypoints[0][0][ka][2]
        conf_b = keypoints[0][0][kb][2]

        angle1 = calculate_angle(frame, keypoints, keys['left_wrist'], keys['left_elbow'], keys['left_shoulder'], 0.2)
        angle2 = calculate_angle(frame, keypoints, keys['right_wrist'], keys['right_elbow'], keys['right_shoulder'], 0.2)

        if angle1 != None: 
            self.angles1.append(angle1)

        if angle2 != None: 
            self.angles2.append(angle2)

        if len(self.angles1) < 2:
            self.angles1.append(angle1)

        if len(self.angles2) < 2:
            self.angles2.append(angle2)

        if (conf_a > threshold) and (conf_b > threshold):
            if self.position == 'down':
                if (ay - margin < by) and (self.angles1[-1] < 30 or self.angles2[-1] < 30):
                    self.position = 'up'
            elif self.position == 'up':
                if ay + margin > by and (self.angles1[-1] > 165 or self.angles2[-1] > 165):
                    self.total_reps += 1
                    self.position = 'down'

        return self.total_reps

# -------------------- Usage --------------------
# Outside of loop
# curl_counter = CurlCounter()

# angles = []
# total_reps = 0

# prev_time = time.time()

# Inside of loop
# curr_time = time.time()
# elapsed = curr_time - prev_time

# angle = calculate_angle(frame, keypoints_with_scores, keys['left_wrist'], keys['left_elbow'], keys['left_shoulder'], 0.2)

# if elapsed >= 0.2:
#         angles.append(angle)
#         prev_time = curr_time
#         total_reps = curl_counter.count_curl(frame, keypoints_with_scores, 0.2, angles)
#         print(total_reps)

# cv2.putText(frame, str(total_reps), (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)