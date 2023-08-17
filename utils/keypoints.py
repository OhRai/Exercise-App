import cv2
import numpy as np

keys = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}

edges = {
    (0, 1): 'm', 
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

color_mapping = {
    'm': (255, 0, 255),
    'c': (0, 255, 255),
    'y': (255, 255, 0)
}

def draw_keypoints(frame, keypoints, threshold):
  y, x, _ = frame.shape
  shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

  for kp in shaped:
    ky, kx, conf = kp
    if conf > threshold:
      cv2.circle(frame, (int(kx), int(ky)), 4, (0, 255, 0), -1)

def draw_edges(frame, keypoints, edges, threshold):
  y, x, _ = frame.shape
  shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

  for edge, color_code in edges.items():
    p1, p2 = edge
    y1, x1, c1 = shaped[p1]
    y2, x2, c2 = shaped[p2]

    if (c1 > threshold) & (c2 > threshold):
      color = color_mapping.get(color_code)  
      cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)