import numpy as np
from utils.keypoints import keys

def calculate_angle(frame, keypoints, ka, kb, kc, threshold):
    y, x, _ = frame.shape

    a = np.squeeze(keypoints[0][0][ka][:2] * [y, x])
    b = np.squeeze(keypoints[0][0][kb][:2] * [y, x]) 
    c = np.squeeze(keypoints[0][0][kc][:2] * [y, x])

    conf_a = keypoints[0][0][ka][2]
    conf_b = keypoints[0][0][kb][2]
    conf_c = keypoints[0][0][kc][2]

    if (conf_a > threshold) and (conf_b > threshold) and (conf_c > threshold):

        vector_ab = a - b
        vector_bc = c - b

        dot_product = np.dot(vector_ab, vector_bc)

        mag_ab = np.linalg.norm(vector_ab)
        mag_bc = np.linalg.norm(vector_bc)

        complementary_cosine = 1 - dot_product / (mag_ab * mag_bc)
        normalized_angle = (complementary_cosine / 2) * 180

        angle = int(normalized_angle)

        return angle
