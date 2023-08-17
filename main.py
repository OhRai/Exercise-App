import cv2
import numpy as np
import tensorflow as tf
from PIL import ImageFont, ImageDraw, Image

# Load Model
from utils.models import model
from utils.keypoints import draw_keypoints, draw_edges, edges

# Initialize TensorFlow Lite Interpreter
model_type, input_size = model('thunder')
interpreter = tf.lite.Interpreter(model_path=model_type)
interpreter.allocate_tensors()

# Exercise Class Initializer
from exercises.push_up import PushUpCounter
from exercises.bicep_curl import CurlCounter
from exercises.squat import SquatCounter
from exercises.deadlift import DeadliftCounter

push_up = PushUpCounter()
curl_counter = CurlCounter()
squat_counter = SquatCounter()
deadlift_counter = DeadliftCounter()

# Load Interface and Video Capture
interface = cv2.imread('app_ui/main.png')
cap = cv2.VideoCapture('data/video7.mp4')
clean_interface = interface.copy()

# Initialize UI Position and Exercise Variables
push_pos = [(720, 308), (720+240, 308+65)]
bicep_pos = [(1000, 308), (1000+240, 308+65)]
squat_pos = [(720, 411), (720+240, 411+65)]
deadlift_pos = [(1000, 411), (1000+240, 411+65)]

font = ImageFont.truetype('app_ui/roboto.ttf', 36)
total_reps = 0
exercise = 'Push-up'

# Button Click Event Handler
def button_click(event, x, y, flags, param):
    global exercise, total_reps, push_up, curl_counter, squat_counter, deadlift_counter
    if event == cv2.EVENT_LBUTTONDOWN:
        if push_pos[0][0] <= x <= push_pos[1][0] and push_pos[0][1] <= y <= push_pos[1][1]:
            exercise = 'Push-up'
            push_up = PushUpCounter()
        if bicep_pos[0][0] <= x <= bicep_pos[1][0] and bicep_pos[0][1] <= y <= bicep_pos[1][1]:
            exercise = 'Bicep Curl'
            curl_counter = CurlCounter()
        if squat_pos[0][0] <= x <= squat_pos[1][0] and squat_pos[0][1] <= y <= squat_pos[1][1]:
            exercise = 'Squat'
            squat_counter = SquatCounter()
        if deadlift_pos[0][0] <= x <= deadlift_pos[1][0] and deadlift_pos[0][1] <= y <= deadlift_pos[1][1]:
            exercise = 'Deadlift'
            deadlift_counter = DeadliftCounter()

# Set up UI Window and Mouse Click Event
cv2.namedWindow('Exercise App')
cv2.setMouseCallback('Exercise App', button_click)

# Video Loop
while cap.isOpened():
    # Setup Background and Camera
    interface = clean_interface.copy()
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Ensure Frame Aspect Ratio
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if (width > height): 
        border_size = (width - height) // 2
        frame = cv2.copyMakeBorder(frame, border_size, border_size, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    
    else: 
        border_size = (height - width) // 2
        frame = cv2.copyMakeBorder(frame, 0, 0, border_size, border_size, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    frame = cv2.resize(frame, (640, 640))

    # Model Camera
    img = frame.copy()
    img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 256, 256)
    input_image = tf.cast(img, dtype=tf.float32)

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
    interpreter.invoke()
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])

    # Process Functions and Exercises
    draw_keypoints(frame, keypoints_with_scores, 0.2)
    draw_edges(frame, keypoints_with_scores, edges, 0.2)

    if exercise == 'Push-up':
        total_reps = push_up.count_pushup(frame, keypoints_with_scores, 0.2)
    elif exercise == 'Bicep Curl':
        total_reps = curl_counter.count_curl(frame, keypoints_with_scores, 0.2)
    elif exercise == 'Squat':
        total_reps = squat_counter.count_squat(frame, keypoints_with_scores, 0.2)  
    elif exercise == 'Deadlift':
        total_reps = deadlift_counter.count_deadlift(frame, keypoints_with_scores, 0.2)  

    # Update Frame and Text
    img_pil = Image.fromarray(interface)
    draw = ImageDraw.Draw(img_pil)

    draw.text((1040, 62), exercise, font=font, fill=(0, 0, 0), antialias=True)
    draw.text((1040, 113), str(total_reps), font=font, fill=(0, 0, 0), antialias=True)

    interface = np.array(img_pil)
    interface[40:640+40, 40:640+40] = frame

    # Show Frame
    cv2.imshow('Exercise App', interface)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
