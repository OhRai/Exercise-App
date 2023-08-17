# Exercise App - Rep Counter

This app is designed to help you keep track of your exercise reps in a user-friendly and efficient way. Whether you're into bicep curls, push-ups, squats, or deadlifts, this app has got you covered. It is powered by Tensorflow and Google's MoveNet Model, and your workout tracking experience is about to get a whole lot smarter!

Now you don't have to get distracted trying to remember how many reps you did while working out!
![](examples/example1.gif)
![](examples/example2.gif)

## Currently Supported Exercises
- Push-ups
- Bicep Curls
- Squats
- Deadlifts

Each exercise has its own logic for counting reps. The logic can be found within the exercises folder, and a README will be included explaining each logic.

## Things I Used
- OpenCV: using my webcam and allowing me to implement my models
- Tensorflow: Machine learning and using the movenet model
- Figma: Designing the UI of the app

## Google's MoveNet Model
I chose this model because it's one of, if not, the fastest pose detection models out there. By using the lightning model, I was able to get 30-60 FPS on average, and about 10-20 FPS with the thunder model. I used the keypoints given to me from these models and created logic for each counter.

To use the models, use the following code: 
```Python
# The models you can use are 'thunder' for accuracy and 'lightning' for speed 
from utils.models import model
model_type, input_size = model('model_name')
```
The model_type will be used for the interpreter and the input_size will be used for resizing the frame.

## Installation and Usage
1. Clone the repo: 
```
git clone https://github.com/OhRai/exercise-app.git
cd exercise-tracking-app
```

2. Setup up a virtual environment:
```
python -m venv name_of_virtual_env
```

3. Install the dependencies:
```
pip install -r requirements.txt
```

4. Go into the main.py file and change the VideoCapture under the "Load Interface and Video Capture" section to either a video file or your camera by using an integer (0 is usually the default number)
```Python
cap = cv2.VideoCapture('data/video.mp4') # For video files
cap = cv2.VideoCapture(0) # For webcam feed
```
If 0 doesn't work, try playing around with other integers like 1, 2, 3, 4, etc...

5. Run the main.py script:
```
python main.py
```
To exit the app, press "q".

## Project Structure
The project is organized as follows:
- exercises/: Contains exercise-specific counter classes
- utils/: Includes utility functions and models for keypoints detection
- data/: Holds any video clips and files to use for the app
- app_ui/: Contains UI

# Final Thoughts
This is a fun way to end the summer! I personally love exercising and working out, however sometimes I get distracted by counting how many reps I did, then end up doing too little or too much. I used some of the things I learnt in first year at Waterloo such as Linear Algebra and some of my own personal experiences such as having a proper form for a certain exercise for this app.

Here are some things I can do in the future: 
* Add more exercises
* Make it into a mobile app
* Add more functionality and cutomization such as: 
    - Timers
    - How many reps you want to do
    - Sounds/buzzers to let you know when you're done
    - Form/posture corrector
    - Integrate into other exercise apps such as Strong

Things to improve on: 
- Remake the bicep curl logic or fix it, as it may increment in reps when it shouldn't 
- Use a dependency like Tkinter, Kivy, PySimpleGUI, etc...